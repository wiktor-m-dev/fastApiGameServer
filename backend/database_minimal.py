import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "game_server")
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Database connected")
        except Error as e:
            print(f"Error: {e}")

    def query(self, sql, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.connection.commit()
            return cursor.fetchall() if "SELECT" in sql.upper() else cursor.lastrowid
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def fetch_one(self, sql, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def user_exists(self, username):
        result = self.fetch_one("SELECT user_id FROM users WHERE username = %s", (username,))
        return result is not None

    def create_user(self, username, password):
        if self.user_exists(username):
            return None
        hashed = self.hash_password(password)
        self.query("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        return self.fetch_one("SELECT * FROM users WHERE username = %s", (username,))

    def authenticate_user(self, username, password):
        user = self.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user and self.verify_password(password, user['password']):
            return user
        return None

    def get_user(self, user_id):
        return self.fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))

    def create_match(self, player1_id, player2_id):
        self.query("INSERT INTO matches (player1_id, player2_id) VALUES (%s, %s)", (player1_id, player2_id))
        return self.fetch_one("SELECT * FROM matches WHERE player1_id = %s AND player2_id = %s ORDER BY created_at DESC LIMIT 1", (player1_id, player2_id))

    def find_opponent(self, user_id):
        return self.fetch_one("SELECT * FROM users WHERE user_id != %s ORDER BY user_id LIMIT 1", (user_id,))

    def get_match(self, match_id):
        return self.fetch_one("SELECT * FROM matches WHERE match_id = %s", (match_id,))

    def end_match(self, match_id, winner_id):
        self.query("UPDATE matches SET winner_id = %s WHERE match_id = %s", (winner_id, match_id))

    def get_match_history(self, user_id):
        return self.query("SELECT * FROM matches WHERE player1_id = %s OR player2_id = %s ORDER BY created_at DESC LIMIT 10", (user_id, user_id))

db = DatabaseConnection()
