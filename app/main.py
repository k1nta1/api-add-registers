from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_PATH = Path("/data/registros.db")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                version TEXT NOT NULL,
                fecha TEXT NOT NULL
            )
            """
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Normativa Records API", version="1.0.0", lifespan=lifespan)


class RecordCreate(BaseModel):
    usuario: str = Field(min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=255)


class Record(BaseModel):
    id: int
    usuario: str
    version: str
    fecha: datetime


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/records", response_model=Record, status_code=201)
def create_record(record: RecordCreate) -> Record:
    fecha = datetime.now(timezone.utc)
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO records (usuario, version, fecha) VALUES (?, ?, ?)",
            (record.usuario, record.version, fecha.isoformat()),
        )
        record_id = cursor.lastrowid
    return Record(id=record_id, usuario=record.usuario, version=record.version, fecha=fecha)


@app.get("/records", response_model=list[Record])
def list_records() -> list[Record]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, usuario, version, fecha FROM records ORDER BY id ASC"
        ).fetchall()
    return [Record(**dict(row)) for row in rows]
