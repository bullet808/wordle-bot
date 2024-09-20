from wordle_game import Game
from bot import Bot
from main import play_game

def run_test(words: list[str]) -> dict[int: int]:
    guesses_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 0: 0}
    failed_words = []

    for idx, word in enumerate(words):
        if idx % 100 == 0:
            print(f"Current word no. {idx + 1} - {word}\n{guesses_count[0]} failed so far.")
        
        try:
            guesses_taken = play_game(Game(word), Bot(), output=False)
            guesses_count[guesses_taken] += 1

            if guesses_taken == 0:
                failed_words.append(word)
        
        except:
            print(f"Error with {word}")

    save_failed_words(failed_words)

    return guesses_count

def save_failed_words(failed_words: list[str]) -> None:
    with open("failed_words.txt", "w") as file:
        for word in failed_words:
            file.write(f"{word}\n")

def output_results(guesses_count: dict[int: int]) -> None:
    total = 0

    print(f"Attempted every word:")
    for guess_number in guesses_count:
        print(f"{'Guess ' + str(guess_number) if guess_number != 0 else 'DNF'} - {guesses_count[guess_number]} time{'s' if guesses_count[guess_number] > 1 else ''}.")
        
        if guess_number != 0:
            total += guess_number * guesses_count[guess_number]

    print(f"Average number of guesses (excluding DNFs): {round(total / (len(words) - guesses_count[0]), 5)}")
    print(f"Fail Rate: {round(guesses_count[0] / len(words), 5)}")

# Iterating through every word to test Bot performance
if __name__ == "__main__":
    with open("words.txt") as file:
        words = [line.rstrip() for line in file]

    guesses_count = run_test(words)
    output_results(guesses_count)
    