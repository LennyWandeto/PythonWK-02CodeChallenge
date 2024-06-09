from database.setup import create_tables
from database.connection import get_db_connection

CONN = get_db_connection()
CURSOR = CONN.cursor()

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        CURSOR.execute('INSERT INTO author (name) VALUES (?)', (self.name,))
        CONN.commit()
    
    @property
    def id(self):
        CURSOR.execute('SELECT id FROM authors WHERE name =?', (self.name,))
        return CURSOR.fetchone()['id']
    
    @id.setter
    def id(self, id):
        if not isinstance(self.id, int):
            print("ID must be a integer")
        CURSOR.execute('UPDATE authors SET id =? WHERE name =?', (id, self.name))
        CONN.commit()
    
    @property
    def name(self):
        CURSOR.execute('SELECT name FROM authors WHERE id =?', (self.id,))
        return CURSOR.fetchone()['name']
    
    @name.setter
    def name(self, name):
        if not isinstance(self.name, str):
            print("Name must be a string")
        elif len(name) > 0:
            CURSOR.execute('UPDATE authors SET name =? WHERE id =?', (name, self.id))
            CONN.commit()
        else:
            print("Name must be more than 0")
    
    @property
    def articles(self):
        CURSOR.execute("""
            SELECT articles.title, articles.author_id
            FROM articles
            LEFT JOIN authors
            ON articles.author_id = author.id
        """)
        return CURSOR.fetchall()

    #Issue With Fetch here
    @property
    def magazines(self):
        CURSOR.execute("""
            SELECT magazines.name, articles.magazine_id
            FROM articles
            RIGHT JOIN magazines
            ON articles.magazine_id = magazines.id
                       
        """)
        return CURSOR.fetchall()


    def __repr__(self):
        return f'<Author {self.name}>'
