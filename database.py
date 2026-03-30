# import mysql.connector

# def connect_db():
#     try:
#         conn = mysql.connector.connect(
#             host="103.31.38.137",
#             user="userdb",
#             password="",
#             database="db_rab",
#         )
#         return conn
#     except mysql.connector.Error as e:
#         print(f"Error connecting to MySQL: {e}")
#         return None

import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_rab",
            port=3306
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
