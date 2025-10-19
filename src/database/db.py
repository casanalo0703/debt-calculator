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
        """Crea las tablas necesarias si no existen"""
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
                description TEXT,
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
                SELECT p.id, p.debt_id, p.client_id, p.amount, p.payment_date, 
                    p.description, c.name as client_name, d.ticket_number
                FROM payments p
                JOIN clients c ON p.client_id = c.id
                LEFT JOIN debts d ON p.debt_id = d.id
                WHERE strftime('%m', p.payment_date) = ? 
                AND strftime('%Y', p.payment_date) = ?
                ORDER BY p.payment_date DESC
            """,
                (f"{month:02d}", str(year)),
            )
            return [
                Payment(
                    id=row[0],
                    debt_id=row[1],
                    client_id=row[2],
                    amount=row[3],
                    date=row[4],
                    description=row[5],
                    ticket_number=row[6],
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
                SELECT id, client_id, amount, due_date, description, ticket_number, created_at
                FROM debts
                WHERE strftime('%m', created_at) = ? 
                AND strftime('%Y', created_at) = ?
                AND client_id = ?
                ORDER BY created_at DESC
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
                SELECT p.id, p.debt_id, p.client_id, p.amount, p.payment_date, p.description, d.ticket_number
                FROM payments p
                    LEFT JOIN debts d ON p.debt_id = d.id
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
                    debt_id=row[1],
                    client_id=row[2],
                    amount=row[3],
                    date=row[4],
                    description=row[5],
                    ticket_number=row[6],
                )
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener pagos: {str(e)}")

    def add_payment(self, payment: Payment) -> None:
        self.cursor.execute(
            "INSERT INTO payments (client_id, debt_id, amount, payment_date, description) VALUES (?, ?, ?, ?, ?)",
            (
                payment.client_id,
                payment.debt_id,
                payment.amount,
                payment.date,
                payment.description,
            ),
        )
        self.connection.commit()

    def get_debts_by_client(self, client_id: int) -> list[Debt]:
        self.cursor.execute(
            """
            SELECT id, client_id, amount, due_date, description, ticket_number, created_at
            FROM debts
            WHERE client_id = ?
            ORDER BY created_at DESC
        """,
            (client_id,),
        )
        debts = self.cursor.fetchall()
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
            for row in debts
        ]

    def get_remaining_debt(self, debt_id: int) -> float:
        self.cursor.execute(
            """
            SELECT amount FROM debts WHERE id = ?
        """,
            (debt_id,),
        )
        debt = self.cursor.fetchone()
        if not debt:
            return 0.0

        total_debt = debt[0]

        self.cursor.execute(
            """
            SELECT SUM(amount) FROM payments WHERE debt_id = ?
        """,
            (debt_id,),
        )
        payments = self.cursor.fetchone()
        total_payments = payments[0] if payments[0] is not None else 0.0

        return total_debt - total_payments

    def close(self) -> None:
        self.connection.close()

    def get_all_debts_by_client(self, client_id: int) -> list[Debt]:
        try:
            self.cursor.execute(
                """
                SELECT d.id, d.client_id, d.amount, d.due_date, d.created_at, 
                    d.description, d.ticket_number
                FROM debts d
                WHERE d.client_id = ?
                ORDER BY d.created_at DESC
            """,
                (client_id,),
            )
            return [
                Debt(
                    id=row[0],
                    client_id=row[1],
                    amount=row[2],
                    due_date=row[3],
                    created_at=row[4],
                    description=row[5],
                    ticket_number=row[6],
                )
                for row in self.cursor.fetchall()
            ]
        except Exception as e:
            print(f"Error en get_all_debts_by_client: {str(e)}")
            return []

    def get_all_payments_by_client(self, client_id: int) -> list[Payment]:
        try:
            self.cursor.execute(
                """
                SELECT p.id, p.client_id, p.debt_id, p.amount, 
                    p.payment_date, p.description, d.ticket_number
                FROM payments p
                LEFT JOIN debts d ON p.debt_id = d.id
                WHERE p.client_id = ?
                ORDER BY p.payment_date DESC
            """,
                (client_id,),
            )
            return [
                Payment(
                    id=row[0],
                    client_id=row[1],
                    debt_id=row[2],
                    amount=row[3],
                    date=row[4],
                    description=row[5],
                    ticket_number=row[6],
                )
                for row in self.cursor.fetchall()
            ]
        except Exception as e:
            print(f"Error en get_all_payments_by_client: {str(e)}")
            return []
