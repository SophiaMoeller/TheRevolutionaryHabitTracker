import pytest
import sqlite3
from db import (create_tables, add_habit, increment_habit, get_date_for_habit, get_all_dates_for_habit, get_periodicity,
                get_all_habits, get_current_streak, update_current_streak, delete_habit_from_db, habit_exists)


@pytest.fixture
def db():
    """
    Connect to an in-memory SQLite database for testing

    :return: In-memory database connection
    """
    conn = sqlite3.connect(':memory:')
    create_tables(conn)
    yield conn
    conn.close()


def test_create_tables(db):
    # Call the function under test
    create_tables(db)

    # Check if the habit table is created
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habit';")
    assert cursor.fetchone() is not None

    # Check if the completion_dates table is created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='completion_dates';")
    assert cursor.fetchone() is not None

    # Check if the habit table has the expected columns
    cursor.execute("PRAGMA table_info(habit);")
    habit_columns = [row[1] for row in cursor.fetchall()]
    expected_habit_columns = ['habit_name', 'description', 'periodicity', 'habit_group', 'creation_date',
                              'current_streak', 'longest_streak']
    assert set(habit_columns) == set(expected_habit_columns)

    # Check if the completion_dates table has the expected columns
    cursor.execute("PRAGMA table_info(completion_dates);")
    completion_dates_columns = [row[1] for row in cursor.fetchall()]
    expected_completion_dates_columns = ['habit_name', 'event_date']
    assert set(completion_dates_columns) == set(expected_completion_dates_columns)


def test_add_habit(db):
    # Call the function under test
    habit_name = "Running"
    description = "Run 5km each day"
    periodicity = "Daily"
    habit_group = "Health"
    creation_date = "2024-01-01"
    current_streak = 0
    longest_streak = 0

    add_habit(db, habit_name, description, periodicity, habit_group, creation_date, current_streak, longest_streak)

    # Check if the habit is added to the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habit WHERE habit_name=?", (habit_name,))
    habit_entry = cursor.fetchone()
    assert habit_entry is not None

    # Check if the habit attributes match the provided values
    assert habit_entry[0] == habit_name
    assert habit_entry[1] == description
    assert habit_entry[2] == periodicity
    assert habit_entry[3] == habit_group
    assert habit_entry[4] == creation_date
    assert habit_entry[5] == current_streak
    assert habit_entry[6] == longest_streak


def test_add_existing_habit(db):
    # Add a habit to the database
    habit_name = "Running"
    description = "Run 5km each day"
    periodicity = "Daily"
    habit_group = "Health"
    creation_date = "2024-01-01"
    current_streak = 0
    longest_streak = 0

    add_habit(db, habit_name, description, periodicity, habit_group, creation_date, current_streak, longest_streak)

    # Call the function under test with an existing habit name
    with pytest.raises(Exception) as exception_info:
        add_habit(db, habit_name, description, periodicity, habit_group, creation_date, current_streak,
                  longest_streak)

    # Check if the correct exception is raised
    assert str(exception_info.value) == f"The habit with the name '{habit_name}' already exists."


def test_increment_habit(db):
    habit_name = "Running"
    event_date = "2024-03-16"

    # Call the increment_habit function
    increment_habit(db, habit_name, event_date)

    # Assert that the event date is stored in the database for the specified habit
    cur = db.cursor()
    cur.execute("SELECT * FROM completion_dates WHERE habit_name=? AND event_date=?", (habit_name, event_date))
    result = cur.fetchone()
    assert result is not None  # Assert that a row exists for the habit and event date


def test_get_date_for_habit(db):
    # Create a habit and add completion dates
    habit_name = "Running"
    completion_dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS completion_dates (
        habit_name VARCHAR(20),
        event_date DATE
        )''')
    for date in completion_dates:
        cursor.execute("INSERT INTO completion_dates VALUES (?, ?)", (habit_name, date))
    db.commit()

    # Call the function under test
    retrieved_dates = get_date_for_habit(db, habit_name)

    # Check if the retrieved dates match the expected dates
    assert retrieved_dates == completion_dates


def test_get_all_dates_for_habit(db):
    habit_name = "Running"
    event_dates = [("2024-01-01",), ("2024-01-05",), ("2024-01-10",)]

    # Create the completion_dates table
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS completion_dates (
                        habit_name VARCHAR(20),
                        event_date DATE,
                        FOREIGN KEY (habit_name) REFERENCES habit(habit_name)
                    )''')

    # Insert sample event dates
    for event_date in event_dates:
        cursor.execute("INSERT INTO completion_dates VALUES (?, ?)", (habit_name, event_date[0]))
    db.commit()

    # Call the function under test
    result = get_all_dates_for_habit(db, habit_name)

    # Adjust the format of event_dates to match the format of the result
    expected_result = [(habit_name, date[0]) for date in event_dates]

    # Check if the returned list matches the expected event dates
    assert result == expected_result


