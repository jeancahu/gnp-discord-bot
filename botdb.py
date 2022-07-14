import sqlite3

ign_save = ''' INSERT OR REPLACE INTO member(user_id,aov,ign)
VALUES(?,?,?) '''

ign_load= ''' SELECT user_id,aov,ign FROM member
WHERE user_id=? '''

ign_pull= ''' SELECT user_id,aov,ign FROM member
'''


class homuri_memori ():
    def __init__(self):

        self.connection = sqlite3.connect('db.sqlite3')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS member
        (user_id INT primary key,
        aov BOOLEAN NOT NULL,
        ign TEXT varchar(130))
        ''')
        self.connection.commit()

    def __str__(self):
        return ""

    def save_ign(self, user_id, aov, ign):
        self.cursor.execute(ign_save, [
            user_id,
            aov,
            ign
        ])
        self.connection.commit()

    def load_ign(self, user_id):
        self.cursor.execute(ign_load, [
            user_id
        ])

        rows = self.cursor.fetchall()
        return rows

    def pull_ign(self):
        self.cursor.execute(ign_pull)
        rows = self.cursor.fetchall()
        return rows


    def close(self):
        self.connection.close()
