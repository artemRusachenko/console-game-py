from Game import Game


def showPrompt(userName):
    promptStr = f"\n{userName}, do you want to play a new game? (y/n): "
    startGame = input(promptStr).lower()

    while startGame not in ['y', 'n']:
        print("\nIncorrect answer. Please, try again.")
        startGame = input(promptStr)
    return startGame


def main():
    userName = input("\nPlease, enter your name: ")
    startGame = showPrompt(userName)

    while startGame == 'y':
        game = Game(userName)
        game.start()
        del game
        startGame = showPrompt(userName)

    print(f'\n{userName}, see you next time!')


if __name__ == "__main__":
    main()



# game = Game()
# is_start = game.is_start()
#
# if is_start:
#     while not game.is_over:
#         game.ask_question()
#         if len(game.hints) > 0:
#             game.offer_hint()
#         game.answer_question()
#         if not game.is_over: game.choose_action()
#     game.over()
#     game.bye()
# else:
#     game.bye()
