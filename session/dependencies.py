from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

import uuid

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
        
    def add_user(self, username, password):
        # check user existence
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM user 
        WHERE username = %s;
        """, (username,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
        # user existed - return msg 
        if result:
            cursor.close()
            return "User existed. Please Log In."
        
        # user doesn't exist - register new user, return msg 
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO user (id, username, password)
            VALUES (%s, %s, %s);
            """, (generateUUID, username, password))
            cursor.close()
            self.connection.commit()
            return "New user successfully registered!"
    
    # get user for login
    def get_user(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM user 
        WHERE username = %s AND password = %s;
        """, (username, password))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
        cursor.close()
        return result
    
    def add_news (self, title, content, image):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news
        WHERE title = %s;
        """, (title, ))
        
        for row in cursor.fetchall():
            result.append({
                'title': row['title'],
                'content': row['content'],
                'image': row['image']
            })
        if result:
            cursor.close()
            return "News existed. Please enter a different title."
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO news (id, title, content, image)
            VALUES (%s, %s, %s, %s);
            """, (generateUUID, title, content, image))
            cursor.close()
            self.connection.commit()
            return "News successfully added!"
            
    def edit_news (self, title, content, image):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news
        WHERE title = %s;               
        """, (title,))
        for row in cursor.fetchall():
            result.append({
                'title' : row['title'],
                'content' : row['content'],
                'image' : row['image']
            })
        if result:
            cursor.execute("""
            UPDATE news 
            SET content=%s, image= %s 
            WHERE title= %s
            """, (content, image, title))
            cursor.close()
            self.connection.commit()
            return "News successfully updated."
        else:
            cursor.close()
            return "News does not exist, nothing is updated."
            
    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news;
        """)
        for row in cursor.fetchall():
            result.append({
                'title' : row['title'],
                'content' : row['content'],
                'image' : row['image']
            })
        cursor.close() 
        if result:    
            return result
        else:
            return "There are no news."
        
    def get_news_by_id(self, uuid):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news
        WHERE id = %s;
        """, (uuid, ))
        for row in cursor.fetchall():
            result.append({
                'title' : row['title'],
                'content' : row['content'],
                'image' : row['image']
            })
        cursor.close() 
        if result:    
            return result
        else:
            return "No news matches this ID."
        
    def delete_news(self, uuid):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news
        WHERE id = %s;
        """, (uuid, ))
        for row in cursor.fetchall():
            result.append({
                'title' : row['title'],
                'content' : row['content'],
                'image' : row['image']
            })
        if result:
            cursor.execute("""
            DELETE FROM news
            WHERE id = %s;
            """, (uuid, ))
            cursor.close()
            self.connection.commit()
            return "News successfully deleted."
        else:
            cursor.close()
            return "No news matches this ID."
        
    def download_file_by_id (self, uuid):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news
        WHERE id = %s;
        """, (uuid,))
        for row in cursor.fetchall():
            result.append({
                'title' : row['title'],
                'content' : row['content'],
                'image' : row['image']
            })
        cursor.close()
        if result:
            return result
        else:
            return "No news matches this ID."         
        
class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='soa',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())