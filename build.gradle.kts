plugins {
    kotlin("multiplatform") version "2.4.20"
    kotlin("plugin.serialization") version "2.4.20"
    id("com.google.devtools.ksp") version "2.3.10"
}

// Kotlin 版本下限 2.4.20：低于它（包括 2.4.20 的 Beta / RC）直接拒绝编译。
// Neton 各仓走同一条 Kotlin 线 —— 混用时 K/N klib 与 KSP 产物会以很难看懂的方式失败。
run {
    val required = KotlinVersion(2, 4, 20)
    val actual = org.jetbrains.kotlin.gradle.plugin.getKotlinPluginVersion(logger)
    val parts = actual.substringBefore('-').split('.').map { it.toIntOrNull() ?: 0 } + listOf(0, 0, 0)
    val parsed = KotlinVersion(parts[0], parts[1], parts[2])
    require(parsed > required || (parsed == required && '-' !in actual)) {
        "Kotlin $actual is below the required minimum $required. Upgrade the Kotlin Gradle plugin."
    }
}

repositories {
    mavenCentral()
}

val netonVersion = "1.0.0-beta7"

kotlin {
    listOf(macosArm64(), macosX64(), linuxX64(), linuxArm64(), mingwX64()).forEach { target ->
        target.binaries.executable { entryPoint = "main" }
    }

    sourceSets {
        commonMain.dependencies {
            // One versioned line: core + logging + http + routing, plus version constraints
            // for every other neton-* module, so extra modules are added without a version.
            implementation("com.netonstream:neton:$netonVersion")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.11.0")
        }
    }
}

// KSP generates routes for @Controller classes. Generation runs once, on the host's own
// target, and the output is shared with every target because it is identical for all of them.
val hostTarget = with(System.getProperty("os.name").lowercase() to System.getProperty("os.arch").lowercase()) {
    when {
        first.contains("mac") && (second.contains("aarch64") || second.contains("arm")) -> "macosArm64"
        first.contains("mac") -> "macosX64"
        first.contains("linux") && (second.contains("aarch64") || second.contains("arm")) -> "linuxArm64"
        first.contains("linux") -> "linuxX64"
        first.contains("windows") -> "mingwX64"
        else -> error("Unsupported host: $first/$second")
    }
}
val hostTargetCapital = hostTarget.replaceFirstChar { it.uppercase() }

dependencies {
    add("ksp$hostTargetCapital", "com.netonstream:neton-ksp:$netonVersion")
}

kotlin.sourceSets.named("commonMain") {
    kotlin.srcDir("build/generated/ksp/$hostTarget/${hostTarget}Main/kotlin")
}
afterEvaluate {
    kotlin.sourceSets.findByName("${hostTarget}Main")?.let { ss ->
        val filtered = ss.kotlin.srcDirs.filter { !it.path.contains("generated/ksp") }
        if (filtered.size < ss.kotlin.srcDirs.size) ss.kotlin.setSrcDirs(filtered)
    }
}
tasks.matching { it.name.matches(Regex("compileKotlin(MacosArm64|MacosX64|LinuxX64|LinuxArm64|MingwX64)")) }.configureEach {
    dependsOn("kspKotlin$hostTargetCapital")
}
// The generated sources are added to commonMain, so the metadata compilation reads them too
// and `./gradlew build` fails on an unresolved GeneratedInitializer without this.
tasks.matching { it.name == "compileCommonMainKotlinMetadata" }.configureEach {
    dependsOn("kspKotlin$hostTargetCapital")
}

// `./gradlew run` builds and starts the executable for whatever machine you are on.
tasks.register("run") {
    group = "application"
    description = "Build and run neton-app for the current host."
    dependsOn("runDebugExecutable$hostTargetCapital")
}
