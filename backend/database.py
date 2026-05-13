import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any, Tuple
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

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Database connection successful")
            return self.connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            cursor.close()

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def user_exists(self, username: str) -> bool:
        """Check if a user exists by username"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"Query error: {e}")
            return False

    def create_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Create a new user with hashed password"""
        try:
            # Check if user already exists
            if self.user_exists(username):
                return None
            
            # Hash the password
            hashed_password = self.hash_password(password)
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            self.connection.commit()
            
            # Get the newly created user
            user_id = cursor.lastrowid
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            
            return user
        except Error as e:
            print(f"Query error: {e}")
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user by username and password"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            
            if user and self.verify_password(password, user['password']):
                return user
            return None
        except Error as e:
            print(f"Query error: {e}")
            return None

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by user_id"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Query error: {e}")
            return None

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            cursor.close()

# Global database instance
db = DatabaseConnection()
