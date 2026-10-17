"""Bounded offline fixtures; not a native WHMCS or licensed-panel certification."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
tests = ["coexistence", "cpanel_tenant_isolation", "cpanel_ssh_security", "plesk_scope", "plesk_report",
         "plesk_transport", "plesk_native", "plesk_health", "plesk_services"]
for name in tests:
    print("Running " + name, flush=True)
    subprocess.run(["php", str(ROOT / "tests" / (name + ".php"))], cwd=ROOT, check=True, timeout=120)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True, timeout=180)
