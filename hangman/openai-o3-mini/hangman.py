#!/usr/bin/env python3
"""
Hangman Game: Guess the Movie!

The game randomly selects a movie along with its clue. The player guesses
the movie title one letter at a time. For each wrong guess, a part of the
hangman is drawn. If the player correctly guesses the movie title, they are
congratulated and the game moves on to the next movie.
"""

import random


HANGMAN_STAGES = [
    (
        "  ------\n"
        "  |    |\n"
        "  |    \n"
        "  |   \n"
        "  |\n"
        "  |\n"
        "========="
    ),
    (
        "  ------\n"
        "  |    |\n"
        "  |    O\n"
        "  |   \n"
        "  |\n"
        "  |\n"
        "========="
    ),
    (
        "  ------\n"
        "  |    |\n"
        "  |    O\n"
        "  |    |\n"
        "  |\n"
        "  |\n"
        "========="
    ),
    (
        "  ------\n"
        "  |    |\n"
        "  |    O\n"
        "  |   /|\n"
        "  |\n"
        "  |\n"
        "========="
    ),
    (
        "  ------\n"
        "  |    |\n"
        "  |    O\n"
        "  |   /|\\\n"
        "  |\n"
        "  |\n"
        "========="
    ),
    (
        "  ------\n"
        "  |    |\n"
        "  |    O\n"
        "  |   /|\\\n"
        "  |   /\n"
        "  |\n"
        "========="
    ),
    (
        "  ------\n"
        "  |    |\n"
        "  |    O\n"
        "  |   /|\\\n"
        "  |   / \\\n"
        "  |\n"
        "========="
    )
]

# List of movies with their clues.
MOVIE_CLUES = [
    {"movie": "inception", "clue": "A thief enters dreams to steal secrets."},
    {"movie": "titanic", "clue": "A romance unfolds on a doomed ship."},
    {"movie": "avatar", "clue": "Blue beings fight to save their world."},
    {"movie": "gladiator", "clue": "A betrayed general seeks revenge in Rome."},
    {"movie": "matrix", "clue": "A hacker discovers reality is a simulation."},
    {"movie": "interstellar", "clue": "A space voyage to save humanity."},
    {"movie": "joker", "clue": "A man's descent into madness."}
]


def play_game(movie: str, clue: str) -> bool:
    """
    Play one round of the Hangman movie game.

    Args:
        movie: The movie title to be guessed (in lowercase).
        clue: A clue for the movie.

    Returns:
        True if the user guessed the movie correctly, False otherwise.
    """
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = len(HANGMAN_STAGES) - 1
    # Create a set of unique alphabetic letters in the movie title.
    movie_letters = {ch for ch in movie if ch.isalpha()}

    while wrong_guesses < max_wrong:
        # Display current hangman state and the clue.
        print("\n" + HANGMAN_STAGES[wrong_guesses])
        print(f"Clue: {clue}")

        # Display the current state of the movie title.
        display_word = []
        for ch in movie:
            if ch.isalpha():
                display_word.append(ch if ch in guessed_letters else "_")
            else:
                # Directly show spaces or punctuation.
                display_word.append(ch)
        print("Movie: " + " ".join(display_word))

        # Check if the user has guessed all letters.
        if movie_letters.issubset(guessed_letters):
            print("Congratulations! You guessed the movie correctly!")
            return True

        # Ask the user for their next guess.
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single alphabetic letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. Try another.")
            continue

        # Update the state based on the guess.
        if guess in movie_letters:
            guessed_letters.add(guess)
        else:
            wrong_guesses += 1
            print("Wrong guess!")

    # Player has exceeded the allowed wrong guesses.
    print("\n" + HANGMAN_STAGES[wrong_guesses])
    print(f"Game Over! The movie was: {movie.title()}")
    return False


def main() -> None:
    """
    Main function to run the Hangman movie game.
    """
    print("Welcome to the Hangman Movie Game!")
    while True:
        # Randomly select a movie and its clue.
        movie_data = random.choice(MOVIE_CLUES)
        movie = movie_data["movie"].lower()
        clue = movie_data["clue"]

        play_game(movie, clue)

        # Ask the user if they want to play another round.
        choice = input("\nDo you want to play again? (y/n): ").strip().lower()
        if choice != "y":
            print("Thank you for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()
