import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="ks",
        password="ks_pass",
        database="kickstarter"
    )
