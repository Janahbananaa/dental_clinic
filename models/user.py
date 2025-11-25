from typing import Optional

class User:
    def __init__(self, db, login_id: int = None, username: str = "", password: str = ""):
        self.db = db
        self.login_id = login_id
        self.username = username
        self.password = password
    
    def save(self) -> bool:
        if self.login_id:
            query = """UPDATE login SET username=%s, password=%s WHERE login_id=%s"""
            return self.db.execute_query(query, (self.username, self.password, self.login_id))
        else:
            query = """INSERT INTO login (username, password) VALUES (%s, %s)"""
            return self.db.execute_query(query, (self.username, self.password))
    
    @staticmethod
    def authenticate(db, username: str, password: str) -> Optional['User']:
        query = "SELECT * FROM login WHERE username=%s AND password=%s"
        result = db.fetch_one(query, (username, password))
        if result:
            return User(db, result['login_id'], result['username'], result['password'])
        return None
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM login"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(db, login_id: int) -> Optional['User']:
        query = "SELECT * FROM login WHERE login_id=%s"
        result = db.fetch_one(query, (login_id,))
        if result:
            return User(db, result['login_id'], result['username'], result['password'])
        return None
    
    def delete(self) -> bool:
        if self.login_id:
            query = "DELETE FROM login WHERE login_id=%s"
            return self.db.execute_query(query, (self.login_id,))
        return False
