import unittest
from department import Department

class TestDepartment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Department.create_table()

    @classmethod
    def tearDownClass(cls):
        Department.drop_table()

    def setUp(self):
        '''Setup before each test'''
        # Clean up the table to ensure tests are isolated
        Department.drop_table()
        Department.create_table()

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "departments" if it does not exist.'''
        tables = Department.CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'").fetchall()
        assert tables == [('departments',)]

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "departments" if it exists.'''
        Department.create_table()
        Department.drop_table()
        result = Department.CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'").fetchone()
        assert result is None

    def test_saves_department(self):
        '''contains method "save()" that saves a Department instance to the db and assigns the instance an id.'''
        Department.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        assert department.id is not None
        assert department.name == "Payroll"
        assert department.location == "Building A, 5th Floor"

    def test_creates_department(self):
        '''contains method "create()" that creates a new row in the db using parameter data and returns a Department instance.'''
        Department.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        row = Department.CURSOR.execute("SELECT * FROM departments").fetchone()
        assert row is not None
        assert row[1] == "Payroll"
        assert row[2] == "Building A, 5th Floor"

    def test_updates_row(self):
        '''contains a method "update()" that updates an instance's corresponding db row to match its new attribute values.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        id1 = department1.id
        department2 = Department.create("Marketing", "Building B, 3rd Floor")
        department2.name = "Sales and Marketing"
        department2.location = "Building B, 4th Floor"
        department2.update()

        department = Department.find_by_id(id1)
        assert department.name == "Human Resources"
        assert department.location == "Building C, East Wing"

        department = Department.find_by_id(department2.id)
        assert department.name == "Sales and Marketing"
        assert department.location == "Building B, 4th Floor"

    def test_deletes_row(self):
        '''contains a method "delete()" that deletes the instance's corresponding db row'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        id1 = department1.id
        department2 = Department.create("Sales and Marketing", "Building B, 4th Floor")
        id2 = department2.id
        department2.delete()

        department = Department.find_by_id(id1)
        assert (department.id, department.name, department.location) == (id1, "Human Resources", "Building C, East Wing")
        assert Department.find_by_id(id2) is None

    def test_instance_from_db(self):
        '''contains method "instance_from_db()" that takes a table row and returns a Department instance.'''
        Department.create_table()
        Department.create("Payroll", "Building A, 5th Floor")
        row = Department.CURSOR.execute("SELECT * FROM departments").fetchone()
        department = Department.instance_from_db(row)
        assert department.name == "Payroll"
        assert department.location == "Building A, 5th Floor"

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Department instances for every row in the db.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")
        departments = Department.get_all()
        assert len(departments) == 2
        assert departments[0].name == "Human Resources"
        assert departments[1].name == "Marketing"

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Department instance corresponding to the db row retrieved by id.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")
        department = Department.find_by_id(department1.id)
        assert (department.id, department.name, department.location) == (department1.id, "Human Resources", "Building C, East Wing")

    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns a Department instance corresponding to the db row retrieved by name.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")
        department = Department.find_by_name("Human Resources")
        assert (department.id, department.name, department.location) == (department1.id, "Human Resources", "Building C, East Wing")

if __name__ == '__main__':
    unittest.main()
