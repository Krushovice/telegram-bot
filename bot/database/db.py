import sqlite3 as sq


class Database:
    def __init__(self, db_file):
        self.conn = sq.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                email TEXT,
                broker TEXT
            )
        ''')
        self.conn.commit()

    def insert_user(self, user_id, full_name, username, email, broker):
        self.cursor.execute('''
            INSERT INTO users (user_id, full_name, username, email, borker)
            VALUES (?, ?, ?, ?)
        ''', (user_id, full_name, username, email, broker))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()

    def user_exists(self, user_id):
        user = self.get_user(user_id)
        if user:
            return True
        else:
            return False

    def insert_broker(self, user_id, broker):
        self.cursor.execute('UPDATE users SET broker = ? WHERE user_id = ?', (broker, user_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
