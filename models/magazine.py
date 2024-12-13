class Magazine:
    def __init__(self, id, name, category="General"):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @staticmethod
    def get_magazine_by_id(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Magazine WHERE id = ?
        ''', (magazine_id,))
        magazine_row = cursor.fetchone()
        conn.close()
        if magazine_row:
            return Magazine(magazine_row['id'], magazine_row['name'], magazine_row['category'])
        return None

    def update_magazine(self, new_name, new_category):
        self.name = new_name
        self.category = new_category
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Magazine SET name = ?, category = ? WHERE id = ?
        ''', (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_magazine(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Magazine WHERE id = ?
        ''', (magazine_id,))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Article WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT Author.* FROM Author
            JOIN Article ON Author.id = Article.author_id
            WHERE Article.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM Article WHERE magazine_id = ?
        ''', (self.id,))
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Author.*, COUNT(Article.id) as article_count FROM Author
            JOIN Article ON Author.id = Article.author_id
            WHERE Article.magazine_id = ?
            GROUP BY Author.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = [Author(row['id'], row['name']) for row in cursor.fetchall()]
        conn.close()
        return authors if authors else None
