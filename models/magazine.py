from database.setup import create_tables
from database.connection import get_db_connection
from models.author import Author

CONN = get_db_connection()
CURSOR = CONN.cursor()

class Magazine:
    def __init__(self, id, name, category=None):
        self.name = name
        self.category = category
        self.id = id
        CURSOR.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (name, category))
        CONN.commit()
    
    @property
    def id(self):
        CURSOR.execute('SELECT id FROM magazines WHERE name =?', (self.name,))
        return CURSOR.fetchone()['id']
    
    @id.setter
    def id(self, id):
        if not isinstance(self.id, int):
            print("ID must be a integer")
        CURSOR.execute('UPDATE magazines SET id =? WHERE name =?', (id, self.name))
        CONN.commit()
    
    @property
    def name(self):
        CURSOR.execute('SELECT name FROM magazines WHERE id =?', (self.id,))
        return CURSOR.fetchone()['name']
    
    @name.setter
    def name(self, name):
        if not isinstance(self.name, str):
            print("Name must be a string")
        elif 2<= len(self.name) <= 16:
            CURSOR.execute('UPDATE magazines SET name =? WHERE id =?', (name, self.id))
            CONN.commit()
        else:
            print("Name must be between 2 and 16 characters")
    
    @property
    def category(self):
        CURSOR.execute('SELECT category FROM magazines WHERE id =?', (self.id,))
        return CURSOR.fetchone()['category']
    
    @category.setter
    def category(self, category):
        if not isinstance(self.category, str):
            print("Category must be a string")
        elif len(self.category) > 0:
            CURSOR.execute('UPDATE magazines SET category =? WHERE id =?', (category, self.id))
            CONN.commit()
        else:
            print("Category must be more than 0")
    
    @property
    def articles(self):
        CURSOR.execute("""
            SELECT articles.title, articles.magazine_id
            FROM articles
            LEFT JOIN magazines
            ON articles.magazine_id = magazines.id
        """)
        return CURSOR.fetchall()
    
    @property
    def contributors(self):
        CURSOR.execute("""
            SELECT authors.name, articles.author_id
            FROM authors
            LEFT JOIN articles
            ON authors.id = articles.author_id
                       
        """)
        return CURSOR.fetchall()
    
    def article_titles(self):
        CURSOR.execute("""
            SELECT articles.title
            FROM articles
            LEFT JOIN magazines
            ON articles.magazine_id = magazines.id
        """)
        if CURSOR.fetchall() == []:
            return None
        else:
            return CURSOR.fetchall()
    
    def contributing_authors(self):
        CURSOR.execute("""
            SELECT authors.name
            FROM authors
            LEFT JOIN articles
            ON authors.id = articles.author_id           
        """)
        new = CURSOR.fetchall()
        if len(new) > 2:
            return None
        elif not isinstance(new, Author):
            raise TypeError("Article must be of type Author")
        else:
            return CURSOR.fetchall()

    def __repr__(self):
        return f'<Magazine {self.name}>'
