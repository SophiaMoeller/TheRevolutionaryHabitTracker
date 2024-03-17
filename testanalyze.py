import pytest
import sqlite3
import pandas as pd
from tabulate import tabulate
from unittest.mock import patch
from analyze import (calculate_current_streak, calculate_longest_streak, table_sorted_alphabet, table_completion_dates,
                     habit_with_longest_current_streak)


@pytest.fixture
def db():
    """
    Connect to an in-memory SQLite database for testing

    :return: In-memory database connection
    """
    db = sqlite3.connect(':memory:')
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


# Mock functions for get_date_for_habit and get_periodicity
def mock_habit_data(db, habit_name):
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


def mock_get_date_for_habit(db, habit_name):
    # Return a list of completion dates for testing
    return ["2024-01-06", "2024-01-05", "2024-01-04", "2024-01-02", "2024-01-01"]


def mock_get_periodicity(db, habit_name):
    # Return the periodicity for testing
    return "Daily"


# Test cases
def test_calculate_current_streak_daily(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr("analyze.get_date_for_habit", mock_get_date_for_habit)
        m.setattr("analyze.get_periodicity", mock_get_periodicity)

        streak = calculate_current_streak(db, "Running")

        assert streak == 2


def test_calculate_current_streak_weekly(monkeypatch):
    with monkeypatch.context() as m:
        # Mock get_date_for_habit to return completion dates for testing
        def mock_get_date_for_habit_weekly(db, habit_name):
            return ["2024-01-29", "2024-01-22", "2024-01-15", "2024-01-08", "2024-01-01"]

        # Mock get_periodicity to return the periodicity for testing
        def mock_get_periodicity_weekly(db, habit_name):
            return "Weekly"

        m.setattr("analyze.get_date_for_habit", mock_get_date_for_habit_weekly)
        m.setattr("analyze.get_periodicity", mock_get_periodicity_weekly)

        streak = calculate_current_streak(db, "Running")

        assert streak == 4


def test_calculate_current_streak_monthly(monkeypatch):
    with monkeypatch.context() as m:
        # Mock get_date_for_habit to return completion dates for testing
        def mock_get_date_for_habit_monthly(db, habit_name):
            return ["2024-07-31", "2024-07-01", "2024-03-01", "2024-02-01", "2024-01-01"]

        # Mock get_periodicity to return the periodicity for testing
        def mock_get_periodicity_monthly(db, habit_name):
            return "Monthly"

        m.setattr("analyze.get_date_for_habit", mock_get_date_for_habit_monthly)
        m.setattr("analyze.get_periodicity", mock_get_periodicity_monthly)

        streak = calculate_current_streak(db, "Reading")

        assert streak == 1


def mock_get_date_for_habit_ls(db, habit_name):
    # Return a list of completion dates for testing
    return ["2024-01-12", "2024-01-11", "2024-01-10", "2024-01-06", "2024-01-05", "2024-01-04", "2024-01-03",
            "2024-01-02", "2024-01-01"]


def mock_get_periodicity_ls(db, habit_name):
    # Return the periodicity for testing
    return "Daily"


# Test cases
def test_calculate_longest_streak_daily(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr("analyze.get_date_for_habit", mock_get_date_for_habit_ls)
        m.setattr("analyze.get_periodicity", mock_get_periodicity_ls)

        streak = calculate_longest_streak(db, "Running")

        assert streak == 5


def test_calculate_longest_streak_weekly(monkeypatch):
    with monkeypatch.context() as m:
        # Mock get_date_for_habit to return completion dates for testing
        def mock_get_date_for_habit_weekly(db, habit_name):
            return ["2024-01-29", "2024-01-22", "2024-01-15", "2024-01-08", "2024-01-01"]

        # Mock get_periodicity to return the periodicity for testing
        def mock_get_periodicity_weekly(db, habit_name):
            return "Weekly"

        m.setattr("analyze.get_date_for_habit", mock_get_date_for_habit_weekly)
        m.setattr("analyze.get_periodicity", mock_get_periodicity_weekly)

        streak = calculate_longest_streak(db, "Running")

        assert streak == 4


def test_calculate_longest_streak_monthly(monkeypatch):
    with monkeypatch.context() as m:
        # Mock get_date_for_habit to return completion dates for testing
        def mock_get_date_for_habit_monthly(db, habit_name):
            return ["2024-07-31", "2024-07-01", "2024-06-01", "2024-02-01", "2024-01-01"]

        # Mock get_periodicity to return the periodicity for testing
        def mock_get_periodicity_monthly(db, habit_name):
            return "Monthly"

        m.setattr("analyze.get_date_for_habit", mock_get_date_for_habit_monthly)
        m.setattr("analyze.get_periodicity", mock_get_periodicity_monthly)

        streak = calculate_longest_streak(db, "Reading")

        assert streak == 2


# the following test applies similarly to function table_sorted_periodicity, table_sorted_current_streak,
# table_sorted_longest_streak
def test_table_sorted_alphabet(monkeypatch, capsys):
    habit_data = [
        {"habit name": "Reading", "habit description": "Read 30 minutes daily", "periodicity": "Daily",
         "habit group": "Personal Development", "creation date": "2023-01-01", "current streak": 5,
         "longest streak": 7},
        {"habit name": "Running", "habit description": "Run 5km each day", "periodicity": "Daily",
         "habit group": "Fitness", "creation date": "2023-02-01", "current streak": 3, "longest streak": 4},
        {"habit name": "Coding", "habit description": "Code for an hour daily", "periodicity": "Daily",
         "habit group": "Professional Development", "creation date": "2023-03-01", "current streak": 10,
         "longest streak": 15}
    ]

    def mock_get_all_habits(db):
        return habit_data

    monkeypatch.setattr("analyze.get_all_habits", mock_get_all_habits)

    table_sorted_alphabet(db)

    captured = capsys.readouterr()
    printed_table = captured.out

    expected_output = tabulate(pd.DataFrame(habit_data).sort_values(by='habit name'), headers='keys', tablefmt='psql')

    assert printed_table.strip() == expected_output.strip()


def test_table_completion_dates(monkeypatch, capsys):
    habit_name = "Reading"
    completion_dates_data = [
        (habit_name, "2023-01-01"),
        (habit_name, "2023-01-05"),
        (habit_name, "2023-01-10")
    ]

    def mock_get_all_dates_for_habit(db, habit_name):
        return completion_dates_data

    monkeypatch.setattr("analyze.get_all_dates_for_habit", mock_get_all_dates_for_habit)

    table_completion_dates(db, habit_name)

    captured = capsys.readouterr()
    printed_table = captured.out

    expected_df = pd.DataFrame(completion_dates_data, columns=['habit name', 'completion date'])

    expected_output = tabulate(expected_df, headers='keys', tablefmt='psql')

    assert printed_table.strip() == expected_output.strip()


# the following test applies similarly to function habit_with_longest_streak
def test_habit_with_longest_current_streak(capsys):
    habit_data = [
        {"habit name": "Reading", "current streak": 5},
        {"habit name": "Running", "current streak": 3},
        {"habit name": "Coding", "current streak": 10},
        {"habit name": "Meditation", "current streak": 7}
    ]

    with patch("analyze.get_all_habits", return_value=habit_data):
        habit_with_longest_current_streak(None)

    captured = capsys.readouterr()

    assert "Habit with the longest current streak (10): Coding" in captured.out
