import random

HANGMAN_STAGES = [
    """
        +---+
        |   |
            |
            |
            |
            |
      =========
    """,
    """
        +---+
        |   |
        O   |
            |
            |
            |
      =========
    """,
    """
        +---+
        |   |
        O   |
        |   |
            |
            |
      =========
    """,
    """
        +---+
        |   |
        O   |
       /|   |
            |
            |
      =========
    """,
    """
        +---+
        |   |
        O   |
       /|\\  |
            |
            |
      =========
    """,
    """
        +---+
        |   |
        O   |
       /|\\  |
       /    |
            |
      =========
    """,
    """
        +---+
        |   |
        O   |
       /|\\  |
       / \\  |
            |
      =========
    """
]

MOVIES = [
    {"movie": "INCEPTION", "clue": "Dream within a dream"},
    {"movie": "TITANIC", "clue": "Ship that sank on its maiden voyage"},
    {"movie": "JURASSICPARK", "clue": "Dinosaur theme park disaster"},
    {"movie": "AVATAR", "clue": "Blue aliens on a distant moon"},
    {"movie": "MATRIX", "clue": "Virtual reality simulation"},
]


class HangmanGame:
    """A class representing a Hangman game session for a movie."""

    def __init__(self, movie, clue):
        """Initialize a new game with the given movie and clue."""
        self.movie = movie.upper()
        self.clue = clue
        self.guessed_letters = set()
        self.max_attempts = 6
        self.remaining_attempts = self.max_attempts
        self.revealed_word = ['_' if c.isalpha() else c for c in self.movie]

    def display_clue(self):
        """Display the clue for the current movie."""
        print(f"Clue: {self.clue}")

    def display_hangman(self):
        """Display the current state of the hangman based on remaining attempts."""
        stage = self.max_attempts - self.remaining_attempts
        print(HANGMAN_STAGES[stage])

    def display_revealed_word(self):
        """Display the current state of the guessed movie with underscores and letters."""
        print(' '.join(self.revealed_word))

    def guess_letter(self, letter):
        """Process a guessed letter and update the game state accordingly."""
        letter = letter.upper()
        if letter in self.guessed_letters:
            print("You already guessed that letter.")
            return False
        self.guessed_letters.add(letter)
        if letter in self.movie:
            for i, char in enumerate(self.movie):
                if char == letter:
                    self.revealed_word[i] = letter
            return True
        self.remaining_attempts -= 1
        return False

    def is_win(self):
        """Check if the player has guessed all letters in the movie."""
        return '_' not in self.revealed_word

    def is_game_over(self):
        """Check if the game is over (win or loss)."""
        return self.is_win() or self.remaining_attempts <= 0

    def play(self):
        """Run the game loop for the current movie."""
        self.display_clue()
        while not self.is_game_over():
            self.display_hangman()
            self.display_revealed_word()
            while True:
                guess = input("Guess a letter: ").strip().upper()
                if len(guess) == 1 and guess.isalpha():
                    break
                print("Please enter a single alphabetic character.")
            self.guess_letter(guess)
        if self.is_win():
            print("Congratulations! You've guessed the movie correctly!")
        else:
            print(f"Game over! The movie was: {self.movie}")
        print("\nStarting next game...\n")


def main():
    """Main function to run the Hangman game indefinitely."""
    while True:
        movie_info = random.choice(MOVIES)
        game = HangmanGame(movie_info["movie"], movie_info["clue"])
        game.play()


if __name__ == "__main__":
    main()