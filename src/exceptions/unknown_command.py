class UnknownCommand(Exception):
    def __init__(self, command: str, message="Unknown command") -> None:
        self.command = command
        super().__init__(f"{message}:{command}")
