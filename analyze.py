from db import (get_date_for_habit, get_all_habits, get_periodicity, get_all_dates_for_habit)
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import questionary


def calculate_current_streak(db, habit_name):
    """
    Calculate the length of the current streak

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the length of the current streak should be calculated
    :return: Length of the current streak
    """
    completion_dates = get_date_for_habit(db, habit_name)
    completion_dates.reverse()
    periodicity = get_periodicity(db, habit_name)
    print(periodicity)
    current_streak = 0

    for i in range(len(completion_dates) - 1):
        if periodicity == 'Daily':
            date1 = datetime.strptime(completion_dates[i], '%Y-%m-%d')
            print(date1)
            date2 = datetime.strptime(completion_dates[i + 1], '%Y-%m-%d')
            print(date2)
            delta = timedelta(days=1)
            print(delta)
            if date2 - date1 == delta:
                current_streak += 1
                print(current_streak)
            else:
                current_streak = 0
                print('The current streak has been reset')
        elif periodicity == 'Weekly':
            date1 = datetime.strptime(completion_dates[i], '%Y-%m-%d')
            print(date1)
            date2 = datetime.strptime(completion_dates[i + 1], '%Y-%m-%d')
            print(date2)
            delta = timedelta(weeks=1)
            print(delta)
            if date2 - date1 == delta:
                current_streak += 1
                print(current_streak)
            else:
                current_streak = 0
                print('The current streak has been reset')
        elif periodicity == 'Monthly':
            date1 = datetime.strptime(completion_dates[i], '%Y-%m-%d')
            print(date1)
            date2 = datetime.strptime(completion_dates[i + 1], '%Y-%m-%d')
            print(date2)
            delta = timedelta(days=30)
            print(delta)
            if date2 - date1 == delta:
                current_streak += 1
                print(current_streak)
            else:
                current_streak = 0
                print('The current streak has been reset')
    return current_streak


def calculate_longest_streak(db, habit_name):
    """
    Calculate the length of the longest streak

    :param db: An initialized SQLite3 database connection
    :param habit_name: Name of the habit for which the longest streak should be calculated
    :return: Length of the longest streak since tracking the habit
    """
    completion_dates = get_date_for_habit(db, habit_name)
    completion_dates.reverse()
    periodicity = get_periodicity(db, habit_name)
    print(periodicity)
    longest_streak = 0
    current_streak = 0

    for i in range(len(completion_dates) - 1):
        date1 = datetime.strptime(completion_dates[i], '%Y-%m-%d')
        print(date1)
        date2 = datetime.strptime(completion_dates[i + 1], '%Y-%m-%d')
        print(date2)

        if periodicity == 'Daily':
            delta = timedelta(days=1)
            print(delta)
        elif periodicity == 'Weekly':
            delta = timedelta(weeks=1)
        elif periodicity == 'Monthly':
            delta = timedelta(days=30)

        if date2 - date1 == delta:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0

    return longest_streak


def table_all_habits(db):
    """
    Returns a table including all habits and the information stored with the habits

    :param db: An initialized SQLite3 database connection
    :return: Table of all habits
    """
    all_habits_data = get_all_habits(db)
    if not all_habits_data:
        print("No habits found.")
    else:
        df = pd.DataFrame(all_habits_data)
        print(tabulate(df, headers='keys', tablefmt='psql'))


def table_sorted_alphabet(db):
    """
    Returns a table including all habits and the information stored with the habits sorted by alphabet

    :param db: An initialized SQLite3 database connection
    :return: Table of all habits sorted by alphabet
    """
    all_habits_data = get_all_habits(db)
    if not all_habits_data:
        print("No habits found.")
    else:
        df = pd.DataFrame(all_habits_data)
        df_sorted = df.sort_values(by='habit name')
        print(tabulate(df_sorted, headers='keys', tablefmt='psql'))


def table_sorted_periodicity(db):
    """
    Returns a table including all habits and the information stored with the habits sorted by periodicity

    :param db: An initialized SQLite3 database connection
    :return: Table of all habits sorted by periodicity
    """
    all_habits_data = get_all_habits(db)
    if not all_habits_data:
        print("No habits found.")
    else:
        df = pd.DataFrame(all_habits_data)
        df_sorted = df.sort_values(by='periodicity')
        print(tabulate(df_sorted, headers='keys', tablefmt='psql'))


