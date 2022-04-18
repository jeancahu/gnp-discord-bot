import re

class MudaeTuRecord ():
    def __init__(self, tu_message):
        l_tu = tu_message.split("\n")

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
        self.power =  re.search(r"\*\*[^*]*", l_tu[5])[0].replace('*', '')
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
        return """Object user: {}
        can_claim: {}
        claim_reset: {}
        rolls: {}
        rolls_reset: {}
        daily: {}
        daily_reset: {},
        kadera: {}
        kadera_reset: {}
        power: {}
        stock: {}
        can_dk: {}
        can_dk_reset: {}
        can_vote: {}
        can_vote_reset: {}
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
        )
