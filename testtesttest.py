import sqlite3
from datetime import datetime
from db import (get_periodicity, get_habit_group, get_description, get_creation_date)


def get_periodicity(habit_name):
    """
    retrieves the periodicity column of a certain habit

    :param db: name of the sqlite3 database connection
    :param habit_name: name of the habit
    """
    db = sqlite3.connect("main.db")
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habit WHERE habit_name=?", (habit_name,))
    habit_periodicity = cur.fetchone()
    print(habit_periodicity)
    return habit_periodicity


print(get_periodicity("Laufen"))


def get_date_for_habit(habit_name):
    """
    retrieves event date from the database based on the habit's name

    :param db: name of the sqlite3 database connection
    :param habit_name: name of the habit
    :return: retrieves all the rows returned by the SQL query and returns them as a list of tuples
    """
    db = sqlite3.connect("main.db")
    cur = db.cursor()
    cur.execute("SELECT event_date FROM completion_dates WHERE habit_name=?", (habit_name,))
    completion_dates = cur.fetchall()
    return completion_dates


print(get_date_for_habit("Laufen"))


class Habit:

    def __init__(self, habit_name: str, habit_description: str, periodicity: str, creation_date, habit_group: str):
        self.habit_name = habit_name
        self.habit_description = habit_description
        self.periodicity = periodicity  # daily, weekly, or monthly
        self.creation_date = creation_date  # creation date of the habit
        self.completion_dates = []  # list to store completion dates
        self.habit_group = habit_group  # allocate habits to different groups
        self.track_count = 0  # counts the fulfillment of the habit according to it's periodicity
        self.longest_streak = 0  # displays the longest streak depending on the chosen periodicity

    def complete_habit(self):
        self.completion_dates.append(datetime.today())

habit_name = "Laufen"
db = sqlite3.connect("main.db")
desc = get_description(db, habit_name)
periodicity = get_periodicity(db, habit_name)
creation_date = get_creation_date(db, habit_name)
habit_group = get_habit_group(db, habit_name)
chosen_habit = Habit(habit_name, desc, periodicity, creation_date, habit_group)
chosen_habit.complete_habit()
print(Habit.completion_dates)