def table_sorted_current_streak(db):
    """
    Returns a table including all habits and the information stored with the habits sorted by current streak

    :param db: An initialized SQLite3 database connection
    :return: Table of all habits sorted by current streak
    """
    all_habits_data = get_all_habits(db)
    if not all_habits_data:
        print("No habits found.")
    else:
        df = pd.DataFrame(all_habits_data)
        df_sorted = df.sort_values(by='current streak')
        print(tabulate(df_sorted, headers='keys', tablefmt='psql'))


def table_sorted_longest_streak(db):
    """
    Returns a table including all habits and the information stored with the habits sorted by longest streak

    :param db: An initialized SQlite3 database connection
    :return: Table of all habits sorted by longest streak
    """
    all_habits_data = get_all_habits(db)
    if not all_habits_data:
        print("No habits found.")
    else:
        df = pd.DataFrame(all_habits_data)
        df_sorted = df.sort_values(by='longest streak')
        print(tabulate(df_sorted, headers='keys', tablefmt='psql'))


def table_completion_dates(db, habit_name):
    """
    Returns a table including all completion dates for a specific habit

    :param habit_name: Name of the habit for which completion dates should be retrieved
    :param db: An initialized SQlite3 database connection
    :return: Table of all completion dates for a specific habit
    """
    completion_dates = get_all_dates_for_habit(db, habit_name)
    if not completion_dates:
        print("There are currently no completion dates for this habit.")
    else:
        df = pd.DataFrame(completion_dates)
        df.rename(columns={0: 'habit name', 1: 'completion date'}, inplace=True)
        print(tabulate(df, headers='keys', tablefmt='psql'))


def display_habit_by_periodicity(db):
    """
    Displays a list of habits with the same periodicity

    :param db: An initialized SQlite3 database connection
    :return: Returns a statement including the habit name, the current streak, and the longest streak for all habits
    with the same periodicity
    """
    chosen_periodicity = questionary.select("For which periodicity do you want to display your habits?",
                                            choices=["Daily", "Weekly", "Monthly"]
                                            ).ask()
    user_habits = get_all_habits(db)
    filtered_habits = [habit for habit in user_habits if habit["periodicity"] == chosen_periodicity]
    if not user_habits:
        print("There are no existing habits.")
    else:
        print(f"Habits with {chosen_periodicity} periodicity:")
        for habit in filtered_habits:
            print(f"Name: {habit['habit name']}, Current Streak: {habit['current streak']}, "
                  f"Longest Streak: {habit['longest streak']}")


def display_habit_by_group(db):
    """
    Displays a list of habits within the same group

    :param db: An initialized SQlite3 database connection
    :return: Returns a statement including the habit name, the current streak, and the longest streak for all habits
    with the same group
    """
    chosen_group = questionary.select("Which group does your habit belong to?",
                                      choices=["Health", "Education", "Food", "Sports", "Living"]
                                      ).ask()
    user_habits = get_all_habits(db)
    filtered_habits = [habit for habit in user_habits if habit["habit group"] == chosen_group]
    if not user_habits:
        print("There are no existing habits.")
    else:
        print(f"Habits with {chosen_group} group:")
        for habit in filtered_habits:
            print(f"Name: {habit['habit name']}, Current Streak: {habit['current streak']},"
                  f"Longest Streak: {habit['longest streak']}")


def habit_with_longest_current_streak(db):
    """
    Display the habit with the longest current streak among all habits

    :param db: An initialized SQlite3 database connection
    :return: Returns a statement including the habit name and the current streak for the habit with the
    longest current streak
    """
    habit_list = get_all_habits(db)
    if not habit_list:
        print("No habits found.")
    else:
        habit_with_max_current_streak = max(habit_list, key=lambda habit: habit['current streak'])
        print(
            f"Habit with the longest current streak ({habit_with_max_current_streak['current streak']}): "
            f"{habit_with_max_current_streak['habit name']}")


def habit_with_longest_streak(db):
    """
    Display the habit with the longest streak among all habits

    :param db: An initialized SQlite3 database connection
    :return: Returns a statement including the habit name and the longest streak for the habit with the
    longest streak
    """
    habit_list = get_all_habits(db)
    if not habit_list:
        print("No habits found.")
    else:
        habit_with_max_longest_streak = max(habit_list, key=lambda habit: habit['longest streak'])
        print(
            f"Habit with the longest streak ({habit_with_max_longest_streak['longest streak']}): "
            f"{habit_with_max_longest_streak['habit name']}")
