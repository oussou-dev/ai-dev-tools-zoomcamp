import reflex as rx


class State(rx.State):
    """Shared application state for the collaborative editor."""

    code: str = "# Welcome to CodeITWS\nprint('Hello from Reflex')\n"
    language: str = "python"

    @rx.var
    def get_code(self) -> str:
        return self.code

    @rx.var
    def get_language(self) -> str:
        return self.language

    @rx.action
    def set_code(self, code: str) -> None:
        """Server action to update the shared code value."""
        # naive replace - in a production app use OT/CRDT for collaborative edits
        self.code = code

    @rx.action
    def set_language(self, language: str) -> None:
        self.language = language
