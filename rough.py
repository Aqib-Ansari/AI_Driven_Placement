import sql_functions
import mysql
import mysql.connector
# quiz_questions = sql_functions.fetch_quiz_question("mysql")
# # print(len(quiz_questions))
# for i in range(len(quiz_questions)):
#     print(quiz_questions[i]["id"])
    
# mysql

def create_connection():
    connection_my = mysql.connector.connect(
        host = "database-1.cdhiotv5c9su.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "aidriven",
        database = "database-1"
    )
    return connection_my

create_connection()