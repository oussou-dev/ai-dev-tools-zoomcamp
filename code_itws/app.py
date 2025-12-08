import reflex as rx
from pages import index
from state import State


app = rx.App(state=State)
app.add_page(index.index, route="/")


if __name__ == "__main__":
    # Compile the app (generates frontend files). Use `reflex run` to start the dev server.
    app.compile()
