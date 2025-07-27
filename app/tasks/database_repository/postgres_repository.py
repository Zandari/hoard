from .base import BaseRepository
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as Connection, cursor as Cursor
from typing import Optional


class PostgresRepository(BaseRepository):
    def __init__(
        self,
        host: str,
        port: int | str,
        username: str | None,
        password: str | None,
        database_name: str,
        table_name: str,
        *args, **kwargs
    ):
        self._connection: Connection = psycopg2.connect(
            dbname=database_name,
            host=host,
            port=port,
            user=username,
            password=password,
        )
        self._table_name = table_name
        self._cursor: Optional[Cursor] = None

    def __enter__(self) -> "PostgresRepository":
        self._cursor = self._connection.cursor()
        self._create_table()
        return self

    def _create_table(self) -> None:
        if not self._cursor:
            raise RuntimeError("Cursor not initialized")

        query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table} (
            exchange VARCHAR(50) NOT NULL,
            instrument VARCHAR(50) NOT NULL,
            period VARCHAR(10) NOT NULL,
            timestamp BIGINT NOT NULL,
            open_price NUMERIC(18, 8) NOT NULL,
            highest_price NUMERIC(18, 8) NOT NULL,
            lowest_price NUMERIC(18, 8) NOT NULL,
            close_price NUMERIC(18, 8) NOT NULL,
            PRIMARY KEY (exchange, instrument, period, timestamp)
        );
        """).format(table=sql.Identifier(self._table_name))

        self._cursor.execute(query)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._cursor:
            if exc_type is None:
                self._connection.commit()
            else:
                self._connection.rollback()
            self._cursor.close()

    def close(self) -> None:
        self._connection.close()

    def insert_candlestick(
        self,
        exchange_identifier: str,
        instrument_identifier: str,
        period: str,
        timestamp_dt: int,
        open_price: int | float,
        highest_price: int | float,
        lowest_price: int | float,
        close_price: int | float
    ) -> None:
        if not self._cursor:
            raise RuntimeError("Context manager not active")

        query = sql.SQL("""
            INSERT INTO {table} (
                exchange, instrument, period,
                timestamp, open_price, highest_price,
                lowest_price, close_price  # Added missing column
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """).format(table=sql.Identifier(self._table_name))

        self._cursor.execute(query, (
            exchange_identifier,
            instrument_identifier,
            period,
            timestamp_dt,
            open_price,
            highest_price,
            lowest_price,
            close_price,  # Added missing value
        ))
