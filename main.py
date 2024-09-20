from wordle_game import Game
from bot import Bot

def play_game(game: Game, bot: Bot, output: bool = True) -> int:
    for guess_number in range(6):
        guess = bot.choose_best_word(guess_number + 1)
        info = game.check_guess(guess)

        if output:
            print(f"GUESS {guess} | {info}")

        if game.guessed:
            return guess_number + 1

        bot.evaluate(info)

    return 0

if __name__ == "__main__":
    game = Game("guess")
    bot = Bot()

    guesses_taken = play_game(game, bot)
    
    if game.guessed:
        print(f"SOLVED IN {guesses_taken} GUESSES.")
    else:
        print("UNABLE TO SOLVE.")
