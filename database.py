from flask import g
import bcrypt
import sqlite3

class Database:
    def __init__(self, path="development.db"):
        self.dbpath = path
        self.conn = sqlite3.connect(self.dbpath)
        self.check_tables()

    def close(self):
        self.conn.close()

    def check_tables(self):
        cur = self.conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY ASC, username TEXT, email TEXT, password TEXT, admin BOOLEAN)")
        cur.execute("CREATE TABLE IF NOT EXISTS devices (id INTEGER PRIMARY KEY ASC, ip TEXT, public_key TEXT, private_key TEXT, cores INTEGER, ram INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY ASC, name TEXT, program TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS assignments (project INTEGER, device INTEGER, count INTEGER)")

        self.conn.commit()

    def has_users(self):
        cur = self.conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]

        return count > 0

    def get_user(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        return cur.fetchone()

    def get_email(self, email):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        return cur.fetchone()

    def register(self, username, email, password):
        if self.get_user(username):
            return False, "That user name has already been used in this instance."

        if self.get_email(email):
            return False, "That email has already been used in this instance."

        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        cur = self.conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed))
        self.conn.commit()

        return True, ""

    def login(self, username, password):
        user = self.get_user(username)

        if not user:
            return False, "Unable to find those credentials."

        if not bcrypt.hashpw(password.encode('utf8'), user[3].encode('utf8')) == user[3].encode('utf8'):
            return False, "Unable to find those credentials."

        return True, user[4]

def get_db():
    if not hasattr(g, 'dbref'):
         g.dbref = Database()

    return g.dbref

def close_db():
    if hasattr(g, 'dbref'):
        g.dbref.close()
        g.dbref = None
