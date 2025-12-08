import reflex as rx
from pages import index


class State(rx.State):
    """Application state for the collaborative editor."""

    code: str = "# Welcome to CodeITWS\nprint('Hello from Reflex')\n"
    language: str = "python"


app = rx.App(state=State)
app.add_page(index.index, route="/")


if __name__ == "__main__":
    # Compile the app (generates frontend files). Use `reflex run` to start the dev server.
    app.compile()
