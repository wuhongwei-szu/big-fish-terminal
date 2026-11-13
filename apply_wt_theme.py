#!/usr/bin/env python3
"""Portable version of the installed theme's apply_wt_theme.py. Python 3.10+."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
START = "# >>> bigfish terminal >>>"
END = "# <<< bigfish terminal <<<"

def read_settings(path):
    # JSONC comments and trailing commas are supported; keep strings intact.
    text = path.read_text(encoding="utf-8-sig")
    tokens = re.compile(r'"(?:\\.|[^"\\])*"|//[^\r\n]*|/\*.*?\*/', re.S)
    text = tokens.sub(lambda m: m.group() if m.group().startswith('"') else ' ', text)
    tokens = re.compile(r'"(?:\\.|[^"\\])*"|,(\s*[}\]])', re.S)
    text = tokens.sub(lambda m: m.group(1) if m.group(1) else m.group(), text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("settings must contain a JSON object")
    return data

def backup(path):
    if path.exists():
        target = path.with_name(path.name + ".bak-bigfish-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
        shutil.copy2(path, target)
        print("backup:", target)

def read_profile(path):
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
    return raw.decode(encoding).replace("\r\n", "\n")

def write(path, text):
    if path.exists() and read_profile(path) == text:
        print("unchanged:", path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8-sig" if path.suffix==".ps1" else "utf-8", dir=path.parent, delete=False) as f:
        f.write(text)
        temp = Path(f.name)
    temp.replace(path)

def install(args):
    settings = Path(args.settings).expanduser().resolve()
    targets = [Path(p).expanduser().resolve() for p in args.profile]
    if len(set(targets)) != len(targets):
        raise ValueError("duplicate profile paths")
    for target in [settings, *targets]:
        if target.is_relative_to(ROOT):
            raise ValueError("configuration target must be outside the theme folder: " + str(target))
    if settings in targets or any(p.suffix.lower() != ".ps1" for p in targets):
        raise ValueError("profiles must be separate .ps1 files")
    data = read_settings(settings)
    scheme = json.loads((ROOT / "scheme.json").read_text(encoding="utf-8"))
    background = Path(args.background).expanduser().resolve() if args.background else ROOT / "assets" / "harbor-night.png"
    if not background.is_file():
        raise FileNotFoundError(background)
    icon = Path(args.icon).expanduser().resolve() if args.icon else None
    if icon and not icon.is_file():
        raise FileNotFoundError(icon)
    starship = Path(args.starship).expanduser().resolve() if args.starship else None
    if starship and not starship.is_file():
        raise FileNotFoundError(starship)
    data["schemes"] = [s for s in data.get("schemes", []) if s.get("name") != scheme["name"]] + [scheme]
    defaults = data.setdefault("profiles", {}).setdefault("defaults", {})
    defaults.update({"colorScheme": scheme["name"], "font": {**defaults.get("font", {}), "face": "Cascadia Code", "size": 11},
        "backgroundImage": str(background), "backgroundImageOpacity": 1.0, "backgroundImageAlignment": "bottomRight",
        "backgroundImageStretchMode": "uniformToFill", "cursorShape": "filledBox"})
    if icon:
        defaults["icon"] = str(icon)
    prepared = []
    for profile_arg in args.profile:
        profile = Path(profile_arg).expanduser().resolve()
        old = read_profile(profile) if profile.exists() else ""
        if (START in old) != (END in old):
            raise ValueError("incomplete Big Fish block in " + str(profile))
        command = ". '" + str(ROOT / "prompt.ps1").replace("'", "''") + "'"
        if starship:
            command += " -StarshipPath '" + str(starship).replace("'", "''") + "'"
        block = START + "\n" + command + "\n" + END
        if START in old:
            result = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, old, flags=re.S)
        else:
            result = old.rstrip() + "\n\n" + block + "\n"
        prepared.append((profile, result))
    # Validate every input before changing files. Existing unrelated values remain.
    write(settings, json.dumps(data, ensure_ascii=False, indent=4) + "\n")
    for profile, text in prepared:
        write(profile, text)
    print("settings:", settings)
    print("background:", background)
    print("Open a new PowerShell tab to load the prompt.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("settings", help="Windows Terminal settings.json path")
    parser.add_argument("--background", help="Your own licensed background image")
    parser.add_argument("--icon", help="Your own licensed icon image")
    parser.add_argument("--profile", action="append", default=[], help="PowerShell profile path; repeat for both editions")
    parser.add_argument("--starship", help="Optional absolute path to an existing Starship executable")
    install(parser.parse_args())

if __name__ == "__main__":
    main()
