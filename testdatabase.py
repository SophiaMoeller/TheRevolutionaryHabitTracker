import sqlite3
from datetime import date


def get_db(name='main.db'):
    """
    calls database and creates tables within the specified database

    :param name: name of the sqlite3 database
    :return: creates tables within the sqlite3 database
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    creates tables for habits, users, and completion dates

    :param db: name of the sqlite3 database connection
    :return: creates a database with the three tables habits, users, and completion dates
    """
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS habit (
    habit_name VARCHAR(20) PRIMARY KEY,
    description TEXT NOT NULL, 
    periodicity VARCHAR(20) NOT NULL,
    habit_goal INT,
    habit_group VARCHAR(20), 
    creation_date DATE NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
    user_name VARCHAR(20) PRIMARY KEY 
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS completion_dates (
    habit_id INT PRIMARY KEY,
    habit_name VARCHAR(20) NOT NULL,
    date DATETIME,
    FOREIGN KEY (habit_name) REFERENCES habit(habit_name)
    )''')

    db.commit()


def add_habit(db, habit_name, description, periodicity, habit_goal, habit_group, creation_date):
    """
    adding a new habit with is corresponding attributes to the database

    :param db: name of the sqlite3 database connection
    :param habit_name: name of the habit that should be added to the database
    :param description: description of the habit that should be added to the database
    :param periodicity: periodicity of the habit that should be added to the database
    :param habit_goal: goal of the habit that should be added to the database
    :param habit_group: group of the habit that should be added to the database
    :param creation_date: creation date of the habit that should be added to the database
    :return: a table with the columns displayed above including the new entry of a habit
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habit VALUE(?,?,?,?,?)",
                (habit_name, description, periodicity, habit_goal, habit_group, creation_date))
    db.commit()


def increment_habit(db, habit_id, habit_name, event_date=None):
    """
    store the dates on which a habit was executed in the database

    :param db: name of the sqlite3 database connection
    :param habit_id: uniquely identifying number for a specific habit
    :param habit_name: name of the habit for which an additional completion date should be stored
    :param event_date: date the respective habit was executed
    :return: added date to the table completion dates
    """
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO completion_dates VALUES (?,?,?)", (event_date, habit_name, habit_id))
    db.commit()


def get_habit_data(db, name):
    """
    retrieve data related to a habit from the database based on the habit's name

    :param db: name of the sqlite3 database connection
    :param name: name of the habit
    :return: retrieves all the rows returned by the SQL query and returns them as a list of tuples
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit WHERE habit_name=?", (name,))
    habit_data = cur.fetchall()
    if not habit_data:
        return print("This habit does not exist")
    return habit_data


database_con = get_db()
create_tables(database_con)
curs = database_con.cursor()
res = curs.execute("SELECT * FROM habit")
print(res.fetchone())
