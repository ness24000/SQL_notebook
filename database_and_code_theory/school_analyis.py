import sqlite3

# connect to database. Creates the database in current directory if it does not exist already.
connection = sqlite3.connect('school_database.db')
cursor = connection.cursor()

# to close the connection use 
connection.close()
# run queries without any output
cursor.execute("UPDATE teacher SET first_name = 'Nestor' WHERE teacher_id = 1")

# save changes permanently. Otherwise the changes will only exist
# in the current connection to the database and will be lost. 
connection.commit()

# run queries that have output

cursor.execute("SELECT * FROM teacher WHERE teacher_id = 1 OR teacher_id = 2").fetchall()

result = cursor.execute("SELECT * FROM teacher WHERE teacher_id = 1 OR teacher_id = 2")
result.fetchone()

# placeholders (use python variables in queries)

    # key to use a sequence of the same length as there are ?
cursor.execute("SELECT * FROM client WHERE client_id = ?", (101,)).fetchall()

    # you can also use named placeholders
cursor.execute("SELECT * FROM client WHERE client_id = :id", {'id':101}).fetchall()

# execute many (ONLY FOR DML CODE)
data = [(7,'Tomas', 'Smith', 'MAN', None, '1990-11-12', 34650, '+447840921326'), 
        (8, 'Maria', 'Johnson', 'ENG', None, '1985-09-25', 54892, '+447840921327'),
        (9, 'John', 'Doe', 'MAN', 'ENG', '1978-03-15', 73651, '+447840921328'), 
        (10, 'Emily', 'Williams', 'ESP', None, '1995-07-08', 20984, '+447840921329')]

cursor.executemany("INSERT INTO teacher VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

# AN EXERCISE

result =cursor.execute("""        
SELECT teacher.first_name, teacher.last_name, teacher.tax_id, teacher.phone_no
FROM teacher 
JOIN course ON course.teacher = teacher.teacher_id
WHERE course.client = (
SELECT client_id
FROM client
WHERE industry = 'NGO'
)
""")

result_list = result.fetchall()
tax_ngo_data = {}
for record in result_list:
    name = record[0] + '_' + record[1]    
    if name not in tax_ngo_data:
        tax_ngo_data[name] = (record[2], record[3])

tax_ngo_data



