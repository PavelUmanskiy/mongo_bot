from typing import Iterable

from aiogram.types import ContentType, Message
from aiogram.filters import Filter


class ContentTypeFilter(Filter):
    def __init__(self, preferred_type: ContentType | Iterable[ContentType]
    ) -> None:
        self.preferred_type = preferred_type
    
    async def __call__(self, message: Message) -> bool:
        if type(self.preferred_type) in [list, tuple]:
            return message.content_type in self.preferred_type
        else:
            return message.content_type == self.preferred_type
        

            