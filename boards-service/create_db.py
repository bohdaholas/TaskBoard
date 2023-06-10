from app import app, mysql

with app.app_context():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boards (
            board_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255)
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            board_id INT NOT NULL
        )
        ''')
    
    cursor.execute('''TRUNCATE boards''')
    cursor.execute('''TRUNCATE members''')
    conn.commit()
    cursor.close()