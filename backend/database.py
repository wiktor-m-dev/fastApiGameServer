import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

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
