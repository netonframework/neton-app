"""Run the real release binary twice, checking HTTP and graceful shutdown."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import tempfile
import time
import urllib.request

def require(value, message):
    if not value:
        raise RuntimeError(message)

def port_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False

def validate_hello(payload, expected_version=None):
    require(payload.get("code") == 0, "Invalid response envelope")
    data = payload.get("data", {})
    require(data.get("framework") == "Neton" and data.get("message") == "Welcome to Neton", "Invalid welcome payload")
    require(bool(data.get("version")), "Missing framework version")
    if expected_version is not None:
        require(data["version"] == expected_version, "Running framework version differs from candidate")

def health(port, candidate):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/hello", timeout=5) as response:
        require(response.status == 200, "HTTP health failed")
        validate_hello(json.load(response), candidate)

def validate_shutdown(code, listening):
    require(code == 0, f"Nonzero shutdown: {code}")
    require(not listening, "HTTP port still listening after shutdown")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
    binary = args.binary.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    evidence = {"passed": False, "candidate": args.candidate,
                "binarySha256": hashlib.sha256(binary.read_bytes()).hexdigest(), "cycles": []}
    windows = os.name == "nt"
    process = None
    try:
        with tempfile.TemporaryDirectory(prefix="neton-app-smoke-") as directory:
            work = Path(directory)
            (work / "config").mkdir()
            with socket.socket() as reservation:
                reservation.bind(("127.0.0.1", 0))
                port = reservation.getsockname()[1]
            (work / "config/application.conf").write_text(f'[server]\nhost = "127.0.0.1"\nport = {port}\n')
            env = {k: v for k, v in os.environ.items() if not k.startswith("NETON_")}
            for cycle in (1, 2):
                require(not port_open(port), "Port already occupied")
                with (output / f"cycle-{cycle}.log").open("w") as log:
                    process = subprocess.Popen([str(binary)], cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT,
                        start_new_session=not windows, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if windows else 0)
                    deadline = time.monotonic() + 60
                    while True:
                        require(process.poll() is None, "Process exited before readiness")
                        try:
                            health(port, args.candidate)
                            break
                        except (OSError, ValueError, RuntimeError):
                            require(time.monotonic() < deadline, "Readiness timeout")
                            time.sleep(0.25)
                    started = time.monotonic()
                    while time.monotonic() - started < 60:
                        require(process.poll() is None, "Process exited during health hold")
                        health(port, args.candidate)
                        time.sleep(1)
                    process.send_signal(signal.CTRL_BREAK_EVENT if windows else signal.SIGTERM)
                    code = process.wait(timeout=30)
                    validate_shutdown(code, port_open(port))
                    evidence["cycles"].append({"cycle": cycle, "healthySeconds": time.monotonic() - started,
                        "exitCode": code, "portClosed": True, "signal": "CTRL_BREAK_EVENT" if windows else "SIGTERM"})
                    process = None
            evidence["passed"] = True
    finally:
        if process is not None and process.poll() is None:
            process.kill()  # Cleanup only, never accepted as graceful shutdown.
            process.wait(timeout=10)
        (output / "evidence.json").write_text(json.dumps(evidence, indent=2))

if __name__ == "__main__":
    main()
