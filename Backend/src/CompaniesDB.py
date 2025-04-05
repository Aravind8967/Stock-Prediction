from flask import json
import mysql
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class CompaniesDB:
    def __init__(self):
        self.connection = self.dbConnection()

    def dbConnection(self):
        try:
            db_connection = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASSWORD,
                database = DB_NAME,
                port = DB_PORT
            )
            status = 200
            return {'connection':db_connection, 'status':status}
        except:
            status = 404
            return {'status':status, 'data':'database connection error'}

    def searchName(self, c_symbol):
        if self.connection['status'] == 200:
            connection = self.connection['connection']
            q = 'SELECT * FROM companies WHERE c_symbol = %s'
            cursor = connection.cursor(dictionary = True)
            cursor.execute(q, (c_symbol,))
            data = cursor.fetchall()
            if len(data) == 0:
                return {'status':404, 'data':'company not found'}
            else:
                return {'status':200, 'data':data}
        else:
            return {"status":404, "data":'database connection error'}

    def searchID(self, c_id):
        if self.connection['status'] == 200:
            connection = self.connection['connection']
            q = 'SELECT * FROM companies WHERE c_id = %s'
            cursor = connection.cursor(dictionary = True)
            cursor.execute(q, (c_id,))
            data = cursor.fetchall()
            if len(data) == 0:
                return {'status':404, 'data':'company not found'}
            else:
                return {'status':200, 'data':data}
        else:
            return {"status":404, "data":'database connection error'}

    def searchName(self, c_name):
        if self.connection['status'] == 200:
            connection = self.connection['connection']
            q = 'SELECT * FROM companies WHERE c_name = %s'
            cursor = connection.cursor(dictionary = True)
            cursor.execute(q, (c_name,))
            data = cursor.fetchall()
            if len(data) == 0:
                return {'status':404, 'data':'company not found'}
            else:
                return {'status':200, 'data':data}
        else:
            return {"status":404, "data":'database connection error'}

    def getNameSuggestions(self, query):
        if self.connection['status'] == 200:
            connection = self.connection['connection']
            q = 'SELECT c_name FROM companies WHERE c_name LIKE %s OR c_symbol LIKE %s LIMIT 5'
            cursor = connection.cursor(dictionary = True)
            cursor.execute(q, (f'%{query}%', f'%{query}%'))
            data = cursor.fetchall()
            suggestions = [item['c_name'] for item in data]
            return suggestions
        else:
            return []
        
        
if __name__ == '__main__':
    db = CompaniesDB()
    # print(DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, DB_HOST)
    itc = db.searchName('ITC Limited')
    print(itc)