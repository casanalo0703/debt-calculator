import sqlite3

from models.debt import Debt
from models.payment import Payment
from models.client import Client


class Database:
    def __init__(self, db_name: str = "deudas.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                amount REAL NOT NULL,
                due_date TEXT NOT NULL,
                description TEXT,
                ticket_number TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                debt_id INTEGER,
                amount REAL NOT NULL,
                payment_date TEXT NOT NULL,
                FOREIGN KEY (debt_id) REFERENCES debts (id),
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        """
        )
        self.connection.commit()

    def get_all_debts(self) -> list[tuple[str, float, str, str | None, str | None]]:
        self.cursor.execute(
            """
            SELECT c.name, d.amount, d.due_date, d.description, d.ticket_number
            FROM debts d
            JOIN clients c ON d.client_id = c.id
            ORDER BY d.created_at DESC
        """
        )
        debts = self.cursor.fetchall()
        return debts

    def get_all_payments(self) -> list[tuple[str, float, str, str | None]]:
        self.cursor.execute(
            """
            SELECT c.name, p.amount, p.payment_date
            FROM payments p
            JOIN clients c ON p.client_id = c.id
            ORDER BY p.payment_date DESC
        """
        )
        payments = self.cursor.fetchall()
        return payments

    def add_client(self, client: Client) -> int | None:
        """
        Agrega un nuevo cliente a la base de datos
        Retorna: ID del cliente creado
        """
        try:
            self.cursor.execute(
                """
                    INSERT INTO clients (name, phone, email, created_at)
                    VALUES (?, ?, ?, ?)
                """,
                (
                    client.name,
                    client.phone,
                    client.email,
                    client.created_at.isoformat(),
                ),
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            raise Exception(f"Error al agregar cliente: {str(e)}")

    def get_client(self, client_id: int) -> Client | None:
        """
        Obtiene un cliente por su ID
        """
        self.cursor.execute(
            """
            SELECT id, name, phone, email, created_at
            FROM clients
            WHERE id = ?
        """,
            (client_id,),
        )
        client = self.cursor.fetchone()
        if client:
            return Client(
                id=client[0],
                name=client[1],
                phone=client[2],
                email=client[3],
                created_at=client[4],
            )
        return None

    def get_all_clients(self) -> list[Client]:
        """
        Obtiene todos los clientes
        """
        self.cursor.execute(
            """
            SELECT id, name, phone, email, created_at
            FROM clients
            ORDER BY id DESC
        """
        )
        clients = self.cursor.fetchall()
        return [
            Client(
                id=client[0],
                name=client[1],
                phone=client[2],
                email=client[3],
                created_at=client[4],
            )
            for client in clients
        ]

    def update_client(self, client_id: int, client_data: Client) -> None:
        try:
            self.cursor.execute(
                """
                UPDATE clients 
                SET name = ?, phone = ?, email = ?
                WHERE id = ?
            """,
                (client_data.name, client_data.phone, client_data.email, client_id),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            raise Exception(f"Error al actualizar cliente: {str(e)}")

    def add_debt(
        self,
        debt: Debt,
    ) -> None:
        self.cursor.execute(
            "INSERT INTO debts (client_id, amount, due_date, description, ticket_number) VALUES (?, ?, ?, ?, ?)",
            (
                debt.client_id,
                debt.amount,
                debt.due_date,
                debt.description,
                debt.ticket_number,
            ),
        )
        self.connection.commit()

    def get_debts_by_month(self, month: int, year: int) -> list[Debt]:
        try:
            self.cursor.execute(
                """
                SELECT d.id, d.client_id, d.amount, d.due_date, d.description, 
                    d.status, c.name as client_name
                FROM debts d
                JOIN clients c ON d.client_id = c.id
                WHERE strftime('%m', d.due_date) = ? 
                AND strftime('%Y', d.due_date) = ?
                ORDER BY d.due_date DESC
            """,
                (f"{month:02d}", str(year)),
            )
            return [
                Debt(
                    id=row[0],
                    client_id=row[1],
                    amount=row[2],
                    due_date=row[3],
                    description=row[4],
                    ticket_number=row[5],
                    created_at=row[6],
                )
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener deudas: {str(e)}")

    def get_payments_by_month(self, month: int, year: int) -> list[Payment]:
        try:
            self.cursor.execute(
                """
                SELECT p.id, p.client_id, p.amount, p.payment_date, 
                    p.description, c.name as client_name
                FROM payments p
                JOIN clients c ON p.client_id = c.id
                WHERE strftime('%m', p.payment_date) = ? 
                AND strftime('%Y', p.payment_date) = ?
                ORDER BY p.payment_date DESC
            """,
                (f"{month:02d}", str(year)),
            )
            return [
                Payment(
                    id=row[0],
                    client_id=row[1],
                    amount=row[2],
                    date=row[3],
                    description=row[4],
                )
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener pagos: {str(e)}")

    def get_debts_by_month_and_client(
        self, month: int, year: int, client_id: int
    ) -> list[Debt]:
        try:
            self.cursor.execute(
                """
                SELECT *
                FROM debts d
                WHERE strftime('%m', d.created_at) = ? 
                AND strftime('%Y', d.created_at) = ?
                AND d.client_id = ?
                ORDER BY d.created_at DESC
            """,
                (f"{month:02d}", str(year), client_id),
            )
            return [
                Debt(
                    id=row[0],
                    client_id=row[1],
                    amount=row[2],
                    due_date=row[3],
                    description=row[4],
                    ticket_number=row[5],
                    created_at=row[6],
                )
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener deudas: {str(e)}")

    def get_payments_by_month_and_client(
        self, month: int, year: int, client_id: int
    ) -> list[Payment]:
        try:
            self.cursor.execute(
                """
                SELECT *
                FROM payments p
                WHERE strftime('%m', p.payment_date) = ? 
                AND strftime('%Y', p.payment_date) = ?
                AND p.client_id = ?
                ORDER BY p.payment_date DESC
            """,
                (f"{month:02d}", str(year), client_id),
            )
            return [
                Payment(
                    id=row[0],
                    client_id=row[1],
                    amount=row[2],
                    date=row[3],
                    description=row[4],
                )
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener pagos: {str(e)}")

    def close(self) -> None:
        self.connection.close()
