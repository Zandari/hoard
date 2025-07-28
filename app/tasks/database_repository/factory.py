import typing
from urllib.parse import urlparse, unquote
from .postgres_repository import PostgresRepository
from .quest_repository import QuestRepository


if typing.TYPE_CHECKING:
    from .base import BaseRepository


class RepositoryFactory:
    @staticmethod
    def make_repository_from_url(
        url: str,
        table_name: str,
        *args, **kwargs
    ) -> "BaseRepository":
        parsed = urlparse(url)

        protocol = parsed.scheme
        username = unquote(parsed.username) if parsed.username else None
        password = unquote(parsed.password) if parsed.password else None
        host = unquote(parsed.hostname) if parsed.hostname else None
        port = parsed.port
        database = unquote(parsed.path[1:]) if parsed.path else None

        repository_class: "BaseRepository" = {
            "quest": QuestRepository,
            "postgres": PostgresRepository
        }[protocol]

        return repository_class(
            host=host,
            port=port,
            username=username,
            password=password,
            table_name=table_name,
            *args, **kwargs
        )
