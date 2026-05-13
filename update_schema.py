import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='', database='game_server')
cursor = conn.cursor()

# Add status column if it doesn't exist
try:
    cursor.execute("ALTER TABLE matches ADD COLUMN status VARCHAR(20) DEFAULT 'active' AFTER player2_id")
    print('Added status column to matches table')
except Exception as e:
    if 'Duplicate column' in str(e):
        print('Status column already exists')
    else:
        print(f'Error: {e}')

# Create queue table
try:
    cursor.execute('''CREATE TABLE IF NOT EXISTS queue (
        queue_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL UNIQUE,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )''')
    print('Queue table created')
except Exception as e:
    print(f'Queue table error: {e}')

conn.commit()
cursor.close()
conn.close()
print('Database schema updated successfully!')
