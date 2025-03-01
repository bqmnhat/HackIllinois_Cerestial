import psycopg2
from datetime import datetime
import os

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
    def __init__(self):
        self.conn = psycopg2.connect(database="mydatabase", user="myuser", password="mypassword", host='db', port=5432)
        
    def findLastMessage(self, n):
        curs = self.conn.cursor()
        query = "SELECT * FROM (SELECT * FROM CONVERSATION ORDER BY %s DESC LIMIT 10) sub ORDER BY id ASC;"
        curs.execute(query, (n))
        messages = curs.fetchall()
        curs.close()
        return [Message(message).to_dict() for message in messages]
        
    def insertMessage(self, is_bot, message):
        time = datetime.now()  

        query = "INSERT INTO CONVERSATION (isBot, message, time) VALUES (%s, %s, %s);"

        try:
            cur = self.conn.cursor()
            cur.execute(query, (is_bot, message, time))
            self.conn.commit()

            cur.close()
            print("Message inserted successfully!")

        except Exception as e:
            print("Error inserting message:", e)