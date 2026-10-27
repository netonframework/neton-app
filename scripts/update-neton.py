"""Find the newest shared 1.0.0 beta/rc in Central; never use dynamic Gradle versions."""
import argparse
from pathlib import Path
import re
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://repo.maven.apache.org/maven2/com/netonstream"
PATTERN = re.compile(r"1\.0\.0-(beta|rc)([1-9][0-9]*)", re.I)


def version_key(version):
    match = PATTERN.fullmatch(version)
    if not match:
        raise ValueError(f"Unsupported preview version: {version}")
    return (1 if match[1].lower() == "rc" else 0, int(match[2]))


def latest_shared(framework, processor):
    candidates = {v for v in framework if PATTERN.fullmatch(v)} & set(processor)
    if not candidates:
        raise ValueError("No shared 1.0.0 beta/rc for neton and neton-ksp")
    return max(candidates, key=version_key)


def versions(artifact):
    with urlopen(f"{BASE}/{artifact}/maven-metadata.xml", timeout=30) as response:
        return [v.text for v in ET.fromstring(response.read()).findall("./versioning/versions/version")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Update the pin; otherwise check only")
    args = parser.parse_args()
    path = ROOT / "gradle.properties"
    content = path.read_text()
    pins = re.findall(r"^netonVersion=(\S+)$", content, re.M)
    if len(pins) != 1:
        raise ValueError("Expected exactly one netonVersion property")
    latest = latest_shared(versions("neton"), versions("neton-ksp"))
    if version_key(latest) < version_key(pins[0]):
        raise ValueError("Central metadata is behind the local pin; refusing downgrade")
    print(f"Current: {pins[0]}; latest shared preview: {latest}")
    if args.write and latest != pins[0]:
        path.write_text(re.sub(r"^netonVersion=\S+$", f"netonVersion={latest}", content, flags=re.M))


if __name__ == "__main__":
    main()
