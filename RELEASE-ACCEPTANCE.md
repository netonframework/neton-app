# Public reference application acceptance

This repository is a minimal consumer, not a business distribution. Neton Framework's
reference fixture owns database migration and connection-zero acceptance.

Normal builds resolve the checked-in preview version from Maven Central. Scheduled
checks propose a new pin only after macOS, Linux and Windows agree. No automatic merge.

For a staged candidate, use both explicit properties:

```sh
./gradlew -PnetonVersion=VERSION -Pneton.repository=/absolute/repository linkReleaseExecutableMacosArm64
python3 scripts/runtime_smoke.py --binary build/bin/macosArm64/releaseExecutable/neton-app.kexe --candidate VERSION --output /new/evidence/directory
```

The smoke test uses isolated temporary configuration, checks the actual welcome JSON
envelope, holds health for at least 60 seconds in each of two cycles, sends SIGTERM
(Windows: targeted CTRL_BREAK_EVENT), requires exit 0 and a closed listener before
cleanup. A killed process, HTTP 200 with the wrong body, or timeout is a failure.
Evidence records the binary hash and candidate version. The framework's candidate
gate additionally pins this repository's SHA and verifies the signed upstream payload
manifest before linking. Run it on native macOS ARM64, Linux x64 and Windows x64.

本仓库的运行验收不替代框架数据库验收；版本必须固定，不能用旧 beta 成功记录
冒充新候选的证据。验收不发布 Maven 制品，也不创建正式发布标签。
