"""Insert a deterministic, fictional sample dataset into streaming.db."""

from datetime import date, datetime, time, timedelta
from pathlib import Path
import sqlite3


DATABASE_PATH = Path(__file__).resolve().parent / "streaming.db"

FIRST_NAMES = [
    "Ana", "Bruno", "Camila", "Diego", "Elisa", "Felipe", "Gabriela", "Henrique", "Isabela", "João",
    "Karen", "Lucas", "Mariana", "Nicolas", "Olivia", "Pedro", "Quitéria", "Rafael", "Sofia", "Thiago",
    "Úrsula", "Vinícius", "Wesley", "Yasmin", "Caio",
]
LAST_NAMES = [
    "Almeida", "Barbosa", "Carvalho", "Dias", "Esteves", "Ferreira", "Gomes", "Moura", "Oliveira", "Pereira",
    "Queiroz", "Ribeiro", "Silva", "Teixeira", "Vargas", "Andrade", "Costa", "Freitas", "Lima", "Nogueira",
]
PLANS = ("Básico", "Padrão", "Premium")
STATUSES = ("Ativo", "Cancelado")
GENRES = (
    "Ação", "Comédia", "Drama", "Suspense", "Terror", "Ficção Científica",
    "Documentário", "Animação",
)
DEVICES = ("Smart TV", "Smartphone", "Computador", "Tablet")
TITLES = (
    "Horizonte de Aço", "Apartamento 23", "Cartas para Aurora", "O Último Sinal",
    "Noite no Observatório", "Órbita de Vidro", "Rios Invisíveis", "Pequenos Gigantes",
    "Código Boreal", "Café das Seis", "Entre Duas Estações", "A Casa na Colina",
    "Maré de Outubro", "Planeta de Papel", "Arquivo das Sombras", "Manual do Amanhã",
    "Ventos do Norte", "O Enigma do Farol", "Quase Domingo", "Jardim de Inverno",
    "Cidade Submersa", "Frequência Zero", "Receita para Recomeçar", "Além da Neblina",
    "Estação Luar", "O Peso das Nuvens", "Retratos da Terra", "Robôs no Quintal",
    "Linha de Fuga", "A Última Página", "Ponto de Encontro", "Vigília",
    "Oceano de Dentro", "Mundo Miúdo", "Chave Mestra", "Riso de Quinta",
    "Depois do Eclipse", "O Som das Montanhas", "Projeto Íris", "Férias em Marte",
    "Fronteira Azul", "Segredos do Mercado", "A Menina e o Cometa", "Sinais de Fumaça",
    "Quarto Andar", "Vida em Miniatura", "Operação Miragem", "Ecos da Floresta",
    "Um Lugar ao Sol", "Pássaros de Neon",
)


