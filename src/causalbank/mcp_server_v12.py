"""Pinned legacy MCP 2025-11-25 local-stdio adapter for the V12 service."""
import asyncio
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

import anyio
import jsonschema
from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from mcp.server import session as sdk_session
from mcp.shared.exceptions import McpError

from .artifacts_v12 import ROOT
from .cli_v12 import state_root
from .operation_service_v12 import CONTRACT, REQUEST_SCHEMA, RESPONSE_SCHEMA
from .runtime_v12 import IMPLEMENTED, Runtime

_MAPPING = json.loads((CONTRACT / "mcp-contract.json").read_text())
if _MAPPING["protocol_version"] != "2025-11-25":
    raise RuntimeError("Unreviewed MCP protocol revision")
TOOL_TO_OPERATION = {x["mcp_tool"]: x["id"] for x in _MAPPING["tool_mapping"]}
AVAILABLE = {tool: op for tool, op in TOOL_TO_OPERATION.items() if op in IMPLEMENTED}
READABLE_ROLES = {"report", "evidence_summary", "canonical_response"}


def build_server(service):
    # SDK 1.27.0 has no per-server supported-version setting. Restrict this
    # dedicated process's negotiation table; do not claim older untested eras.
    sdk_session.SUPPORTED_PROTOCOL_VERSIONS = ["2025-11-25"]
    server = Server("causalbank-local-v12", version="0.4.0")

    @server.list_tools()
    async def list_tools():
        return [types.Tool(name=tool, title=op,
            description=f"Local reference {op}: {IMPLEMENTED[op]}. Scientific status is inside the canonical response.",
            inputSchema=REQUEST_SCHEMA, outputSchema=RESPONSE_SCHEMA)
            for tool, op in AVAILABLE.items()]

    @server.call_tool()
    async def call_tool(name, arguments):
        op = AVAILABLE.get(name)
        if op is None:
            return types.CallToolResult(content=[types.TextContent(type="text", text="Unknown or unavailable causal operation")],
                                        isError=True)
        if arguments.get("operation") != op:
            return types.CallToolResult(content=[types.TextContent(type="text", text="Tool and canonical operation disagree")],
                                        isError=True)
        try:
            response = await anyio.to_thread.run_sync(service.invoke, arguments)
            jsonschema.validate(response, RESPONSE_SCHEMA)
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=json.dumps(response, sort_keys=True, allow_nan=False))],
                structuredContent=response,
                isError=response["status"] in {"failed", "rejected"})
        except (ValueError, jsonschema.ValidationError, KeyError, TypeError) as exc:
            return types.CallToolResult(content=[types.TextContent(type="text", text=f"Invalid local causal request: {str(exc)[:300]}")],
                                        isError=True)
        except (FileNotFoundError, PermissionError):
            return types.CallToolResult(content=[types.TextContent(type="text", text="Required authorized artifact unavailable")],
                                        isError=True)
        except Exception as exc:
            print(f"Causal operation failed: {type(exc).__name__}", file=sys.stderr)
            return types.CallToolResult(content=[types.TextContent(type="text", text="Local causal operation failed")],
                                        isError=True)

    # The SDK decorator turns handler exceptions into tool execution errors.
    # Unknown tool names belong to the protocol-error layer in the pinned spec.
    # Guard outside that decorator while leaving its schema/error handling intact.
    decorated_call = server.request_handlers[types.CallToolRequest]

    async def guarded_call(req):
        if req.params.name not in AVAILABLE:
            raise McpError(types.ErrorData(code=types.INVALID_PARAMS, message="Unknown causal tool"))
        return await decorated_call(req)

    server.request_handlers[types.CallToolRequest] = guarded_call

    @server.list_resources()
    async def list_resources():
        return [types.Resource(name=r["artifact_id"], title=r["role"],
            uri=f"causal-artifact://{r['artifact_id']}", mimeType="application/json", size=r["bytes"])
            for r in service.store.list_refs() if r["role"] in READABLE_ROLES and r["bytes"] <= 65536]

    @server.read_resource()
    async def read_resource(uri):
        parsed = urlsplit(str(uri))
        if parsed.scheme != "causal-artifact" or not parsed.netloc or parsed.path or parsed.query or parsed.fragment:
            raise ValueError("Only opaque local causal artifact resource IDs are supported")
        ref = service.store.reference(parsed.netloc)
        if ref["role"] not in READABLE_ROLES or ref["bytes"] > 65536:
            raise ValueError("Raw or large artifacts are not MCP resources")
        return json.dumps(service.store.get(ref, limit=65536), sort_keys=True, allow_nan=False)

    return server


async def main():
    service = Runtime(state_root())
    server = build_server(service)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
