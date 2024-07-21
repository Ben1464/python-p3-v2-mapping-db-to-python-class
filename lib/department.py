import sqlite3

class Department:
    CONNECTION = sqlite3.connect(':memory:')  # Using an in-memory database for testing
    CURSOR = CONNECTION.cursor()

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        cls.CURSOR.execute(sql)
        cls.CONNECTION.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments"
        cls.CURSOR.execute(sql)
        cls.CONNECTION.commit()

    def save(self):
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            self.__class__.CURSOR.execute(sql, (self.name, self.location))
            self.id = self.__class__.CURSOR.lastrowid
        else:
            sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
            self.__class__.CURSOR.execute(sql, (self.name, self.location, self.id))
        self.__class__.CONNECTION.commit()

    @classmethod
    def create(cls, name, location):
        department = cls(id=None, name=name, location=location)
        department.save()
        return department

    def update(self):
        self.save()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?"
        self.__class__.CURSOR.execute(sql, (self.id,))
        self.__class__.CONNECTION.commit()
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        if row:
            return cls(id=row[0], name=row[1], location=row[2])
        return None

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = cls.CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = cls.CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = cls.CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row)
