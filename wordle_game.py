class Game:
    """
    Holds all methods and attributes related to the game itself.
    """
    def __init__(self, answer) -> None:
        self.answer = answer
        self.guessed = False # set to True when the Bot guesses correctly

    def check_guess(self, guess: str) -> str:
        """
        Checks the user's guess against the answer.
        If a character is in the right space, a G is added to the info.
        If a character is in the word but the wrong space, a Y is added to the info.

        A string of the info is returned.
        """

        if guess == self.answer:
            self.guessed = True
            return "GGGGG"

        info = list("-----")
        guess_list = list(guess)
        answer = list(self.answer)

        # checking for letters in right position
        for idx, letter in enumerate(guess_list):
            if letter == answer[idx]:
                info[idx] = "G"
                guess_list[idx] = "."
                answer[idx] = "."
        
        # checking if letters are in word but wrong position
        for idx, letter in enumerate(guess_list):
            if letter in answer and letter != ".":
                info[idx] = "Y"
                guess_list[idx] = "."
                answer[answer.index(letter)] = "."

        return "".join(info)
