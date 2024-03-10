import sqlite3

db = sqlite3.connect("main.db")
cursor = db.cursor()
data1 = [('Running', 'Go for a 5km run', 'Daily', 'Sports', '2024-02-18', 0, 0),
         ('Cleaning', 'Vacuum and clean the apartment', 'Weekly', 'Living', '2024-02-17', 0, 0),
         ('Drink enough', 'Drink at least 2 liters of water a day', 'Daily', 'Health', '2024-02-16', 0, 0),
         ('Clean windows', 'Clean all the windows in one room', 'Monthly', 'Living', '2024-02-15', 0, 0)
         ]
sql_query = ("INSERT INTO habit (habit_name, description, periodicity, habit_group, creation_date, current_streak,"
             " longest_streak) Values (?,?,?,?,?,?,?)")
cursor.executemany(sql_query, data1)
db.commit()
data2 = [
    ('Running', '2024-02-18'),
    ('Running', '2024-02-14'),
    ('Running', '2024-02-13'),
    ('Running', '2024-02-12'),
    ('Running', '2024-02-11'),
    ('Running', '2024-02-10'),
    ('Running', '2024-02-07'),
    ('Running', '2024-02-06'),
    ('Running', '2024-02-05'),
    ('Running', '2024-02-04'),
    ('Running', '2024-02-03'),
    ('Running', '2024-02-02'),
    ('Running', '2024-02-01'),
    ('Running', '2024-01-28'),
    ('Running', '2024-01-27'),
    ('Running', '2024-01-26'),
    ('Running', '2024-01-25'),
    ('Running', '2024-01-23'),
    ('Running', '2024-01-21'),
    ('Running', '2024-01-19'),
    ('Running', '2024-01-17'),
    ('Running', '2024-01-16'),
    ('Running', '2024-01-15'),
    ('Running', '2024-01-14'),
    ('Running', '2024-01-13'),
    ('Running', '2024-01-12'),
    ('Running', '2024-01-10'),
    ('Running', '2024-01-07'),
    ('Running', '2024-01-05'),
    ('Running', '2024-01-03'),
    ('Running', '2024-01-02'),
    ('Running', '2024-01-01'),
    ('Cleaning', '2024-02-16'),
    ('Cleaning', '2024-02-09'),
    ('Cleaning', '2024-02-02'),
    ('Cleaning', '2024-01-26'),
    ('Cleaning', '2024-01-19'),
    ('Cleaning', '2024-01-12'),
    ('Cleaning', '2024-01-05'),
    ('Drink enough', '2024-02-18'),
    ('Drink enough', '2024-02-17'),
    ('Drink enough', '2024-02-16'),
    ('Drink enough', '2024-02-15'),
    ('Drink enough', '2024-02-14'),
    ('Drink enough', '2024-02-13'),
    ('Drink enough', '2024-02-12'),
    ('Drink enough', '2024-02-11'),
    ('Drink enough', '2024-02-10'),
    ('Drink enough', '2024-02-04'),
    ('Drink enough', '2024-02-03'),
    ('Drink enough', '2024-02-02'),
    ('Drink enough', '2024-02-01'),
    ('Drink enough', '2024-01-28'),
    ('Drink enough', '2024-01-26'),
    ('Drink enough', '2024-01-24'),
    ('Drink enough', '2024-01-22'),
    ('Drink enough', '2024-01-20'),
    ('Drink enough', '2024-01-19'),
    ('Drink enough', '2024-01-17'),
    ('Drink enough', '2024-01-16'),
    ('Drink enough', '2024-01-15'),
    ('Drink enough', '2024-01-14'),
    ('Drink enough', '2024-01-13'),
    ('Drink enough', '2024-01-11'),
    ('Drink enough', '2024-01-10'),
    ('Drink enough', '2024-01-07'),
    ('Drink enough', '2024-01-06'),
    ('Drink enough', '2024-01-04'),
    ('Drink enough', '2024-01-02'),
    ('Drink enough', '2024-01-01'),
    ('Clean windows', '2024-01-01'),
    ('Clean windows', '2024-01-31')
]
sql_query = "INSERT INTO completion_dates (habit_name, event_date) Values (?, ?)"
cursor.executemany(sql_query, data2)
db.commit()


