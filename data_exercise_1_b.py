import sqlite3
import numpy as np

'''Data Exercise 1, part  B- List Count of patients by gender'''
conn = None
cursor = None

try:
    conn = sqlite3.connect('openmrs.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT gender, count(gender)
        FROM patient
        GROUP BY gender
    ''')
    data = (cursor.fetchall())

    for datum in data:
        gender = ''

        if datum[0].strip().lower() == 'm':
            gender = 'Male'
        elif datum[0].strip().lower() == 'f':
            gender = 'Female'
        else:
            gender = 'Unspecified'


        print(f'{gender}: {datum[1]}')

finally:
    cursor.close()
    conn.close()
