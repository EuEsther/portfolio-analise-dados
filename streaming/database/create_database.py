"""Create the SQLite database used by the streaming platform."""

from pathlib import Path
import sqlite3


DATABASE_PATH = Path(__file__).resolve().parent / "streaming.db"


def create_database(database_path: Path = DATABASE_PATH) -> None:
    """Create the schema if it does not already exist."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    try:
        with connection:
            # SQLite foreign key enforcement is disabled by default and is per connection.
            connection.execute("PRAGMA foreign_keys = ON")

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data_adesao TEXT,
                    tipo_plano TEXT,
                    status_assinatura TEXT NOT NULL
                        CHECK (status_assinatura IN ('Ativo', 'Cancelado'))
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS historico_visualizacao (
                    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    data TEXT,
                    titulo_conteudo TEXT,
                    genero TEXT,
                    minutos_assistidos REAL
                        CHECK (
                            minutos_assistidos IS NULL
                            OR (
                                typeof(minutos_assistidos) IN ('integer', 'real')
                                AND minutos_assistidos >= 0
                            )
                        ),
                    dispositivo_utilizado TEXT,
                    FOREIGN KEY (id_cliente)
                        REFERENCES clientes (id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_historico_visualizacao_id_cliente
                ON historico_visualizacao (id_cliente)
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_historico_visualizacao_data
                ON historico_visualizacao (data)
                """
            )
    finally:
        connection.close()


if __name__ == "__main__":
    create_database()
    print(f"Banco de dados criado/verificado em: {DATABASE_PATH}")
