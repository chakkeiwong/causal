"""
Lineage graph: append-only, hash-chained event log per P7.

Chapter 12 principle P7: Append-only hash-chained lineage.

Components integrate ONLY through the lineage graph. No direct calls.
The graph is tamper-evident: if any historical event is modified, the chain breaks.
"""

import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

import duckdb

from .types import LineageEvent, LineageEventType, RunID


def _canonical_default(obj: Any) -> Any:
    """
    Coerce non-JSON types to a canonical, stable representation.

    P5 requires bit-identical replay, so the encoding of any given value must
    never vary between runs. numpy scalars and pandas/NumPy datetimes arrive here
    from component metadata (counts, quantiles, timestamps) and must serialise
    the same way every time.

    Raises TypeError for anything unrecognised rather than guessing: a silently
    coerced value would produce a hash that cannot be reproduced.
    """
    # numpy scalars expose .item() -> Python int/float/bool/str
    item = getattr(obj, "item", None)
    if callable(item) and getattr(obj, "shape", None) == ():
        return item()
    if hasattr(obj, "tolist"):  # numpy arrays
        return obj.tolist()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        # str() preserves the exact decimal, unlike float()
        return str(obj)
    if isinstance(obj, (set, frozenset)):
        return sorted(obj, key=repr)
    raise TypeError(f"Object of type {type(obj).__name__} is not hashable into lineage")


def _compute_content_hash(parent_hash: Optional[str], event_data: Dict[str, Any]) -> str:
    """
    Compute SHA-256 hash of (parent_hash || event_data).

    Forms a tamper-evident chain: if any historical event changes, chain breaks.

    Args:
        parent_hash: Hash of previous event in chain, or None for genesis
        event_data: Event metadata as dict

    Returns:
        64-character hex SHA-256 hash
    """
    sha256 = hashlib.sha256()
    if parent_hash:
        sha256.update(parent_hash.encode("utf-8"))
    # Canonical JSON: sorted keys, no whitespace, stable coercion of numpy/datetime
    canonical = json.dumps(
        event_data, sort_keys=True, separators=(",", ":"), default=_canonical_default
    )
    sha256.update(canonical.encode("utf-8"))
    return sha256.hexdigest()


