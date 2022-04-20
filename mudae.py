import re
import sqlite3
from os import system as bash
from time import time

class MudaeTuRecord ():
    ## Class members:
    connection = sqlite3.connect('mudae.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tu_record
              (user TEXT varchar(30) primary key, can_claim BOOLEAN NOT NULL,
    claim_reset INT NOT NULL, rolls INT NOT NULL, rolls_reset INT NOT NULL,
    daily BOOLEAN NOT NULL, daily_reset INT NOT NULL, kakera BOOLEAN NOT NULL,
    kakera_reset INT NOT NULL, power INT NOT NULL, stock INT NOT NULL,
    can_dk BOOLEAN NOT NULL, can_dk_reset INT NOT NULL, can_vote BOOLEAN NOT NULL,
    can_vote_reset INT NOT NULL, message_id INT NOT NULL, min_time INT NOT NULL)''')
    connection.commit()

    sql_save = ''' INSERT OR REPLACE INTO tu_record(user,can_claim,claim_reset,
    rolls,rolls_reset,daily,daily_reset,
    kakera,kakera_reset,power,stock,can_dk,
    can_dk_reset,can_vote,can_vote_reset,message_id,min_time)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    sql_load= ''' SELECT user,can_claim,claim_reset,
    rolls,rolls_reset,daily,daily_reset,
    kakera,kakera_reset,power,stock,can_dk,
    can_dk_reset,can_vote,can_vote_reset,message_id,min_time FROM tu_record
    WHERE user=? '''

    # Use a class method to close the db
    #connection.close() # TODO FIXME

    def __init__(self, tu_message, from_db=False):

        if from_db:
            self.user = tu_message
            self.load(tu_message)
            return

        ## Verify message is valid:
        embeds = getattr(tu_message, "embeds")
        if len(embeds) >= 1: # An embed only:
            raise TypeError('Message contains embeds')

        if not tu_message.author.id == 432610292342587392: # Mudae Bot
            raise ValueError('Message author is not Mudae')

        if not "**=>** $tuarrange" in tu_message.content:
            raise ValueError('Message is not a $tu from Mudae')

        l_tu = tu_message.content.split("\n")
        self.message_id = tu_message.id
        self.min_time = int(time()/60) # Time in minutes

        ## Primera línea MARRY
        try:
            self.user = re.search(r"\*\*[^*]*", l_tu[0])[0].replace('*', '')
            if "__can__" in l_tu[0]:
                self.can_claim = True
                l_temp = re.search(r"next claim reset is in \*\*[^*]*", l_tu[0])[0].replace('next claim reset is in **', '').split('h ')
            else:
                self.can_claim = False
                l_temp = re.search(r"claim for another \*\*[^*]*", l_tu[0])[0].replace('claim for another **', '').split('h ')

            i_temp = l_temp[0]
            if len(l_temp) >= 2:
                i_temp = int(l_temp[0])*60 + int(l_temp[1])
            self.claim_reset = i_temp
        except:
            print("Fails first line")

        ## Segunda línea ROLLS
        try:
            self.rolls = re.search(r"\*\*[^*]*", l_tu[1])[0].replace('*', '')
            l_temp = re.search(r"Next rolls reset in \*\*[^*]*", l_tu[1])[0].replace('Next rolls reset in **', '').split('h ')
            i_temp = l_temp[0]
            if len(l_temp) >= 2:
                i_temp = int(l_temp[0])*60 + int(l_temp[1])
            self.rolls_reset = i_temp
        except:
            print("Fails second line")

        ## Tercera línea DAILY
        if "Next $daily reset" in l_tu[2]:
            self.daily = False
            l_temp = re.search(r"\*\*[^*]*", l_tu[2])[0].replace('*', '').split('h ')
            i_temp = l_temp[0]
            if len(l_temp) >= 2:
                i_temp = int(l_temp[0])*60 + int(l_temp[1])
            self.daily_reset = i_temp
        else:
            self.daily = True
            self.daily_reset = "0"

        ## Quinta línea, kakera reaction
        if "__can__" in l_tu[4]:
            self.kakera = True
            self.kakera_reset = "0"
        else:
            self.kakera = False
            l_temp = re.search(r"\*\*[^*]*", l_tu[4])[0].replace('*', '').split('h ')
            i_temp = l_temp[0]
            if len(l_temp) >= 2:
                i_temp = int(l_temp[0])*60 + int(l_temp[1])
            self.kakera_reset = i_temp


        ## Sexta y novena línea, POWER + STOCK
        self.power =  re.search(r"\*\*[^*]*", l_tu[5])[0].replace('*', '').replace("%", '')
        self.stock =  re.search(r"\*\*[^*]*", l_tu[8])[0].replace('*', '')


        ## DK claim
        if "Next $dk reset in" in l_tu[10]:
            self.can_dk = False
            l_temp = re.search(r"\*\*[^*]*", l_tu[10])[0].replace('*', '').split('h ')
            i_temp = l_temp[0]
            if len(l_temp) >= 2:
                i_temp = int(l_temp[0])*60 + int(l_temp[1])
            self.can_dk_reset = i_temp
        else:
            self.can_dk = True
            self.can_dk_reset =  "0"

        ## Vote
        if "You may vote again in" in l_tu[11]:
            self.can_vote = False
            l_temp = re.search(r"\*\*[^*]*", l_tu[11])[0].replace('*', '').split('h ')
            i_temp = l_temp[0]
            if len(l_temp) >= 2:
                i_temp = int(l_temp[0])*60 + int(l_temp[1])
            self.can_vote_reset =  i_temp
        else:
            self.can_vote = True
            self.can_vote_reset =  "0"

    def __str__(self):
        return """
\tObject user:\t\t**{}**
\tCan claim:\t\t**{}**
\tClaim reset:\t\t**{}** minutes
\tRolls:\t\t\t**{}**
\tRolls reset:\t\t**{}** minutes
\tDaily:\t\t\t**{}**
\tDaily reset:\t\t**{}** minutes
\tKakera:\t\t\t**{}**
\tKakera reset:\t\t**{}** minutes
\tPower:\t\t\t**{}**
\tStock:\t\t\t**{}**
\tCan $dk:\t\t**{}**
\tCan $dk_reset:\t\t**{}** minutes
\tCan vote:\t\t**{}**
\tCan vote reset:\t\t**{}** minutes
\tMessage ID:\t\t{}
\tTime:\t\t{} minutes
        """.format(
            self.user,
            self.can_claim,
            self.claim_reset,
            self.rolls,
            self.rolls_reset,
            self.daily,
            self.daily_reset,
            self.kakera,
            self.kakera_reset,
            self.power,
            self.stock,
            self.can_dk,
            self.can_dk_reset,
            self.can_vote,
            self.can_vote_reset,
            self.message_id,
            self.min_time,
        )

    def print(self):
        print(self.__str__().replace("*", ''))

    def save(self):
        self.update()
        self.cursor.execute(self.sql_save, [
            self.user,
            self.can_claim,
            self.claim_reset,
            self.rolls,
            self.rolls_reset,
            self.daily,
            self.daily_reset,
            self.kakera,
            self.kakera_reset,
            self.power,
            self.stock,
            self.can_dk,
            self.can_dk_reset,
            self.can_vote,
            self.can_vote_reset,
            self.message_id,
            self.min_time,
        ])
        self.connection.commit()

    def load(self, name):
        self.cursor.execute(self.sql_load, [
            self.user,
        ])

        rows = self.cursor.fetchall()
        for row in rows:
            self.user = str(row[0])
            self.can_claim = bool(row[1])
            self.claim_reset = int(row[2])
            self.rolls = int(row[3])
            self.rolls_reset = int(row[4])
            self.daily = bool(row[5])
            self.daily_reset = int(row[6])
            self.kakera = bool(row[7])
            self.kakera_reset = int(row[8])
            self.power = int(row[9])
            self.stock = int(row[10])
            self.can_dk = bool(row[11])
            self.can_dk_reset = int(row[12])
            self.can_vote = bool(row[13])
            self.can_vote_reset = int(row[14])
            self.message_id = int(row[15])
            self.min_time = int(row[16])

    def update(self):
        claim_reset = int(self.claim_reset) + int(int(self.min_time) - int(time()/60))
        if claim_reset <= 0:
            self.can_claim = True
            self.claim_reset = 0
        else:
            self.can_claim = False
            self.claim_reset = claim_reset

        # TODO
        # self.rolls
        # self.rolls_reset

        # self.daily
        # self.daily_reset

        # self.kakera
        # self.kakera_reset

        # self.power
        # self.stock

        # self.can_dk
        # self.can_dk_reset
        # self.can_vote
        # self.can_vote_reset
        # self.message_id
        # self.min_time


### Mudae claim embed
class MudaeClaimEmbed():
    def __init__(self, reaction, user=None):

        if user: # User is supplied
            if not user.id == 432610292342587392: # Not Mudae Bot
                raise ValueError('Reaction author is not Mudae')

        ## Verify message is valid:
        embeds = getattr(reaction.message, "embeds")
        if not len(embeds) == 1: # An embed only:
            raise TypeError('Message doesn\'t contain an embed')

        if not reaction.message.author.id == 432610292342587392: # Mudae Bot
            raise ValueError('Message author is not Mudae')

        if "**=>** $tuarrange" in reaction.message.content:
            raise ValueError('Message is a $tu from Mudae')

        if type(reaction.emoji) == type(str()):
            raise AttributeError('Emoji is string type')

        if reaction.emoji.id == 847502744176820256: # Rem
            raise ValueError('Reaction is a Rem emoji')

        if reaction.emoji.id == 847502746025459792: # Ram
            raise ValueError('Reaction is a Ram emoji')

        print("\nClaim class Message ID: {},\tReaction emoji ID: {}\n".format(reaction.message.id, reaction.emoji.id))
        bash("bash ./kakera_react.sh")
