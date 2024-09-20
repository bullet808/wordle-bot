from string import ascii_lowercase
from json import load as json_load

class Bot:
    """
    Holds all methods and attributes related to the bot.
    """

    def __init__(self) -> None:
        self.word_score_dict = self.get_dict("positional_scores.json")
        self.grey_letters = [] # letters confirmed not to be in the answer
        self.green_letters = {letter: 0 for letter in ascii_lowercase}
        self.yellow_letters = {letter: 0 for letter in ascii_lowercase}
        self.latest_guess = None
        self.word = [Char() for _ in range(5)]

    def get_dict(self, file_name: str) -> dict:
        """
        Loads the dictionary stored at a given file name.
        """

        with open(file_name, "r") as file:
            return json_load(file)
        
    def evaluate(self, info: str) -> None:
        """
        A guess' success is evaluated.
        """

        self.apply_info(info)
        self.filter_remaining_words()
        
    def apply_info(self, info: str) -> None:
        """
        Information obtained from the guess is applied to the Bot.
        """

        y_chars = []
        g_chars = []
      
        for char_idx, char in enumerate(info):
            char_in_answer = self.word[char_idx]
            char_in_guess = self.latest_guess[char_idx]

            if char == "G":
                if char_in_answer.value is None:
                    self.yellow_letters[char_in_guess] = max(0, self.yellow_letters[char_in_guess] - 1)
                    self.green_letters[char_in_guess] += 1
              
                    char_in_answer.value = char_in_guess

                g_chars.append(char_in_guess)

            elif char == "Y":
                char_in_answer.wrong.append(char_in_guess)
                y_chars.append(char_in_guess)

            elif char == "-":
                char_in_answer.wrong.append(char_in_guess)

        for char in y_chars:
            self.yellow_letters[char] = max(y_chars.count(char), self.yellow_letters[char]) - self.green_letters[char]

        # greying out letters that are neither green nor yellow
        for char_idx, char in enumerate(self.latest_guess):
            if y_chars.count(char) + g_chars.count(char) == 0:
                self.grey_letters.append(char)

        """similar_indices = self.get_similar_indices()
        if len(similar_indices) > 2:
            remaining_words = self.get_remaining_words()
            for idx in similar_indices:
                if self.word[idx].value is None:
                    char = remaining_words[0][idx]
                    
                    self.word[idx].value = char
                    self.yellow_letters[char] = max(0, self.yellow_letters[char] - 1)
                    self.green_letters[char] += 1"""

    def get_similar_indices(self) -> list[int]:
        words = self.get_remaining_words()

        key = list(words[0])

        for idx in range(5):
            for word in words[1:]:
                if word[idx] != key[idx]:
                    key[idx] = "-"
                    break

        return [idx for idx, item in enumerate(key) if item != "-"]

    def filter_remaining_words(self) -> None:
        """
        The remaining words in the dictionary are filtered to not include:
        - words with letters that are known to not be in the final word;
        - words without a known letter in its correct position;
        - words where a letter is in a position that isn't possible.
        """

        for word in self.get_remaining_words():
            do_rest = True
            for letter in self.yellow_letters:
                if word.count(letter) < (self.yellow_letters[letter] + self.green_letters[letter]):
                    self.word_score_dict.pop(word)
                    do_rest = False
                    break

            if do_rest:
                for char_idx, char in enumerate(word):
                    current_char = self.word[char_idx]
    
                    if char in self.grey_letters: # if char known not to be in answer
                        self.word_score_dict.pop(word)
                        break
    
                    elif current_char.value != None and char != current_char.value: # if current position value known and not equal to char
                        self.word_score_dict.pop(word)
                        break
                    
                    elif char in current_char.wrong: # if char known not to be in current position
                        self.word_score_dict.pop(word)
                        break
                  
    def get_alternate_word(self) -> str:
        """
        If there are 3 or 4 green letters, no yellows, more than one possible word remaining, and it's not the final guess, the bot chooses an alternate word to gather more information.

        First, the bot iterates through every remaining possible word and creates a list of the letters that could fill the gaps.

        Then, the bot iterates through every single word and finds the one that contains the most of those letters.
        """

        with open("words.txt") as file:
            all_alt_words = [line.rstrip() for line in file]

        """
        Firstly, a list is created containing the indices of every unknown char in the word.
        """
        unknown_idxs = [] 
        for char_idx, char in enumerate(self.word):
            if char.value == None:
                unknown_idxs.append(char_idx)

        AMOUNT_TO_INCREMENT = 1 / (len(self.word_score_dict) * 5)

        needed_chars_weighted = {char: 0 for char in ascii_lowercase}
        for word in self.word_score_dict:
            for idx in unknown_idxs:
                needed_chars_weighted[word[idx]] += AMOUNT_TO_INCREMENT

        best_word = (all_alt_words[0], float("-inf"))
        for word in all_alt_words:
            word_score = 0
            unique_chars = []
            for char_idx, char in enumerate(word):
                current_char = self.word[char_idx]
                if char not in unique_chars:
                    if current_char.value != char:
                        word_score += needed_chars_weighted[char]

                    unique_chars.append(char)

            word_score *= len(unique_chars)

            if word_score > best_word[1]:
                best_word = (word, word_score)

        return best_word[0]
    
    def get_remaining_words(self) -> list[str]:
        return list(self.word_score_dict.keys())

    def choose_best_word(self, guess_number: int) -> str:
        """
        Returns the Bot's best guess.
        """

        green_count = 0
        for char in self.word:
            if char.value != None:
                green_count += 1

        yellow_count = 0
        for char in self.yellow_letters:
            yellow_count += self.yellow_letters[char]

        all_remaining_words = self.get_remaining_words()

        
        if guess_number > 1 and guess_number < 6 and len(all_remaining_words) > 1 and yellow_count == 0:
            self.latest_guess = self.get_alternate_word()
        else:
            self.latest_guess = all_remaining_words[0]

        return self.latest_guess
        
class Char:
    """
    Represents a character in the solution.
    """
    def __init__(self) -> None:
        self.wrong = [] # a list of every letter this character is confirmed not to be
        self.value = None # set to char's actual value when found
