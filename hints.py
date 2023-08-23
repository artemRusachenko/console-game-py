import os.path
from random import choice, randint
from abc import ABC, abstractmethod


class Hint(ABC):
    def __init__(self):
        self._name = None
        self._isUsed = False

    def isUsed(self):
        return self._isUsed

    def getName(self):
        return self._name

    @abstractmethod
    def getHint(self, answers, correctAnswNum):
        pass


class Fifty(Hint):
    def __init__(self):
        super().__init__()
        self._name = "50/50"

    def getHint(self, answers, correctAnswNum):
        self._isUsed = True

        possibleAnswNums = list(range(1, 5))
        possibleAnswNums.remove(correctAnswNum)

        hintAnswNums = [answers[correctAnswNum - 1], answers[choice(possibleAnswNums) - 1]]
        hintAnsws = list(filter(lambda a: a in hintAnswNums, answers))

        return hintAnsws, None


class Call(Hint):

    def __init__(self):
        super().__init__()
        self._name = "call a friend"
        self._loadPhrases()

    def _loadPhrases(self):
        file_name = "friend_answers.txt"

        with open(file_name, "r+") as f:
            phrases = f.read()
            self._phrases = phrases.split("\n")

    def getHint(self, answers, correctAnswNum):
        self._isUsed = True

        phrase_ind = randint(0, 2)
        res = self._phrases[phrase_ind]
        if phrase_ind == 0:
            return None, res + f" {answers[correctAnswNum - 1][0]}"
        elif phrase_ind == 1:
            answer_ind = randint(correctAnswNum - 1, correctAnswNum) if correctAnswNum == 4 else randint(correctAnswNum,
                                                                                                correctAnswNum + 1)
            return None, res + f" {answers[answer_ind][0]}"
        else:
            answer_ind = randint(0, 3)
            return None, res + f" {answers[answer_ind][0]}"


class HallHelp(Hint):

    def __init__(self):
        super().__init__()
        self._name = "hall help"

    def getHint(self, answers, correctAnswNum):
        self._isUsed = True
        stats = []

        for i in range(3):
            stats.append(randint(0, 100 - sum(stats)))
        stats.append(100 - sum(stats))

        sort_stats = sorted(stats)
        answer_mapping = ["A", "B", "C", "D"]
        correct_answer_index = correctAnswNum - 1

        res = f"{answer_mapping.pop(correct_answer_index)}: {sort_stats.pop(-1)} "
        for i in range(3):
            res += f"{answer_mapping.pop()}: {sort_stats.pop()} "

        return None, res
