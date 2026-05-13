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
        cursor = None
        try:
            if not self.connection:
                print("Database not connected")
                return None
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            if "SELECT" in sql.upper():
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def fetch_one(self, sql, params=None):
        cursor = None
        try:
            if not self.connection:
                print("Database not connected")
                return None
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor:
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

    # Queue management
    def add_to_queue(self, user_id):
        """Add user to matchmaking queue if not already in one"""
        existing = self.fetch_one("SELECT queue_id FROM queue WHERE user_id = %s", (user_id,))
        if existing:
            return existing
        self.query("INSERT INTO queue (user_id) VALUES (%s)", (user_id,))
        return self.fetch_one("SELECT * FROM queue WHERE user_id = %s ORDER BY queue_id DESC LIMIT 1", (user_id,))

    def remove_from_queue(self, user_id):
        """Remove user from queue"""
        return self.query("DELETE FROM queue WHERE user_id = %s", (user_id,))

    def find_opponent_in_queue(self, user_id):
        """Find another user in queue (not the current user) - returns oldest queued user"""
        result = self.fetch_one(
            "SELECT u.* FROM users u JOIN queue q ON u.user_id = q.user_id WHERE u.user_id != %s AND u.user_id IS NOT NULL ORDER BY q.queue_id ASC LIMIT 1",
            (user_id,)
        )
        # Verify the user still exists and is in queue
        if result:
            queue_check = self.fetch_one("SELECT queue_id FROM queue WHERE user_id = %s", (result['user_id'],))
            if queue_check:
                return result
        return None

    def get_queue_status(self, user_id):
        """Get current queue status for user"""
        return self.fetch_one("SELECT * FROM queue WHERE user_id = %s", (user_id,))

    # Match management
    def create_match(self, player1_id, player2_id):
        """Create a new match and return match details"""
        self.query("INSERT INTO matches (player1_id, player2_id, status) VALUES (%s, %s, 'active')", (player1_id, player2_id))
        return self.fetch_one(
            "SELECT * FROM matches WHERE player1_id = %s AND player2_id = %s ORDER BY match_id DESC LIMIT 1",
            (player1_id, player2_id)
        )

    def get_match(self, match_id):
        return self.fetch_one("SELECT * FROM matches WHERE match_id = %s", (match_id,))

    def get_active_match(self, user_id):
        """Get active match for user"""
        return self.fetch_one(
            "SELECT * FROM matches WHERE (player1_id = %s OR player2_id = %s) AND status = 'active' LIMIT 1",
            (user_id, user_id)
        )

    def end_match(self, match_id, winner_id):
        """End a match and record winner"""
        self.query("UPDATE matches SET status = 'ended', winner_id = %s WHERE match_id = %s", (winner_id, match_id))
        return self.get_match(match_id)

    def get_match_history(self, user_id):
        return self.query(
            "SELECT m.*, u1.username as player1_username, u2.username as player2_username FROM matches m "
            "JOIN users u1 ON m.player1_id = u1.user_id "
            "JOIN users u2 ON m.player2_id = u2.user_id "
            "WHERE (m.player1_id = %s OR m.player2_id = %s) AND m.status = 'ended' "
            "ORDER BY m.created_at DESC LIMIT 10",
            (user_id, user_id)
        )

db = DatabaseConnection()
