import sqlite3

connection = sqlite3.connect('mudae.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tu_record
              (user TEXT varchar(30) primary key, can_claim BOOLEAN NOT NULL, claim_reset INT NOT NULL, rolls INT NOT NULL, rolls_reset INT NOT NULL)''')
connection.commit()

sql = ''' INSERT OR REPLACE INTO tu_record(user,can_claim,claim_reset,rolls,rolls_reset)
VALUES(?,?,?,?,?) '''

cursor.execute(sql, ["homura",True,30,1,30])
connection.commit()

connection.close()
