import os
import mysql.connector as conn
import dotenv

dotenv.load_dotenv()

def get_connection():
    connection=conn.connect(
    host='localhost',
    user='root',
    password=os.getenv("Password"),
    database='online_delivery_db'
)
    return connection


