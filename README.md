# neton-app

The smallest useful [Neton](https://github.com/netonframework/neton) application: one controller,
one HTML page, one JSON endpoint. Clone it, run it, then make it yours.

## Run

```bash
git clone https://github.com/netonframework/neton-app.git
cd neton-app
./gradlew run
```

Then open <http://localhost:8080/> — you should see **Welcome to Neton**.
`http://localhost:8080/api/hello` returns JSON.

`./gradlew run` builds a native binary for the machine you are on (macOS ARM64/x64,
Linux x64/ARM64, Windows x64) and starts it. There is no JVM at runtime.

Requirements: JDK 17+ for Gradle, and Xcode command line tools on macOS. First build downloads
the Kotlin/Native toolchain (a few minutes); later builds take seconds.

## What is in here

```
build.gradle.kts                          one versioned dependency: com.netonstream:neton
config/application.conf                   port, log level
src/commonMain/kotlin/Main.kt             Neton.run { http; routing; modules(GeneratedInitializer) }
src/commonMain/kotlin/controller/         WelcomeController: GET /  and  GET /api/hello
```

`com.netonstream:neton` pulls in `neton-core`, `neton-logging`, `neton-http` and
`neton-routing`, and pins every other Neton module to the same release. Add more without a
version:

```kotlin
implementation("com.netonstream:neton-database")
implementation("com.netonstream:neton-redis")
```

Routes come from `@Controller` classes; KSP collects them into `GeneratedInitializer`, which
`Main.kt` passes to `modules(...)`. Add a controller, rebuild, done.

## Following Neton previews

`gradle.properties` pins `netonVersion` for both the framework and KSP. This sample
tracks published `1.0.0-betaN` / `1.0.0-rcN` builds, not unpublished source snapshots
or a dynamic `+` dependency. Check manually with `python3 scripts/update-neton.py`;
add `--write` to update the pin, then build and test before committing.

The preview workflow checks Central every six hours (and on manual dispatch), verifies
the same candidate on macOS ARM64 and Linux x64, and opens an upgrade PR only when both
release binaries link. It does not auto-merge or claim runtime/cross-platform acceptance.
It becomes active after this workflow reaches the default branch and GitHub Actions is
enabled. Enable “Allow GitHub Actions to create and approve pull requests” in repository
settings for PR creation; no external dependency bot is needed. Failed builds remain
visible as failed workflow runs, with the current pin unchanged on the default branch.
Final `1.0.0` adoption is a deliberate policy change, not an automatic channel switch.

## Next

- Guide: <https://netonframework.github.io/guide/>
- Routing and controllers: <https://netonframework.github.io/guide/routing>
- Database, cache, Redis, events: see the guide sidebar

## 中文

本项目跟踪 Maven Central 已发布的 Neton 1.0 测试版，框架和 KSP 使用同一个明确版本。
工作流进入默认分支并启用 Actions 后，每六小时检查一次；macOS ARM64 与 Linux x64
发布构建均通过才创建升级 PR，不自动合并。需要在仓库设置允许 Actions 创建 PR。
构建通过不代表运行验收或正式版门禁通过；正式版切换需单独决定。

最小可运行的 Neton 应用：一个控制器、一个 HTML 页面、一个 JSON 接口。

```bash
git clone https://github.com/netonframework/neton-app.git
cd neton-app
./gradlew run
```

打开 <http://localhost:8080/> 看到 **Welcome to Neton** 即成功。`./gradlew run` 会为当前机器编译
原生二进制并启动，运行时没有 JVM。首次构建要下载 Kotlin/Native 工具链，之后只需几秒。

依赖只有一行 `com.netonstream:neton`，它带齐最小服务所需的四个模块并对齐其余模块的版本，
追加 `neton-database` 之类不用写版本。路由来自 `@Controller`，KSP 汇聚成 `GeneratedInitializer`，
`Main.kt` 里 `modules(GeneratedInitializer)` 传入即可。文档：<https://netonframework.github.io/zh-hans/guide/>
