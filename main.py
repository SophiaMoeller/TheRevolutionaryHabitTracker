from datetime import datetime
from time import sleep

import questionary
from db import (get_db, delete_habit_from_db, increment_habit, get_all_habits,
                get_periodicity, get_habit_group, get_description, get_creation_date, get_current_streak,
                get_longest_streak, update_current_streak, update_longest_streak, habit_exists)
from habittracker import Habit
from analyze import (calculate_current_streak, calculate_longest_streak, table_all_habits, table_sorted_periodicity,
                     table_sorted_alphabet, table_sorted_current_streak, table_sorted_longest_streak,
                     display_habit_by_periodicity, display_habit_by_group,
                     habit_with_longest_current_streak, habit_with_longest_streak, table_completion_dates)


def cli():
    """
    Command-line interface function that allows the user the interaction with the habit tracker program
    """
    db = get_db()
    print("Welcome to the revolutionary habit tracker")

    stop = False
    while not stop:
        choice_action = questionary.select(
            "What do you want to do?",
            choices=["Create a new habit", "Increment habit", "Analyze habit", "Delete a habit", "Exit program"]
        ).ask()

        if choice_action == 'Create a new habit':
            name = questionary.text("What is the name of the habit you want to create?").ask()
            desc = questionary.text("Please give a brief description of your habit.").ask()
            periodicity = questionary.select("What is the rhythm in which you want to execute your habit?",
                                             choices=["Daily", "Weekly", "Monthly"]
                                             ).ask()
            habit_group = questionary.select("Which group does your habit belong to?",
                                             choices=["Health", "Education", "Food", "Sports", "Living"]
                                             ).ask()
            creation_date = datetime.today().date()
            current_streak = 0
            longest_streak = 0
            new_habit = Habit(name, desc, periodicity, habit_group, creation_date, current_streak, longest_streak)
            new_habit.store_habit(db)
            print("Your new habit has been created.")
            sleep(3)

        elif choice_action == "Increment habit":
            habit_name = questionary.text("Choose a habit to check off:").ask()
            if None == habit_exists(db, habit_name):
                print("This habit does not exist.")
            else:
                desc = get_description(db, habit_name)
                periodicity = get_periodicity(db, habit_name)
                creation_date = get_creation_date(db, habit_name)
                habit_group = get_habit_group(db, habit_name)
                current_streak = get_current_streak(db, habit_name)
                longest_streak = get_longest_streak(db, habit_name)
                chosen_habit = Habit(habit_name, desc, periodicity, habit_group, creation_date, current_streak,
                                     longest_streak)
                chosen_habit.complete_habit()
                increment_habit(db, habit_name)
                print(f"{habit_name} has been incremented.")
                sleep(3)

        elif choice_action == "Analyze habit":
            stop = False
            while not stop:
                choice_analysis = questionary.select(
                    "Which analysis do you want to perform?",
                    choices=["Calculate current streak for specific habit",
                             "Calculate longest streak for specific habit", "Get a table with all habits",
                             "Get a list of habits sorted by alphabet",
                             "Get a list of habits sorted by periodicity",
                             "Get a list of habits sorted by current streak",
                             "Get a list of habits sorted by longest streak",
                             "Display all completion dates for a habit",
                             "Display habits with certain periodicity", "Display habits in certain groups",
                             "Display habit with the longest streak among all habits",
                             "Display habit with the longest current streak among all habits",
                             "Exit program"]
                ).ask()

                if choice_analysis == "Calculate current streak for specific habit":
                    habit_name = questionary.text("Choose a habit to calculate current streak:").ask()
                    if None == habit_exists(db, habit_name):
                        print("This habit does not exist.")
                    else:
                        current_streak = calculate_current_streak(db, habit_name)
                        print(f"Your current streak for {habit_name} is {current_streak}")
                        update_current_streak(db, current_streak, habit_name)
                        print(f"Current streak for habit '{habit_name}' has been updated in the database.")
                    sleep(3)

                if choice_analysis == "Calculate longest streak for specific habit":
                    habit_name = questionary.text("Choose a habit to calculate longest streak:").ask()
                    if None == habit_exists(db, habit_name):
                        print("This habit does not exist.")
                    else:
                        longest_streak = calculate_longest_streak(db, habit_name)
                        print(f"Your longest streak for {habit_name} is {longest_streak}")
                        update_longest_streak(db, longest_streak, habit_name)
                        print(f"Longest streak for habit '{habit_name}' has been updated in the database.")
                    sleep(3)

                elif choice_analysis == "Get a table with all habits":
                    all_habits = get_all_habits(db)
                    if not all_habits:
                        print("There are no existing habits.")
                    else:
                        table_all_habits(db)
                    sleep(3)

                elif choice_analysis == "Get a list of habits sorted by alphabet":
                    user_habits = get_all_habits(db)
                    if not user_habits:
                        print("There are no existing habits.")
                    else:
                        table_sorted_alphabet(db)
                    sleep(3)

                elif choice_analysis == "Get a list of habits sorted by periodicity":
                    user_habits = get_all_habits(db)
                    if not user_habits:
                        print("There are no existing habits.")
                    else:
                        table_sorted_periodicity(db)
                    sleep(3)

                elif choice_analysis == "Get a list of habits sorted by current streak":
                    user_habits = get_all_habits(db)
                    if not user_habits:
                        print("There are no existing habits.")
                    else:
                        table_sorted_current_streak(db)
                    sleep(3)

                elif choice_analysis == "Get a list of habits sorted by longest streak":
                    user_habits = get_all_habits(db)
                    if not user_habits:
                        print("There are no existing habits.")
                    else:
                        table_sorted_longest_streak(db)
                    sleep(3)

                elif choice_analysis == "Display all completion dates for a habit":
                    habit_name = questionary.text("Choose a habit for which you want to "
                                                  "display all your completion dates").ask()
                    if None == habit_exists(db, habit_name):
                        print("This habit does not exist.")
                    else:
                        table_completion_dates(db, habit_name)
                    sleep(3)

                elif choice_analysis == "Display habits with certain periodicity":
                    display_habit_by_periodicity(db)
                    sleep(3)

                elif choice_analysis == "Display habits in certain groups":
                    display_habit_by_group(db)
                    sleep(3)

                elif choice_analysis == "Display habit with the longest current streak among all habits":
                    habit_with_longest_current_streak(db)
                    sleep(3)

                elif choice_analysis == "Display habit with the longest streak among all habits":
                    habit_with_longest_streak(db)
                    sleep(3)

                elif choice_analysis == "Exit program":
                    stop = True
                    print("Thank you for using the revolutionary habit tracker!")
                    sleep(3)

        elif choice_action == "Delete a habit":
            habit_to_delete = questionary.text("Which habit do you want to delete?").ask()
            if None == habit_exists(db, habit_to_delete):
                print("This habit does not exist.")
            else:
                confirm_deletion = questionary.confirm(
                    f"Are you sure you want to delete the habit '{habit_to_delete}'?").ask()
                if confirm_deletion:
                    delete_habit_from_db(db, habit_to_delete)
                else:
                    print("Deletion canceled. The habit was not deleted.")
            sleep(3)

        else:
            stop = True
            print("Thank you for using the revolutionary habit tracker!")
            sleep(3)


if __name__ == '__main__':
    cli()
