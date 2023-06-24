from typing import List
from pyrogram.handlers.message_handler import MessageHandler


class UBModule:
    name: str
    command: str
    help_text: str
    dependencies: List[str]
    handler: MessageHandler

    def __init__(
        self,
        name: str,
        help_text: str,
        handler: MessageHandler,
        dependencies: List[str] = [],
    ) -> None:
        self.name = name
        self.dependencies = dependencies
        self.handler = handler
        self.help_text = help_text
