import sqlite3

# Connect to your SQLite database
connection = sqlite3.connect('chatbot.db')
cursor = connection.cursor()

# Alter table to add a new column
cursor.execute("ALTER TABLE conversations ADD COLUMN modified_at TIMESTAMP")

# Commit the changes and close the connection
connection.commit()
connection.close()
