#!/usr/bin/env python3
"""모드팩 native 폴더에 배포할 ImGui 라이브러리와 출처를 구성한다."""

import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output = root / "build/outputs/imgui"
if output.exists():
    shutil.rmtree(output)
output.mkdir(parents=True)

abis = {"arm64-v8a": 183, "x86_64": 62}
manifest = {
    "repository": "https://github.com/AlphaBs/amethyst-prebuilt-libraries",
    "commit": subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
    ).strip(),
    "sources": {},
    "files": {},
}

for version in [90, 92]:
    module = root / "misc" / f"imgui_moulberry{version}"
    manifest["sources"][str(version)] = subprocess.check_output(
        ["git", "-C", str(module / "source"), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    aar = module / "build/outputs/aar" / f"imgui_moulberry{version}-release.aar"
    library_name = f"libimgui-moulberry{version}.so"
    with zipfile.ZipFile(aar) as archive:
        for abi, machine in abis.items():
            data = archive.read(f"jni/{abi}/{library_name}")
            if data[:6] != b"\x7fELF\x02\x01":
                raise SystemExit(f"64비트 little-endian ELF가 아님: {abi}, {library_name}")
            if int.from_bytes(data[18:20], "little") != machine:
                raise SystemExit(f"잘못된 ELF 아키텍처: {abi}, {library_name}")
            destination = output / "native" / abi / library_name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            symbols = subprocess.check_output(
                ["nm", "-D", "--defined-only", str(destination)],
                text=True,
            )
            exported = {
                line.split()[-1]
                for line in symbols.splitlines()
                if line.strip()
            }
            required_symbol = f"Java_imgui_moulberry{version}_ImGui_nInitJni"
            if required_symbol not in exported:
                raise SystemExit(f"JNI 초기화 심볼이 없음: {abi}, {library_name}")
            if "GImGui" in exported or any(name.startswith("_ZN5ImGui") for name in exported):
                raise SystemExit(f"ImGui 전역 C++ 심볼이 노출됨: {abi}, {library_name}")
            other_version = 92 if version == 90 else 90
            if any(name.startswith(f"Java_imgui_moulberry{other_version}_") for name in exported):
                raise SystemExit(f"다른 버전의 JNI가 섞임: {abi}, {library_name}")
            relative = destination.relative_to(output).as_posix()
            manifest["files"][relative] = {
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
            print(f"외부 네이티브 ABI·JNI·심볼 분리 확인: {relative}")
    shutil.copytree(
        module / "src/main/assets/licenses",
        output / "licenses" / f"imgui-moulberry{version}",
    )

(output / "build-info.json").write_text(json.dumps(manifest, indent=2) + "\n")
shutil.copy2(root / "BUILD-IMGUI.md", output / "BUILD-IMGUI.md")
print(f"배포 폴더: {output}")
