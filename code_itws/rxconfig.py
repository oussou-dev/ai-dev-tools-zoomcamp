import reflex as rx

config = rx.Config(
    app_name="code_itws",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)