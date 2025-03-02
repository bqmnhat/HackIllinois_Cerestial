import psycopg2
from datetime import datetime
import os
import time
import pytz

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
    def __init__(self, max_retries=5, retry_delay=2, reset_table=True):
        self.conn = None
        retries = 0
        
        # Get database connection details from environment variables
        db_host = os.environ.get('DB_HOST', 'db')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'mydatabase')
        db_user = os.environ.get('DB_USER', 'myuser')
        db_password = os.environ.get('DB_PASSWORD', 'mypassword')
        
        while retries < max_retries:
            try:
                self.conn = psycopg2.connect(
                    database=db_name, 
                    user=db_user, 
                    password=db_password, 
                    host=db_host, 
                    port=db_port
                )
                print("Successfully connected to the database")
                
                # Check if we need to reset the table
                if reset_table:
                    self._reset_table()
                else:
                    # Just check if table exists
                    self._ensure_table_exists()
                    
                break
            except Exception as e:
                retries += 1
                print(f"Connection attempt {retries} failed: {e}")
                if retries >= max_retries:
                    raise Exception(f"Failed to connect to database after {max_retries} attempts")
                time.sleep(retry_delay)
    
    def _ensure_table_exists(self):
        """Check if the conversation table exists, create if it doesn't"""
        cur = self.conn.cursor()
        cur.execute("SELECT to_regclass('conversation');")
        result = cur.fetchone()[0]
        cur.close()
        
        if result is None:
            print("Table 'conversation' does not exist, creating it...")
            self._create_table()
        else:
            print(f"Table exists: {result}")
    
    def _reset_table(self):
        """Drop the conversation table if it exists and recreate it"""
        try:
            cur = self.conn.cursor()
            
            # Drop table if exists
            cur.execute("DROP TABLE IF EXISTS conversation;")
            print("Dropped existing conversation table")
            
            # Create new table
            self._create_table()
            
            # Reset sequence
            cur.execute("ALTER SEQUENCE conversation_id_seq RESTART WITH 1;")
            print("Reset sequence to start from 1")
            
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Error resetting table: {e}")
            self.conn.rollback()
            raise
    
    def _create_table(self):
        """Create the conversation table"""
        try:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE conversation (
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
            self.conn.rollback()
            raise

    def findLastMessages(self, n, page, max_id):
        curs = self.conn.cursor()
        offset = page * n
        query = "SELECT * FROM conversation WHERE id < %s ORDER BY id DESC OFFSET %s ROWS LIMIT %s;"
        curs.execute(query, (max_id, offset, n))
        messages = curs.fetchall()
        curs.close()
        return [Message(message).to_dict() for message in messages]
    
    def getCount(self):
        curs = self.conn.cursor()
        query = "SELECT COUNT(*) FROM conversation;"
        curs.execute(query)
        count = curs.fetchone()[0]
        curs.close()
        return count
         
    def insertMessage(self, is_bot, message):
        time = datetime.now()
        query = "INSERT INTO conversation (isBot, message, time) VALUES (%s, %s, %s);"
        
        try:
            cur = self.conn.cursor()
            cur.execute(query, (is_bot, message, time))
            self.conn.commit()
            cur.close()
            print("Message inserted successfully!")
            return True
        except Exception as e:
            print("Error inserting message:", e)
            self.conn.rollback()
            return False
    
    def clearTable(self):
        """Clear all data from the conversation table"""
        try:
            cur = self.conn.cursor()
            cur.execute("TRUNCATE conversation RESTART IDENTITY;")
            self.conn.commit()
            cur.close()
            print("Table cleared successfully")
            return True
        except Exception as e:
            print(f"Error clearing table: {e}")
            self.conn.rollback()
            return False