package controller

import kotlinx.serialization.Serializable
import neton.core.annotations.Controller
import neton.core.annotations.Get
import neton.core.http.HttpContext

@Serializable
data class Hello(val message: String, val framework: String, val version: String)

@Controller
class WelcomeController {

    @Get("/")
    suspend fun index(ctx: HttpContext) {
        ctx.response.html(WELCOME_PAGE)
    }

    @Get("/api/hello")
    fun hello(): Hello = Hello(
        message = "Welcome to Neton",
        framework = "Neton",
        version = NETON_VERSION,
    )

    companion object {
        const val NETON_VERSION = "1.0.0-beta2"

        val WELCOME_PAGE = """
            <!doctype html>
            <html lang="en">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>Welcome to Neton</title>
              <style>
                :root { color-scheme: light dark; }
                body { margin: 0; font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                       display: flex; min-height: 100vh; align-items: center; justify-content: center; }
                main { max-width: 42rem; padding: 3rem 1.5rem; }
                h1 { font-size: 2.25rem; margin: 0 0 .5rem; }
                p { margin: .5rem 0; opacity: .85; }
                code { padding: .15em .4em; border-radius: 4px; background: rgba(127,127,127,.15); }
                ul { padding-left: 1.2rem; }
                footer { margin-top: 2rem; font-size: .9rem; opacity: .6; }
              </style>
            </head>
            <body>
              <main>
                <h1>Welcome to Neton</h1>
                <p>If you can see this page, your Neton application is up and serving requests.</p>
                <p>This is <code>neton-app</code>, a minimal application built on Neton $NETON_VERSION.
                   Edit <code>src/commonMain/kotlin/controller/WelcomeController.kt</code> to make it yours.</p>
                <ul>
                  <li>JSON endpoint: <a href="/api/hello"><code>/api/hello</code></a></li>
                  <li>Documentation: <a href="https://netonframework.github.io/">netonframework.github.io</a></li>
                  <li>Source: <a href="https://github.com/netonframework/neton">github.com/netonframework/neton</a></li>
                </ul>
                <footer>Neton · Kotlin/Native · compiled to a native binary, no JVM</footer>
              </main>
            </body>
            </html>
        """.trimIndent()
    }
}
