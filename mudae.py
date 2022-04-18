import re
import sqlite3

class MudaeTuRecord ():
    ## Class members:
    connection = sqlite3.connect('mudae.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tu_record
              (user TEXT varchar(30) primary key, can_claim BOOLEAN NOT NULL, claim_reset INT NOT NULL, rolls INT NOT NULL, rolls_reset INT NOT NULL)''')
    connection.commit()

    sql = ''' INSERT OR REPLACE INTO tu_record(user,can_claim,claim_reset,rolls,rolls_reset)
    VALUES(?,?,?,?,?) '''

    cursor.execute(sql, ["homura",True,30,1,30])
    connection.commit()

    connection.close() # TODO FIXME

    def __init__(self, tu_message):

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
\tClaim reset:\t\t**{}**
\tRolls:\t\t\t**{}**
\tRolls reset:\t\t**{}**
\tDaily:\t\t\t**{}**
\tDaily reset:\t\t**{}**
\tKakera:\t\t\t**{}**
\tKakera reset:\t\t**{}**
\tPower:\t\t\t**{}**
\tStock:\t\t\t**{}**
\tCan $dk:\t\t**{}**
\tCan $dk_reset:\t\t**{}**
\tCan vote:\t\t**{}**
\tCan vote reset:\t\t**{}**
\tMessage ID:\t\t{}
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
        )

    def print(self):
        print(self.__str__().replace("*", ''))

    def save(self):
        pass

### Mudae claim embed
class MudaeClaimEmbed():
    def __init__(self, message):
        ## Verify message is valid:
        embeds = getattr(message, "embeds")
        if not len(embeds) == 1: # An embed only:
            raise TypeError('Message doesn\'t contain an embed')

        if not message.author.id == 432610292342587392: # Mudae Bot
            raise ValueError('Message author is not Mudae')

        if "**=>** $tuarrange" in message.content:
            raise ValueError('Message is a $tu from Mudae')

        print("\nMessage ID: {}\n".format(message.id))
