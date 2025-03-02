import psycopg2
from datetime import datetime
import os
import time

class Message:
    def __init__(self, array):
        self.id = str(array[0])
        self.isBot = str(array[1])
        self.message = str(array[2])
        self.time = str(array[3])

    def to_dict(self):
        return {
            "id": self.id,
            "isBot": self.isBot,
            "message": self.message,
            "time": self.time,
        }

class DB:
    def __init__(self, max_retries=5, retry_delay=2):
        self.conn = None
        retries = 0
        
        while retries < max_retries:
            try:
                self.conn = psycopg2.connect(
                    database="mydatabase", 
                    user="myuser", 
                    password="mypassword", 
                    host='db', 
                    port=5432
                )
                print("Successfully connected to the database")
                # Test if table exists
                self._test_table_exists()
                break
            except Exception as e:
                retries += 1
                print(f"Connection attempt {retries} failed: {e}")
                if retries >= max_retries:
                    raise Exception(f"Failed to connect to database after {max_retries} attempts")
                time.sleep(retry_delay)
    
    def _test_table_exists(self):
        """Test if the conversation table exists"""
        cur = self.conn.cursor()
        cur.execute("SELECT to_regclass('conversation');")
        result = cur.fetchone()[0]
        cur.close()
        
        if result is None:
            print("WARNING: 'conversation' table does not exist")
            print("Attempting to create table...")
            self._create_table()
        else:
            print(f"Table exists: {result}")
    
    def _create_table(self):
        """Create the conversation table if it doesn't exist"""
        try:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversation (
                    id SERIAL PRIMARY KEY,
                    isBot BOOLEAN NOT NULL,
                    message TEXT NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
            cur.close()
            print("Table created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
            raise

    def findLastMessage(self, n):
        curs = self.conn.cursor()
        # Use lowercase table name to match what we created
        query = "SELECT * FROM conversation ORDER BY id DESC LIMIT %s;"
        curs.execute(query, (n,))
        messages = curs.fetchall()
        curs.close()
        return [Message(message).to_dict() for message in messages]
         
    def insertMessage(self, is_bot, message):
        time = datetime.now()
        
        # Use lowercase table name to match what we created
        query = "INSERT INTO conversation (isBot, message, time) VALUES (%s, %s, %s);"
        
        try:
            cur = self.conn.cursor()
            cur.execute(query, (is_bot, message, time))
            self.conn.commit()
            
            cur.close()
            print("Message inserted successfully!")
        except Exception as e:
            print("Error inserting message:", e)
            # Rollback in case of error
            self.conn.rollback()