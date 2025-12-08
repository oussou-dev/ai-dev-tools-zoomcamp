import reflex as rx
from state import State


def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.image(src="/static/img/logo.svg", height="8"),
                    rx.heading("CodeITWS", size="md"),
                    rx.text("Collaborative coding interviews", color="gray.500", font_size="sm"),
                    spacing="3",
                ),
                spacing="0",
            ),
            rx.hstack(
                rx.input(_id="share-link", read_only=True, placeholder="share link"),
                rx.button("Create link", id="create-link", bg="indigo.600", color="white"),
                rx.button("Copy", id="copy-link"),
                spacing="2",
            ),
            justify="space-between",
            align="center",
            padding="4",
            bg="white",
            shadow="sm",
        )
    )


def editor_panel() -> rx.Component:
    # The actual editor UI will be hydrated by our static JS that attaches CodeMirror to #editor
    return rx.box(
        rx.vstack(
            # Hidden textarea bound to server state. CodeMirror will be initialized from this textarea
            rx.textarea(id="code-textarea", value=State.get_code(), on_change=State.set_code, style={"display": "none"}),

            rx.hstack(
                rx.heading("Shared Code Editor", size="md"),
                rx.text("Real-time: ", id="status-label", color="orange.400"),
                rx.select(
                    children=[
                        rx.option("Python", value="python"),
                        rx.option("JavaScript", value="javascript"),
                        rx.option("Java", value="java"),
                        rx.option("C", value="c"),
                        rx.option("C++", value="cpp"),
                    ],
                    id="language",
                ),
                rx.button("Run (browser)", id="run-code", bg="green.600", color="white"),
                spacing="3",
                justify="space-between",
                align="center",
            ),
            rx.box(id="editor", style={"flex": "1", "minHeight": "480px", "border": "1px solid #e5e7eb"}),
            rx.hstack(rx.button("Undo", id="undo"), rx.button("Redo", id="redo"), justify="end"),
            spacing="3",
            padding="4",
            bg="white",
            shadow="sm",
            height="72vh",
        )
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.heading("Session", size="sm"),
                rx.text("Share the generated link with candidates to join this session.", color="gray.600", font_size="sm"),
                rx.hstack(rx.text("Room", width="20"), rx.input(id="room", placeholder="room id")),
                rx.hstack(rx.text("Language", width="20"), rx.text("Python", id="lang-preview")),
                spacing="3",
            ),
            rx.box(
                rx.heading("Output", size="sm"),
                rx.pre(id="output", children="Program output will appear here."),
                spacing="3",
            ),
            rx.box(
                rx.heading("Participants", size="sm"),
                rx.unordered_list(rx.list_item("Owner (you)"), id="participants"),
            ),
            spacing="4",
            padding="4",
            bg="white",
            shadow="sm",
        )
    )


def index() -> rx.Component:
    # Include external CDN scripts and static JS/CSS required for CodeMirror and editor behavior
    head = rx.tags.head(
        rx.tags.script(src="https://cdn.tailwindcss.com"),
        rx.tags.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css"),
        rx.tags.link(rel="stylesheet", href="/static/css/style.css"),
    )

    scripts = rx.tags.raw("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/javascript/javascript.min.js"></script>
    <script src="/static/js/editor.js"></script>
    """)

    layout = rx.box(
        header(),
        rx.container(
            rx.grid(
                rx.grid_item(editor_panel(), col_span=8),
                rx.grid_item(sidebar(), col_span=4),
                template_columns="repeat(12, minmax(0, 1fr))",
                gap=6,
            ),
            max_width="6xl",
            padding_top=8,
        ),
        scripts,
    )

    return rx.vstack(head, layout)
