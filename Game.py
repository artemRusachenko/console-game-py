import os
import hints
from random import randint
from questions import Question


class Game:
    def __init__(self, name):
        self.name = name
        self.__question = None
        self.lvl = 0
        self._hints = [hints.Fifty(), hints.Call(), hints.HallHelp()]
        self._gain = '0'

    def set_question(self, question):
        self.__question = question

    def get_question(self):
        return self.__question

    def _toNextLevel(self):
        if self.lvl < 15:
            self.lvl += 1
            self._toLevel()
        else:
            self._finish()

    def _toCurLevel(self, showQuestion=True):
        self._toLevel(isNextQuestion=False, showQuestion=showQuestion)

    def _toLevel(self, isNextQuestion=True, showQuestion=True):
        if isNextQuestion:
            Game.clearScreen()
        if showQuestion:
            self._printQuestion(isNextQuestion)

        choice = self._getUserChoice()
        self._execUserChoice(choice)

    def _printQuestion(self, isNextQuestion):
        if isNextQuestion:
            self.set_question(Question(self.lvl))
            print(self.get_question()._question)
        print('\n'.join(self.get_question().getCurAnswers()))

    def _getUserChoice(self, chooseHint=False):
        correctChoices = self._printHintChoices() if chooseHint else self._printAnswerChoices()
        choice = input(f"{self.name}, enter your choice: ")

        if choice in correctChoices:
            return choice

        print("Incorrect input. Try again")
        return self._getUserChoice(chooseHint)

    def _printAnswerChoices(self):
        correctInput = []

        answs = map(lambda q: q[0], self.get_question().getCurAnswers())
        correctInput.extend(answs)

        print(f"({', '.join(correctInput)} - for answer, ", end='')

        if len(self._getNotUsedHints()) > 0:
            correctInput.extend(['h', 'H'])
            print("H - for hint) ", end='')

        # correctInput.extend(['q', 'Q'])
        # print(f"Q - for get prize and quit)")

        return correctInput

    def _printHintChoices(self):
        notUsedHints = self._getNotUsedHints()
        print(f"\n{self.name}, you have {len(notUsedHints)} hint(s): ")

        for i, hint in enumerate(notUsedHints):
            print(f"{i + 1}: {hint.getName()}\n", end='')
        print(f"b: Back")

        correctInput = [str(i) for i in range(1, len(notUsedHints)+1)]
        correctInput.extend(['b', 'B'])

        return correctInput

    def _getNotUsedHints(self):
        return list(filter(lambda h: not h.isUsed(), self._hints))

    def _execUserChoice(self, choice):
        if choice.lower() in ['a', 'b', 'c', 'd']:
            answer_mapping = {"a": "1", "b": "2", "c": "3", "d": "4"}
            answer_ind = answer_mapping.get(choice.lower(), -1)
            self._checkAnswer(int(answer_ind))

        elif choice in ['h', 'H']:
            self._useHint()

        # elif choice in ['q', 'Q']:
        #     if self.lvl != 1:
        #         self._gain = self.get_question().gain
        #     self._finish()

    def _isCountinue(self):
        print(f"Now you can withdraw ${self.get_question().gain}"
              f", but if your next answer is incorrect, you can withdraw ${self._gain}")
        res = input("Do you want to withdraw your money?(y/n)")
        if res.lower() == "y":
            return False
        elif res.lower() == "n":
            return True
        else:
            print("Incorrect input. Try again")
            return self._isCountinue()

    def _checkAnswer(self, answNum):
        if self.get_question().isCorrectAnswer(answNum):
            print("\nGreat job, you are absolutely right!\n")

            if self.lvl in [5, 10, 15]:
                self._gain = self.get_question().gain

            if self._isCountinue():
                self._toNextLevel()
            else:
                if self.lvl != 1:
                    self._gain = self.get_question().gain
                self._finish()
            Game.waitForEnter()

        else:
            print("\nOh, no! Unfortunately, you're wrong :-(")
            self._finish()

    def _useHint(self):
        choice = self._getUserChoice(chooseHint=True)
        if choice in ['b', 'B']:
            self._toCurLevel()
        else:
            notUsedHints = self._getNotUsedHints()
            hint = self.get_question().useHint(notUsedHints[int(choice) - 1])
            print(hint)
            self._toCurLevel(showQuestion=False)

    def _finish(self):
        if self._gain == '1 000 000':
            print(f"{self.name}, you win $ 1.000.000. CONGRATULATIONS!!!")
        elif self._gain != '0':
            print(f"{self.name}, your prize is ${self._gain}. Congratulations!")
        else:
            print(f"{self.name}, unfortunately you prize is $0.")
        self._save_result()

    def _save_result(self):
        file_name = f"statistics.txt"
        with open(file_name, 'r+') as f:
            text = f.read()
            lines = text.split("\n")
        data = list(map(lambda l: l.split("  "), lines))
        player = next((d for d in data if d[0] == self.name), None)
        if player:
            new_lines = []
            for row in data:
                if row[0] == player[0]:
                    record = self._gain if int(self._gain) > int(player[1]) else player[1]
                    update_player = [player[0], record]
                    line = "  ".join(map(str, update_player))
                else:
                    line = "  ".join(map(str, row))
                new_lines.append(f"{line}")
            with open(file_name, 'w') as f:
                f.writelines("\n".join(new_lines))
        else:
            with open(file_name, 'a') as f:
                f.write(f"\n{self.name}  {self._gain}")

    @staticmethod
    def waitForEnter():
        input("\nPress 'Enter' to continue")

    @staticmethod
    def clearScreen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def start(self):
        print('Welcome to the game "Who want to be a millionaire"')
        self._toNextLevel()





    # @staticmethod
    # def _greetings():
    #     print('Welcome to the game "Who want to be a millionaire"')
    #     name = input("Enter your name: ")
    #     return name

    # def is_start(self):
    #     is_start = input(f"{self.name}, do you want to start the game?\n")
    #     is_start = is_start.lower()
    #
    #     if is_start == "yes":
    #         return True
    #     elif is_start == "no":
    #         return False
    #     else:
    #         print('Please enter "yes" or "no"!')
    #         return Game.is_start(self)


    # def bye(self):
    #     print(f"Goodbye, {self.name}")
    #
    # def choose_action(self):
    #     question = self.get_question()
    #     print(f"Your answer is correct\nNow you can withdraw ${question[6]}, but if your next answer is incorrect,"
    #           f" you can withdraw ${self.gain}")
    #     is_over = input("Do you want to withdraw your gain?(yes/no)")
    #
    #     if is_over == "yes":
    #         self.gain = question[6]
    #         self.is_over = True
    #         # self.over()
    #     elif is_over == "no":
    #         # self.ask_question()
    #         return
    #     else:
    #         print('Please enter "yes" or "no"!')
    #         return self.choose_action()
    #
    # def ask_question(self):
    #     self.lvl += 1
    #     file_name = f"Questions/{self.lvl}.txt"
    #
    #     with open(file_name, 'r+') as f:
    #         questions = f.read()
    #         questions = questions.split("\n")
    #
    #     num_line = randint(0, len(questions) - 1)
    #     question = questions[num_line].split("  ")
    #     self.set_question(question)
    #
    #     print(f"{self.lvl} level \n" + "\n".join(question[:5]))
    #
    # def offer_hint(self):
    #     answer = input("Do you want to use a hint?(yes/no)")
    #     if answer == "yes":
    #         print("You have these hints")
    #         text = map(lambda h: f"{self.hints.index(h) + 1}. {h}", self.hints)
    #         hint_list = "\n".join(text)
    #         print(hint_list)
    #         ind = int(input("Write the number of the hint: "))
    #         if self.hints[ind - 1] == "50/50":
    #             print(self.fifty_hint())
    #         elif self.hints[ind - 1] == "call a friend":
    #             print(self.call_hint())
    #         elif self.hints[ind - 1] == "hall help":
    #             print(self.hall_hint())
    #     elif answer == "no":
    #         return
    #     else:
    #         return self.offer_hint()

    # def fifty_hint(self):
    #     answers = []
    #     question = self.get_question()
    #     question_copy = question.copy()
    #
    #     correct_ind = int(question[5])
    #     answers.append(question[correct_ind])
    #
    #     question_copy.pop(correct_ind)
    #     num_question = randint(1, 3)
    #     answers.append(question_copy[num_question])
    #
    #     self.hints.remove("50/50")
    #     return "\n".join(answers)
    #
    # def call_hint(self):
    #     file_name = "friend_answers.txt"
    #
    #     with open(file_name, "r+") as f:
    #         phrases = f.read()
    #         phrases = phrases.split("\n")
    #
    #     phrase_ind = randint(0, 2)
    #     res = phrases[phrase_ind]
    #     question = self.get_question()
    #     correct_ind = int(question[5])
    #     self.hints.remove("call a friend")
    #     if phrase_ind == 0:
    #         return res + f" {question[correct_ind][0]}"
    #     elif phrase_ind == 1:
    #         answer_ind = randint(correct_ind - 1, correct_ind) if correct_ind == 4 else randint(correct_ind,  correct_ind + 1)
    #         return res + f" {question[answer_ind][0]}"
    #     else:
    #         answer_ind = randint(1, 4)
    #         return res + f" {question[answer_ind][0]}"
    #
    # def hall_hint(self):
    #     question = self.get_question()
    #
    #     stats = []
    #
    #     for i in range(3):
    #         stats.append(randint(0, 100 - sum(stats)))
    #     stats.append(100 - sum(stats))
    #
    #     sort_stats = sorted(stats)
    #     answer_mapping = ["A", "B", "C", "D"]
    #     correct_answer_index = int(question[5]) - 1
    #
    #     res = f"{answer_mapping.pop(correct_answer_index)}: {sort_stats.pop(-1)} "
    #     for i in range(3):
    #         res += f"{answer_mapping.pop()}: {sort_stats.pop()} "
    #
    #     self.hints.remove("hall help")
    #     return res
    #
    # def answer_question(self):
    #     answer = input("Enter correct answer: ")
    #     answer = answer.lower()
    #     if answer not in "abcd":
    #         print("You must choose the letter of the answer!!!")
    #         return self.answer_question()
    #
    #     question = self.get_question()
    #
    #     answer_mapping = {"a": "1", "b": "2", "c": "3", "d": "4"}
    #     answer_ind = answer_mapping.get(answer, -1)
    #
    #     if question[5] == answer_ind:
    #         if self.lvl in [5, 10, 15]:
    #             self.gain = question[6]
    #             if self.lvl == 15:
    #                 self.is_over = True
    #     else:
    #         print("Your answer is wrong")
    #         self.is_lose = True
    #         self.is_over = True

    # def over(self):
    #     if :
    #         print(f"You lose(\nYour gain is {self.gain}")
    #     else:
    #         print(f"You win!!!\nYour gain is {self.gain}")
    #     self.save_result()



