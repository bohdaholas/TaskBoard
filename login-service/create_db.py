from app import app, mysql

with app.app_context():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS login")
    cursor.execute("USE login")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        )
        ''')
    conn.commit()
    cursor.close()