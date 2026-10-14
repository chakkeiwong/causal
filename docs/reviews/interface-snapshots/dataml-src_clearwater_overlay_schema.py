"""
Overlay storage schema.

Chapter 12 principle P1: never write source. Corrections live in a separate
table and are composed onto the source at read time.

Chapter 12 principle P2: no correction without a resolvable assumption_id.
Phase 1 enforces this with a real foreign key against an assumptions table.
The full registry (immutability, expiry, method compatibility) lands in Phase 3,
but the referential constraint exists from the start — a TEXT NOT NULL column
would let unresolvable assumptions in, which is exactly what P2 forbids.
"""

CREATE_SEQUENCES = [
    "CREATE SEQUENCE IF NOT EXISTS correction_id_seq START 1",
]

# Minimal assumptions table for Phase 1. Phase 3 replaces this with the full
# registry (see ticket 3.1) but keeps the same primary key so the FK survives.
CREATE_ASSUMPTIONS = """
CREATE TABLE IF NOT EXISTS assumptions (
    assumption_id        TEXT PRIMARY KEY,
    description          TEXT NOT NULL,
    math_statement       TEXT NOT NULL,
    testable_implication TEXT NOT NULL,
    approved_by          TEXT NOT NULL,
    approved_at          TIMESTAMP NOT NULL,
    expires_at           TIMESTAMP
)
"""

# P2 is enforced by `assumption_id TEXT NOT NULL REFERENCES assumptions`.
# P6 (approval precedes effect) is enforced by the reader, which filters on
# approved_at for production purposes; the CHECK below only guarantees that an
# approver and a timestamp travel together.
CREATE_CORRECTIONS = """
CREATE TABLE IF NOT EXISTS corrections (
    correction_id    INTEGER PRIMARY KEY DEFAULT nextval('correction_id_seq'),
    run_id           TEXT NOT NULL,
    dataset          TEXT NOT NULL,
    partition        TEXT NOT NULL,
    row_key          TEXT NOT NULL,
    column_name      TEXT NOT NULL,
    original_value   TEXT,
    corrected_value  TEXT,
    draw_index       INTEGER NOT NULL DEFAULT 0,
    transform_id     TEXT NOT NULL,
    method           TEXT NOT NULL,
    assumption_id    TEXT NOT NULL REFERENCES assumptions(assumption_id),
    uncertainty      DOUBLE,
    confidence       DOUBLE NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    purpose          TEXT NOT NULL,
    approver         TEXT,
    approved_at      TIMESTAMP,
    created_at       TIMESTAMP NOT NULL,
    CHECK ((approver IS NULL) = (approved_at IS NULL))
)
"""

CREATE_INDEXES = [
    # Overlay join: the read path always filters on this tuple.
    "CREATE INDEX IF NOT EXISTS idx_corr_overlay "
    "ON corrections(dataset, partition, row_key, column_name)",
    # P2 audit query: "show me every cell corrected under assumption X".
    "CREATE INDEX IF NOT EXISTS idx_corr_assumption ON corrections(assumption_id)",
    "CREATE INDEX IF NOT EXISTS idx_corr_run ON corrections(run_id)",
    # Per-draw reads select one draw at a time.
    "CREATE INDEX IF NOT EXISTS idx_corr_draw ON corrections(dataset, partition, draw_index)",
]


def create_overlay_schema(conn) -> None:
    """Create sequences, tables and indexes for overlay storage."""
    for stmt in CREATE_SEQUENCES:
        conn.execute(stmt)
    conn.execute(CREATE_ASSUMPTIONS)
    conn.execute(CREATE_CORRECTIONS)
    for stmt in CREATE_INDEXES:
        conn.execute(stmt)
