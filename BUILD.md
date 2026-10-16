# Namu Android prebuilt libraries

## ImGui 90/92

Requires JDK 17, Android SDK 35, NDK 27.3.13750724 and CMake 3.22.1.

```sh
git submodule update --init --recursive --depth 1 misc/imgui_moulberry90/source misc/imgui_moulberry92/source
./gradlew --no-configuration-cache :imgui_moulberry90:assembleRelease :imgui_moulberry92:assembleRelease
python3 tools/package-imgui.py
```

Copy `build/outputs/imgui/native/<ABI>/*.so` into the game folder's `native/<ABI>/` directory. Both `arm64-v8a` and `x86_64` are included. Distribute the accompanying licenses and build-info.json with the files.

These libraries are external game files; the launcher APK does not need to contain them. The launcher stages them in private storage before loading.

Sources: [ImGui 90](https://github.com/Moulberry/imgui-java/tree/c80552861d5de1c929dbe3210cba8b72792e4471), [ImGui 92](https://github.com/Moulberry/imgui-java/tree/4a2813430cc2bc64ba2106289d0c8606e656f32d).

Build scripts and license notices originated in [NamuLauncher/Amethyst-Android](https://github.com/NamuLauncher/Amethyst-Android/tree/75e795293825651f860422be1b42a14757a5ebcf). JNI generation and symbol isolation are unchanged. The known ImGui 92 font-buffer lifetime issue is not fixed by this move.

See [HISTORY.md](HISTORY.md) for the extracted repository history and [NOTICE](NOTICE) for license provenance.

## Skiko 0.9.22.2

Requires JDK 17, Python 3, Git, nm, Android SDK 31 and NDK 27.3.13750724. Set `ANDROID_HOME` to your SDK directory.

```sh
git clone https://github.com/JetBrains/skiko.git skiko-upstream
git -C skiko-upstream checkout 2f621572270c28052549ff4678b762c3fea09fa5
python3 scripts/skiko/patch-linker.py skiko-upstream
export ANDROID_NDK_HOME="$ANDROID_HOME/ndk/27.3.13750724"
bash skiko-upstream/gradlew -p skiko-upstream/skiko \
  linkJvmBindingsAndroidArm64 linkJvmBindingsAndroidX64 \
  -Pskiko.android.enabled=true -Pskiko.awt.enabled=false \
  -Pdeploy.version=0.9.22.2 --no-daemon
mkdir -p build/outputs
NATIVE_ARCH=arm64 NATIVE_ABI=arm64-v8a python3 scripts/skiko/package-native.py skiko-upstream
mv skiko-native build/outputs/skiko-arm64-v8a
NATIVE_ARCH=x64 NATIVE_ABI=x86_64 python3 scripts/skiko/package-native.py skiko-upstream
mv skiko-native build/outputs/skiko-x86_64
```

Create `build/outputs` before packaging. Apply the patch once to a clean checkout. Each output contains `native/<ABI>/libskiko-linux-<arch>.so`, licenses, compatibility source and build information. Distribute these materials together. The filename matches the game mod's AWT loader; the binary is built for Android.

See [Skiko compatibility notes](scripts/skiko/README.md) for the linker and system-theme bridge changes. The launcher APK does not bundle Skiko.
