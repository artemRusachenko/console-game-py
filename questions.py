from random import randint


class Question:

    def __init__(self, lvl):
        self.lvl = lvl
        question = self.__getQuestion(lvl)
        self._question = question[0]
        self._answers = question[1], question[2], question[3], question[4]
        self._curAnswers = self._answers
        self._correctAnswNum = question[5]
        self.gain = question[6]

    def __str__(self):
        return f"Level: {self.lvl}\n{self._question}" + "\n".join(self._curAnswers)

    def __getQuestion(self, lvl):
        file_name = f"Questions/{lvl}.txt"

        with open(file_name, 'r+') as f:
            questions = f.read()
            questions = questions.split("\n")

        num_line = randint(0, len(questions) - 1)
        question = questions[num_line].split("  ")
        return question

    def isCorrectAnswer(self, answNum):
        return int(self._correctAnswNum) == answNum

    def getCorrectAnswer(self):
        return self._answers[int(self._correctAnswNum)-1]

    def useHint(self, hint):
        answs, phrase = hint.getHint(self._curAnswers, int(self._correctAnswNum))
        if answs:
            self._curAnswers = answs
            phrase = '\n'.join(answs)
        return f"{phrase}"

    def getCurAnswers(self):
        return self._curAnswers


