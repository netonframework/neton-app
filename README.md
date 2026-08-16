# neton-start

The smallest useful [Neton](https://github.com/netonframework/neton) application: one controller,
one HTML page, one JSON endpoint. Clone it, run it, then make it yours.

## Run

```bash
git clone https://github.com/netonframework/neton-start.git
cd neton-start
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

## Next

- Guide: <https://netonframework.github.io/guide/>
- Routing and controllers: <https://netonframework.github.io/guide/routing>
- Database, cache, Redis, events: see the guide sidebar

## 中文

最小可运行的 Neton 应用：一个控制器、一个 HTML 页面、一个 JSON 接口。

```bash
git clone https://github.com/netonframework/neton-start.git
cd neton-start
./gradlew run
```

打开 <http://localhost:8080/> 看到 **Welcome to Neton** 即成功。`./gradlew run` 会为当前机器编译
原生二进制并启动，运行时没有 JVM。首次构建要下载 Kotlin/Native 工具链，之后只需几秒。

依赖只有一行 `com.netonstream:neton`，它带齐最小服务所需的四个模块并对齐其余模块的版本，
追加 `neton-database` 之类不用写版本。路由来自 `@Controller`，KSP 汇聚成 `GeneratedInitializer`，
`Main.kt` 里 `modules(GeneratedInitializer)` 传入即可。文档：<https://netonframework.github.io/zh-hans/guide/>
