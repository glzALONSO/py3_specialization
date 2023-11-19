# PASTE YOUR WOFPlayer CLASS (from part A) HERE
class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def addMoney(self, amt):
        self.prizeMoney += amt

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self, prize):
        self.prizes.append(prize)

    def __str__(self):
        return '{} (${})'.format(self.name, self.prizeMoney)


# PASTE YOUR WOFHumanPlayer CLASS (from part B) HERE
class WOFHumanPlayer(WOFPlayer):

    def __init__(self, name):
        WOFPlayer.__init__(self, name)

    def getMove(self, category, obscuredPhrase, guessed):
        prompt = """
        {} has ${}
        Category: {}
        Phrase:  {}
        Guessed: {}

        Guess a letter, phrase, or type 'exit' or 'pass':""".format(self.name, self.prizeMoney, category,
                                                                    obscuredPhrase,
                                                                    guessed)

        move = input(prompt)
        return move


# PASTE YOUR WOFComputerPlayer CLASS (from part C) HERE
class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'

    def __init__(self, name, difficulty):
        WOFPlayer.__init__(self, name)
        self.difficulty = difficulty

    def smartCoinFlip(self):
        flip = random.randint(1, 10)
        if flip >= self.difficulty:
            return False
        if flip <= self.difficulty:
            return True

    def getPossibleLetters(self, guessed):
        pos_letters = ''
        if VOWEL_COST > self.prizeMoney:
            for char in LETTERS:
                if (char in VOWELS) or char in guessed:
                    pos_letters = pos_letters
                else:
                    pos_letters = pos_letters + char

            return pos_letters

        else:
            for char in LETTERS:
                if char in guessed:
                    pos_letters = pos_letters
                else:
                    pos_letters = pos_letters + char

            return pos_letters

    def getMove(self, category, obscuredPhrase, guessed):
        pos_move = self.getPossibleLetters(guessed)

        if pos_move == '':
            return 'pass'
        else:
            flip = self.smartCoinFlip()
            pos_move_lst = [letter for letter in pos_move]

            if flip == True:
                best_move = pos_move_lst[0]
                for pos_move in pos_move_lst:
                    if self.SORTED_FREQUENCIES.index(pos_move) > self.SORTED_FREQUENCIES.index(best_move):
                        best_move = pos_move

                return best_move


            else:
                return random.choice(pos_move_lst)