class LineageGraph:
    """
    Append-only, hash-chained lineage graph.

    All components write events here. No component calls another component directly.

    Schema:
        CREATE TABLE lineage_events (
            event_id INTEGER PRIMARY KEY,
            run_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            event_type TEXT NOT NULL,
            component TEXT NOT NULL,
            dataset TEXT NOT NULL,
            partition TEXT NOT NULL,
            metadata JSON NOT NULL,
            parent_run_id TEXT,
            content_hash TEXT NOT NULL,
            prev_hash TEXT  -- hash of previous event, forms chain
        );
        CREATE INDEX idx_lineage_run ON lineage_events(run_id);
        CREATE INDEX idx_lineage_dataset ON lineage_events(dataset, partition);
        CREATE INDEX idx_lineage_type ON lineage_events(event_type);
    """

    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize lineage graph.

        Args:
            db_path: DuckDB database path; ":memory:" for in-memory (testing only)
        """
        self.conn = duckdb.connect(db_path)
        self._create_schema()

    def _create_schema(self):
        """Create lineage_events table if not exists."""
        # DuckDB has no implicit rowid autoincrement: event_id comes from a sequence.
        # event_id ordering defines the hash chain, so it must be monotonic.
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS lineage_event_id_seq START 1")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS lineage_events (
                event_id INTEGER PRIMARY KEY DEFAULT nextval('lineage_event_id_seq'),
                run_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                event_type TEXT NOT NULL,
                component TEXT NOT NULL,
                dataset TEXT NOT NULL,
                partition TEXT NOT NULL,
                metadata JSON NOT NULL,
                parent_run_id TEXT,
                content_hash TEXT NOT NULL,
                prev_hash TEXT
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_lineage_run ON lineage_events(run_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_lineage_dataset ON lineage_events(dataset, partition)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_lineage_type ON lineage_events(event_type)")

    def append(
        self,
        run_id: RunID,
        event_type: LineageEventType,
        component: str,
        dataset: str,
        partition: str,
        metadata: Dict[str, Any],
        parent_run_id: Optional[RunID] = None,
    ) -> LineageEvent:
        """
        Append event to lineage graph (P7: append-only).

        Computes content_hash as SHA-256(prev_hash || event_data) to form tamper-evident chain.

        Args:
            run_id: Which run generated this event
            event_type: PROFILE, IMPUTATION, RULE_VIOLATION, etc.
            component: Which component (profiler, repair, entity, etc.)
            dataset: Dataset name
            partition: Partition identifier (date, batch ID, etc.)
            metadata: Event-specific metadata (method, params, results)
            parent_run_id: If this run refines a previous run

        Returns:
            LineageEvent with computed content_hash

        Raises:
            RuntimeError: If append fails (should never happen unless DB corrupted)
        """
        # Get hash of previous event to form chain
        result = self.conn.execute("SELECT content_hash FROM lineage_events ORDER BY event_id DESC LIMIT 1").fetchone()
        prev_hash = result[0] if result else None

        # Compute hash for this event
        event_data = {
            "run_id": str(run_id),
            "event_type": event_type.value,
            "component": component,
            "dataset": dataset,
            "partition": partition,
            "metadata": metadata,
            "parent_run_id": str(parent_run_id) if parent_run_id else None,
        }
        content_hash = _compute_content_hash(prev_hash, event_data)

        # Insert (append-only, no updates or deletes)
        timestamp = datetime.now(timezone.utc)
        self.conn.execute(
            """
            INSERT INTO lineage_events
            (run_id, timestamp, event_type, component, dataset, partition, metadata, parent_run_id, content_hash, prev_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                str(run_id),
                timestamp,
                event_type.value,
                component,
                dataset,
                partition,
                json.dumps(metadata, sort_keys=True, default=_canonical_default),
                str(parent_run_id) if parent_run_id else None,
                content_hash,
                prev_hash,
            ],
        )

        return LineageEvent(
            run_id=run_id,
            timestamp=timestamp,
            event_type=event_type,
            component=component,
            dataset=dataset,
            partition=partition,
            metadata=metadata,
            parent_run_id=parent_run_id,
            content_hash=content_hash,
        )

    def query(
        self,
        run_id: Optional[RunID] = None,
        event_type: Optional[LineageEventType] = None,
        dataset: Optional[str] = None,
        partition: Optional[str] = None,
        component: Optional[str] = None,
    ) -> List[LineageEvent]:
        """
        Query lineage graph.

        Args:
            run_id: Filter by run
            event_type: Filter by event type
            dataset: Filter by dataset
            partition: Filter by partition
            component: Filter by component

        Returns:
            List of LineageEvent, ordered by timestamp
        """
        where_clauses = []
        params = []

        if run_id:
            where_clauses.append("run_id = ?")
            params.append(str(run_id))
        if event_type:
            where_clauses.append("event_type = ?")
            params.append(event_type.value)
        if dataset:
            where_clauses.append("dataset = ?")
            params.append(dataset)
        if partition:
            where_clauses.append("partition = ?")
            params.append(partition)
        if component:
            where_clauses.append("component = ?")
            params.append(component)

        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        sql = f"SELECT run_id, timestamp, event_type, component, dataset, partition, metadata, parent_run_id, content_hash FROM lineage_events WHERE {where_sql} ORDER BY timestamp"

        rows = self.conn.execute(sql, params).fetchall()

        events = []
        for row in rows:
            events.append(
                LineageEvent(
                    run_id=RunID(value=row[0]),
                    timestamp=row[1],
                    event_type=LineageEventType(row[2]),
                    component=row[3],
                    dataset=row[4],
                    partition=row[5],
                    metadata=json.loads(row[6]),
                    parent_run_id=RunID(value=row[7]) if row[7] else None,
                    content_hash=row[8],
                )
            )
        return events

    def verify_chain(self) -> bool:
        """
        Verify hash chain integrity (tamper detection).

        Recomputes content_hash for every event and checks against stored hash.

        Returns:
            True if chain is intact, False if tampered

        Example:
            >>> graph = LineageGraph()
            >>> graph.append(...)
            >>> graph.verify_chain()
            True
        """
        rows = self.conn.execute(
            "SELECT event_id, run_id, event_type, component, dataset, partition, metadata, parent_run_id, content_hash, prev_hash FROM lineage_events ORDER BY event_id"
        ).fetchall()

        prev_hash = None
        for row in rows:
            event_data = {
                "run_id": row[1],
                "event_type": row[2],
                "component": row[3],
                "dataset": row[4],
                "partition": row[5],
                "metadata": json.loads(row[6]),
                "parent_run_id": row[7],
            }
            expected_hash = _compute_content_hash(prev_hash, event_data)
            actual_hash = row[8]

            if expected_hash != actual_hash:
                return False  # Chain broken

            prev_hash = actual_hash

        return True

    def close(self):
        """Close database connection."""
        self.conn.close()
