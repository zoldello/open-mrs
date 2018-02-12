import sqlite3
import numpy as np

'''Data Exercise 1, part A- List of male patients'''
conn = None
cursor = None

try:
    conn = sqlite3.connect('openmrs.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *
        FROM patient
        WHERE gender = 'M'
    ''')
    data = np.array(cursor.fetchall())

    print(' '.join(['gender', 'mrm', 'id', 'birthdate', 'birthdate_estimate']))
    print_friendly_data = "\n".join([", ".join(row) for row in data])
    print (print_friendly_data)

finally:
    cursor.close()
    conn.close()
