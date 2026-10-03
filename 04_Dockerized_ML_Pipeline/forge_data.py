import pymysql
import random

#connecting to MySQL
conn = pymysql.connect(host='mysql-db', user='retail_user', password='retail_pass', database='retail_db')
cursor = conn.cursor()

#table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
 trx_id INT AUTO_INCREMENT PRIMARY KEY,
 user_id VARCHAR(10),
 city VARCHAR(50),
 age INT,
 monthly_income INT,
 clicked_ad INT
)
""")

print("Generating 100,000 dirty transaction records...")
cities = ["Jakarta", "Surabaya", "Bandung", "Medan", None]
data = []

for i in range(100000):
    user_id = f"U{random.randint(1000, 9999)}"
    city = random.choice(cities)
    #injecting 15% Null values into age and income
    age = random.randint(18, 60) if random.random() > 0.15 else None
    income = random.randint(3000000, 25000000) if random.random() > 0.15 else None
    clicked = random.choice([0, 1])
    data.append((user_id, city, age, income, clicked))

#bulk injection to MySQL
cursor.executemany("INSERT INTO transactions (user_id, city, age, monthly_income, clicked_ad) VALUES (%s, %s, %s, %s, %s)", data)
conn.commit()
conn.close()

print("Data Injection to MySQL successful!")
