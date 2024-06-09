from database.setup import create_tables
from database.connection import get_db_connection

CONN = get_db_connection()
CURSOR = CONN.cursor()

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        CURSOR.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?,?,?,?)',
                       (self.title, self.content, self.author_id, self.magazine_id))
        CONN.commit()
    
    @property
    def title(self):
        CURSOR.execute('SELECT title FROM articles WHERE id =?', (self.id,))
        return CURSOR.fetchone()['title']
    
    @title.setter
    def title(self, title):
        if not isinstance(self.title, str):
            print("Title must be a string")
        elif 5<=len(self.title) <=50:
            CURSOR.execute('UPDATE articles SET title =? WHERE id =?', (title, self.id))
            CONN.commit()
        else:
            print("Title must be between 5 and 50 characters.")
    
    @property
    def author(self):
        CURSOR.execute("""
            SELECT author.name, articles.content, articles.author_id
            FROM articles
            RIGHT JOIN authors
            ON articles.author_id = author.id
                       
        """)
        return CURSOR.fetchone()['name']
    
    @property
    def magazine(self):
        CURSOR.execute("""
            SELECT magazines.name, article.magazine_id
            FROM articles
            RIGHT JOIN magazines
            ON articles.magazine_id = magazines.id
                       
        """)
        return CURSOR.fetchone()['name']



    def __repr__(self):
        return f'<Article {self.title}>'