# following test applies similarly to function get_description, get_creation_date, get_habit_group, get_current_streak,
# get_longest_streak
def test_get_periodicity(db):
    habit_name = "Running"
    description = "Run 5km each day"
    periodicity = "Daily"
    habit_group = "Health"
    creation_date = "2024-01-01"
    current_streak = 0
    longest_streak = 0

    # Create the habit table
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS habit (
                            habit_name VARCHAR(20),
                            description TEXT,
                            periodicity VARCHAR(20),
                            habit_group VARCHAR(20),
                            creation_date DATE,
                            current_streak INTEGER,
                            longest_streak INTEGER
                        )''')

    # Insert a sample habit
    cursor.execute("INSERT INTO habit VALUES (?, ?, ?, ?, ?, ?, ?)", (habit_name, description,
                                                                      periodicity, habit_group, creation_date,
                                                                      current_streak, longest_streak))
    db.commit()

    # Call the function under test
    result = get_periodicity(db, habit_name)

    # Check if the returned periodicity matches the expected value
    assert result == periodicity


def test_get_periodicity_nonexistent_habit(db):
    habit_name = "NonExistentHabit"

    # Call the function under test for a non-existent habit
    result = get_periodicity(db, habit_name)

    # Check if the result is None
    assert result is None


def test_get_all_habits(db):
    # Create habit table
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS habit (
                        habit_name VARCHAR(20),
                        description TEXT,
                        periodicity VARCHAR(20),
                        habit_group VARCHAR(20),
                        creation_date DATE,
                        current_streak INTEGER,
                        longest_streak INTEGER
                    )''')

    # Insert sample habit data
    habit_data = [
        ("Running", "Run 5km each day", "Daily", "Health", "2024-01-01", 0, 0),
        ("Reading", "Read a book each week", "Weekly", "Personal Development", "2024-01-05", 0, 0),
        ("Meditation", "Meditate for 15 minutes daily", "Daily", "Mindfulness", "2024-01-10", 0, 0)
    ]
    cursor.executemany("INSERT INTO habit VALUES (?, ?, ?, ?, ?, ?, ?)", habit_data)

    # Call the function under test
    all_habits = get_all_habits(db)

    # Verify the returned data
    assert isinstance(all_habits, list)
    assert len(all_habits) == 3  # Assuming three sample habits were inserted

    # Verify the structure of each habit dictionary
    for habit in all_habits:
        assert isinstance(habit, dict)
        assert set(habit.keys()) == {"habit name", "habit description", "periodicity", "habit group", "creation date",
                                     "current streak", "longest streak"}


# the following test applies similarly to function update_longest_streak
def test_update_current_streak(db):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS habit (
                            habit_name VARCHAR(20),
                            description TEXT,
                            periodicity VARCHAR(20),
                            habit_group VARCHAR(20),
                            creation_date DATE,
                            current_streak INTEGER,
                            longest_streak INTEGER
                        )''')

    # Insert sample habit data
    habit_data = [
        ("Running", "Run 5km each day", "Daily", "Health", "2024-01-01", 0, 0),
        ("Reading", "Read a book each week", "Weekly", "Personal Development", "2024-01-05", 0, 0),
        ("Meditation", "Meditate for 15 minutes daily", "Daily", "Mindfulness", "2024-01-10", 0, 0)
    ]
    cursor.executemany("INSERT INTO habit VALUES (?, ?, ?, ?, ?, ?, ?)", habit_data)
    habit_name = "Running"
    current_streak = 5

    # Call the function under test
    update_current_streak(db, current_streak, habit_name)

    # Verify that the current streak of the habit in the database is updated correctly
    updated_current_streak = get_habit_current_streak(db, habit_name)
    assert updated_current_streak == current_streak


def get_habit_current_streak(db, habit_name):
    """
    Retrieves the current streak of a specific habit from the habit table in the database

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the current streak should be retrieved
    :return: Current streak of the habit or None if the habit does not exist
    """
    cur = db.cursor()
    cur.execute("SELECT current_streak FROM habit WHERE habit_name=?", (habit_name,))
    result = cur.fetchone()
    return result[0] if result is not None else None


def test_habit_exists_existing_habit(db):
    habit_name = "Running"
    description = "Run 5km each day"
    periodicity = "Daily"
    habit_group = "Health"
    creation_date = "2024-01-01"
    current_streak = 0
    longest_streak = 0

    add_habit(db, habit_name, description, periodicity, habit_group, creation_date, current_streak, longest_streak)
    exists = habit_exists(db, habit_name)

    # Verify that the function correctly identifies the existence of the habit
    assert exists is not None


def test_habit_exists_nonexistent_habit(db):
    # Define a habit that does not exist in the database
    habit_name = "NonExistentHabit"
    exists = habit_exists(db, habit_name)

    # Verify that the function correctly identifies the non-existence of the habit
    assert exists is None


def test_delete_habit_from_db_existing_habit(db):
    habit_name = "Running"
    description = "Run 5km each day"
    periodicity = "Daily"
    habit_group = "Health"
    creation_date = "2024-01-01"
    current_streak = 0
    longest_streak = 0

    add_habit(db, habit_name, description, periodicity, habit_group, creation_date, current_streak, longest_streak)
    exists = habit_exists(db, habit_name)

    # Call the function under test
    delete_habit_from_db(db, habit_name)

    # Verify that the habit and its associated completion dates are deleted
    assert not habit_exists(db, habit_name)


def test_delete_habit_from_db_nonexistent_habit(db):
    # Attempt to delete a habit that does not exist
    habit_name = "NonExistentHabit"

    # Call the function under test
    delete_habit_from_db(db, habit_name)

    # Verify that the function handles the case when the habit does not exist
    assert not habit_exists(db, habit_name)
