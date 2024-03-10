from db import add_habit
from datetime import datetime


class Habit:

    def __init__(self, habit_name: str, habit_description: str, periodicity: str, habit_group: str, creation_date,
                 current_streak: int, longest_streak: int):
        self.habit_name = habit_name
        self.habit_description = habit_description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_dates = []
        self.habit_group = habit_group
        self.current_streak = current_streak
        self.longest_streak = longest_streak

    pass

    def store_habit(self, db):
        """
        Allows the storage of habit data in the database

        :param db: An initialized SQLite3 database connection
        :return: Stores the habit with its defined class attributes in the database
        """
        add_habit(db, self.habit_name, self.habit_description, self.periodicity, self.habit_group, self.creation_date,
                  self.current_streak, self.longest_streak)

    def complete_habit(self):
        """
        Appends the list of completion date by current date as the user completes a habit

        :param self: Calls the respective habit instance
        """
        self.completion_dates.append(datetime.today())
