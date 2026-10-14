import json
from pathlib import Path
from causalbank.runtime_v12 import Runtime

request = json.loads(Path("request.json").read_text())
runtime = Runtime(Path.cwd() / ".runtime" / "offer-client")
response = runtime.invoke(request)
Path("response.json").write_text(json.dumps(response, indent=2) + "\n")