def build_clients() -> list[tuple[str, str, str, str]]:
    """Build 50 stable fictional clients with varied signup dates and plans."""
    rows = []
    start = date(2022, 1, 1)
    for index in range(50):
        first = FIRST_NAMES[index % len(FIRST_NAMES)]
        last = LAST_NAMES[(index * 7 + index // len(FIRST_NAMES)) % len(LAST_NAMES)]
        name = f"{first} {last}"
        signup = start + timedelta(days=(index * 29 + index % 7 * 11) % 1400)
        plan = PLANS[(index * 2 + index // 3) % len(PLANS)]
        status = STATUSES[1] if index % 4 == 1 else STATUSES[0]
        rows.append((name, signup.isoformat(), plan, status))
    assert len({row[0] for row in rows}) == 50
    return rows


def build_views(clients: list[tuple[str, str, str, str]]) -> list[tuple[int, str, str, str, float, str]]:
    """Build one view per client, always on or after that client's signup."""
    cutoff = date(2025, 11, 30)
    rows = []
    for index in range(50):
        client_index = (index * 17) % 50
        signup = date.fromisoformat(clients[client_index][1])
        available_days = max(0, (cutoff - signup).days)
        viewed_on = signup + timedelta(days=(index * 37 + 13) % (available_days + 1))
        viewed_at = datetime.combine(
            viewed_on,
            time(hour=(index * 3) % 24, minute=(index * 11) % 60),
        ).isoformat(timespec="minutes")
        rows.append(
            (
                client_index,
                viewed_at,
                TITLES[index],
                GENRES[(index * 3) % len(GENRES)],
                float(12 + (index * 19) % 109),
                DEVICES[(index * 3) % len(DEVICES)],
            )
        )
    return rows


def populate_database(database_path: Path = DATABASE_PATH) -> None:
    clients = build_clients()
    views = build_views(clients)
    client_names = [row[0] for row in clients]

    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            existing = {
                row[0]: row[1]
                for row in connection.execute(
                    "SELECT nome, id FROM clientes WHERE nome IN ({})".format(
                        ",".join("?" for _ in client_names)
                    ),
                    client_names,
                )
            }
            total_clients = connection.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
            total_views = connection.execute("SELECT COUNT(*) FROM historico_visualizacao").fetchone()[0]

            if len(existing) == 50:
                # Treat a complete existing batch as a successful no-op.
                matching_views = 0
                for client_index, viewed_at, title, *_ in views:
                    matching_views += connection.execute(
                        """
                        SELECT COUNT(*) FROM historico_visualizacao
                        WHERE id_cliente = ? AND data = ? AND titulo_conteudo = ?
                        """,
                        (existing[client_names[client_index]], viewed_at, title),
                    ).fetchone()[0]
                if matching_views == 50 and total_clients == 50 and total_views == 50:
                    return
                raise RuntimeError(
                    "Foi encontrado um lote parcial ou dados adicionais; nenhuma alteração foi feita."
                )

            if existing or total_clients or total_views:
                raise RuntimeError(
                    "O banco já contém dados ou parte deste lote; nenhuma alteração foi feita. "
                    "Revise os registros antes de executar a carga."
                )

            connection.executemany(
                """
                INSERT INTO clientes (nome, data_adesao, tipo_plano, status_assinatura)
                VALUES (?, ?, ?, ?)
                """,
                clients,
            )
            ids_by_name = {
                name: client_id
                for name, client_id in connection.execute(
                    "SELECT nome, id FROM clientes WHERE nome IN ({})".format(
                        ",".join("?" for _ in client_names)
                    ),
                    client_names,
                )
            }
            connection.executemany(
                """
                INSERT INTO historico_visualizacao
                    (id_cliente, data, titulo_conteudo, genero, minutos_assistidos, dispositivo_utilizado)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (ids_by_name[client_names[client_index]], viewed_at, title, genre, minutes, device)
                    for client_index, viewed_at, title, genre, minutes, device in views
                ],
            )
    finally:
        connection.close()


def validate_and_report(database_path: Path = DATABASE_PATH) -> None:
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        client_count = connection.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        view_count = connection.execute("SELECT COUNT(*) FROM historico_visualizacao").fetchone()[0]
        assert client_count == 50, f"Esperados 50 clientes; encontrados {client_count}."
        assert view_count == 50, f"Esperados 50 eventos; encontrados {view_count}."

        orphan_count = connection.execute(
            """
            SELECT COUNT(*) FROM historico_visualizacao h
            LEFT JOIN clientes c ON c.id = h.id_cliente
            WHERE c.id IS NULL
            """
        ).fetchone()[0]
        invalid_dates = connection.execute(
            """
            SELECT COUNT(*)
            FROM historico_visualizacao h
            JOIN clientes c ON c.id = h.id_cliente
            WHERE datetime(h.data) IS NULL OR date(h.data) < date(c.data_adesao)
            """
        ).fetchone()[0]
        assert orphan_count == 0, f"Encontrados {orphan_count} eventos órfãos."
        assert invalid_dates == 0, f"Encontrados {invalid_dates} eventos com data inválida ou anterior à adesão."
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []

        plans = dict(connection.execute("SELECT tipo_plano, COUNT(*) FROM clientes GROUP BY tipo_plano"))
        statuses = dict(connection.execute("SELECT status_assinatura, COUNT(*) FROM clientes GROUP BY status_assinatura"))
        genres = dict(connection.execute("SELECT genero, COUNT(*) FROM historico_visualizacao GROUP BY genero"))
        devices = dict(connection.execute("SELECT dispositivo_utilizado, COUNT(*) FROM historico_visualizacao GROUP BY dispositivo_utilizado"))
        join_count = connection.execute(
            "SELECT COUNT(*) FROM clientes c JOIN historico_visualizacao h ON h.id_cliente = c.id"
        ).fetchone()[0]
        assert len(plans) >= 3 and len(statuses) == 2
        assert len(genres) == 8 and len(devices) == 4 and join_count == 50

        print(f"Clientes: {client_count}; visualizações: {view_count}; JOIN: {join_count} linhas.")
        print(f"Planos: {plans}")
        print(f"Status: {statuses}")
        print(f"Gêneros: {genres}")
        print(f"Dispositivos: {devices}")
        print(f"Órfãos: {orphan_count}; datas inválidas/anteriores à adesão: {invalid_dates}; FK: OK.")
    finally:
        connection.close()


if __name__ == "__main__":
    populate_database()
    validate_and_report()
