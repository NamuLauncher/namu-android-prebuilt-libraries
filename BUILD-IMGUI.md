# Moulberry ImGui natives

Requires JDK 17, Android SDK 35, NDK 27.3.13750724 and CMake 3.22.1.

```sh
git submodule update --init --recursive --depth 1 misc/imgui_moulberry90/source misc/imgui_moulberry92/source
./gradlew -PimguiOnly=true --no-configuration-cache :imgui_moulberry90:assembleRelease :imgui_moulberry92:assembleRelease
python3 tools/package-imgui.py
```

Copy `build/outputs/imgui/native/<ABI>/*.so` into the game folder's `native/<ABI>/` directory. Both `arm64-v8a` and `x86_64` are included. Distribute the accompanying licenses and build-info.json with the files.

These libraries are external game files; the launcher APK does not need to contain them. The launcher stages them in private storage before loading.

Sources: [ImGui 90](https://github.com/Moulberry/imgui-java/tree/c80552861d5de1c929dbe3210cba8b72792e4471), [ImGui 92](https://github.com/Moulberry/imgui-java/tree/4a2813430cc2bc64ba2106289d0c8606e656f32d).

Build scripts and license notices were moved from [AlphaBs/Amethyst-Android](https://github.com/NamuLauncher/Amethyst-Android/tree/75e795293825651f860422be1b42a14757a5ebcf). JNI generation and symbol isolation are unchanged. The known ImGui 92 font-buffer lifetime issue is not fixed by this move.
