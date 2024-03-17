import sqlite3
from datetime import date


def get_db(name='main.db'):
    """
    Initializes SQlite3 database connection

    :param name: Name of the SQlite3 database
    :return: Allows access to database
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Creates tables for habits and completion dates

    :param db: An initialized SQLite3 database connection
    :return: The tables habit and completion dates are created in the database
    """
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS habit (
    habit_name VARCHAR(20) PRIMARY KEY,
    description TEXT NOT NULL, 
    periodicity VARCHAR(20) NOT NULL,
    habit_group VARCHAR(20), 
    creation_date DATE NOT NULL,
    current_streak INT,
    longest_streak INT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS completion_dates (
    habit_name VARCHAR(20),
    event_date DATETIME,
    FOREIGN KEY (habit_name) REFERENCES habit(habit_name)
    )''')

    db.commit()


def add_habit(db, habit_name, description, periodicity, habit_group, creation_date, current_streak, longest_streak):
    """
    Adding a new habit with its corresponding attributes defined as in the class to the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit that should be added to the database
    :param description: Description of the habit that should be added to the database
    :param periodicity: Periodicity of the habit that should be added to the database
    :param habit_group: Group of the habit that should be added to the database
    :param creation_date: Creation date of the habit that should be added to the database
    :param longest_streak: Longest streak of the habit that should be added to the database
    :param current_streak: Current streak of the habit that should be added to the database
    :return: An entry with the columns displayed above for the new habit is added to the database
    """
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habit WHERE habit_name=?", (habit_name,))
    existing_habit = cur.fetchone()

    if existing_habit:
        raise Exception(f"The habit with the name '{habit_name}' already exists.")
    else:
        cur.execute("INSERT INTO habit VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (habit_name, description, periodicity, habit_group, creation_date, current_streak, longest_streak))
        db.commit()


def increment_habit(db, habit_name, event_date=None):
    """
    Store the dates on which a habit was executed in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which an additional completion date should be stored
    :param event_date: Date the respective habit was executed
    :return: Table completion dates is appended by respective date
    """
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO completion_dates VALUES (?,?)", (habit_name, event_date))
    db.commit()


def get_date_for_habit(db, habit_name):
    """
    Retrieves completion dates from the database based on the habit's name

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which date should be retrieved from the database
    :return: Retrieves all the rows returned by the SQL query and returns them as a list of tuples
    """
    cur = db.cursor()
    cur.execute("SELECT event_date FROM completion_dates WHERE habit_name=?", (habit_name,))
    completion_dates = [date[0] for date in cur.fetchall()]
    return completion_dates


def get_all_dates_for_habit(db, habit_name):
    """
    Retrieves the entire completion dates table from the database based on the habit's name

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which completion date table should be retrieved
    :return: Retrieves entire completion dates table by the SQL query and returns it as a list of tuples
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM completion_dates WHERE habit_name=?", (habit_name,))
    completion_dates = cur.fetchall()
    return completion_dates


def get_habit_data(db, habit_name):
    """
    Retrieves entire habit table from the database based on the habit's name

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which habit table should be retrieved
    :return: Retrieves entire habit table by the SQL query and returns them as a list of tuples
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit WHERE habit_name=?", (habit_name,))
    habit_data = cur.fetchall()
    print(habit_data)
    return habit_data


def get_periodicity(db, habit_name):
    """
    Retrieves the periodicity column of a certain habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which periodicity should be retrieved
    :return: Retrieves the first element as a list of tuples of the periodicity column and returns the specific value
    or None in the case the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habit WHERE habit_name=?", (habit_name,))
    habit_periodicity_row = cur.fetchone()
    if habit_periodicity_row:
        habit_periodicity = habit_periodicity_row[0]
        return habit_periodicity
    else:
        return None


def get_description(db, habit_name):
    """
    Retrieves the description column of a certain habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which description should be retrieved
    :return: Retrieves the first element as a list of tuples of the description column and returns the specific value
    or None in the case the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT description FROM habit WHERE habit_name=?", (habit_name,))
    habit_description_row = cur.fetchone()
    if habit_description_row:
        habit_description = habit_description_row[0]
        return habit_description
    else:
        return None


def get_habit_group(db, habit_name):
    """
    Retrieves the habit group column of a certain habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the habit group should be retrieved
    :return: Retrieves the first element as a list of tuples of the habit group column and returns the specific value
    or None in the case the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT habit_group FROM habit WHERE habit_name=?", (habit_name,))
    habit_group_row = cur.fetchone()
    if habit_group_row:
        habit_group = habit_group_row[0]
        return habit_group
    else:
        return None


def get_creation_date(db, habit_name):
    """
    Retrieves the creation date column of a certain habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the creation date should be retrieved
    :return: Retrieves the first element as a list of tuples of the creation date column and returns the specific value
    or None in the case the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT creation_date FROM habit WHERE habit_name=?", (habit_name,))
    creation_date_row = cur.fetchone()
    if creation_date_row:
        creation_date = creation_date_row[0]
        return creation_date
    else:
        return None


def get_current_streak(db, habit_name):
    """
    Retrieves the current streak column of a certain habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the current streak should be retrieved
    :return: Retrieves the first element as a list of tuples of the current streak column and returns the specific value
    or None in the case the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT current_streak FROM habit WHERE habit_name=?", (habit_name,))
    current_streak_row = cur.fetchone()
    if current_streak_row:
        current_streak = current_streak_row[0]
        return current_streak
    else:
        return None


def get_longest_streak(db, habit_name):
    """
    Retrieves the longest streak column of a certain habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the longest streak should be retrieved
    :return: Retrieves the first element as a list of tuples of the longest streak column and returns the specific value
    or None in the case the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT longest_streak FROM habit WHERE habit_name=?", (habit_name,))
    longest_streak_row = cur.fetchone()
    if longest_streak_row:
        longest_streak = longest_streak_row[0]
        return longest_streak
    else:
        return None


def get_all_habits(db):
    """
    Retrieves all data from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :return: Returns a list which contains dictionaries representing each habit record. Each dictionary has keys
    corresponding to the column names and values representing the habit data.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit")
    habits_data = cur.fetchall()
    columns = ["habit name", "habit description", "periodicity", "habit group", "creation date", "current streak",
               "longest streak"]

    all_habits = []
    for habit_data in habits_data:
        habit_dict = dict(zip(columns, habit_data))
        all_habits.append(habit_dict)

    return all_habits


def update_current_streak(db, current_streak, habit_name):
    """
    Updates the current streak of a specific habit in the database

    :param current_streak: Value of the current streak for a specific habit (Initial value is set to 0)
    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the current streak should be updated
    :return: Updated current streak column in the habit table of the database
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET current_streak = ? WHERE habit_name = ?", (current_streak, habit_name))
    db.commit()


def update_longest_streak(db, longest_streak, habit_name):
    """
    Updates the longest streak of a specific habit in the database

    :param longest_streak: Value of the longest streak for a specific habit (Initial value is set to 0)
    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the longest streak should be updated
    :return: Updated longest streak column in the habit table of the database
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET longest_streak = ? WHERE habit_name = ?", (longest_streak, habit_name))
    db.commit()


def delete_habit_from_db(db, habit_name):
    """
    Delete a habit and its associated completion dates from the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit that should be deleted
    :return: Habit and completion date tables are adjusted for the respective habit entries
    """
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habit WHERE habit_name=?", (habit_name,))
    existing_habit = cur.fetchone()
    if not existing_habit:
        print(f"This habit ({habit_name}) does not exist.")
        return
    else:
        cur.execute("DELETE FROM habit WHERE habit_name=?", (habit_name,))
        cur.execute("DELETE FROM completion_dates WHERE habit_name=?", (habit_name,))
        db.commit()
        print(f"The habit '{habit_name}' and its associated completion dates have been deleted.")


def habit_exists(db, habit_name):
    """
    Checks if a habit exists in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit to check
    :return: True if the habit exists, False otherwise
    """
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habit WHERE habit_name = ?", (habit_name,))
    habit_in_table = cur.fetchone()
    return habit_in_table
