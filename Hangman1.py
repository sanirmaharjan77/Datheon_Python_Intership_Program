import os
import random
import sys

MAX_MISTAKES = 6
WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")

# One ASCII picture per number of mistakes (0 through 6)
STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]

# The word list is scraped from the web and contains spam, adult and
# non-English entries. These are skipped so the game stays family friendly.
BLOCKED_WORDS = {
    "adult", "naked", "gay", "gays", "lesbian", "lesbians", "teen", "teens",
    "sexual", "sexuality", "sexually", "sucking", "shaved", "fetish", "lingerie",
    "porn", "poker", "casino", "casinos", "gambling", "blackjack", "roulette",
    "holdem", "betting", "viagra", "cialis", "levitra", "xanax", "valium",
    "tramadol", "phentermine", "hydrocodone", "adipex", "ambien", "zoloft",
    "paxil", "prozac", "fioricet", "ultram", "propecia", "babes", "hairy",
    "nudist", "spanking", "breast", "erotica", "pichunter", "thumbzilla",
    "thehun", "livecam", "naughty", "sexy", "blonde", "brunette", "redhead",
    "chubby", "booty", "deviant", "swingers", "peeing", "thongs", "thong",
    "pantyhose", "kissing", "licking", "interracial", "transexual",
    "transexuales", "transsexual", "travesti", "beastality", "voyeurweb",
    "voyuer", "shakira", "madonna", "eminem", "britney", "pamela",
    "drunk", "cocaine", "marijuana", "cigarette", "cigarettes", "suicide",
    "abortion", "terrorist", "terrorists", "terrorism", "murder", "torture",
    "violence", "violent", "holocaust", "slave", "nuke", "bomb", "weapon",
    "weapons", "dead", "death", "deaths", "killer", "killed", "killing",
}


def load_words():
    """Load the secret words from words.txt (one word per line).

    Only plain alphabetic words of 5-12 letters are kept, and blocked
    entries are removed, so every secret word is playable.
    """
    if not os.path.exists(WORDS_FILE):
        sys.exit(f"Could not find the word list: {WORDS_FILE}\n"
                 "Put 'words.txt' in the same folder as this script.")

    with open(WORDS_FILE, encoding="utf-8") as f:
        words = []
        for line in f:
            w = line.strip().lower()
            if w.isascii() and w.isalpha() and 5 <= len(w) <= 12 and w not in BLOCKED_WORDS:
                words.append(w)

    if not words:
        sys.exit("words.txt has no usable words (need 5-12 letter alphabetic words).")
    return words


def choose_word(words):
    """Pick a random secret word."""
    return random.choice(words).lower()


def mask_word(word, guessed):
    """Return the word with unguessed letters hidden, e.g. 'p _ t h _ n'."""
    return " ".join(ch if ch in guessed else "_" for ch in word)


def display_state(word, guessed, wrong, mistakes):
    """Print gallows art, masked word and guessed letters."""
    print(STAGES[mistakes])
    print(f"\nWord:   {mask_word(word, guessed)}")
    print(f"Wrong:  {' '.join(sorted(wrong)) or '-'}")
    print(f"Lives:  {MAX_MISTAKES - mistakes}/{MAX_MISTAKES}\n")


def get_guess(already_guessed):
    """Prompt until the player enters a valid, new single letter."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).")
        elif guess in already_guessed:
            print(f"You already guessed '{guess}'. Try another letter (no penalty).")
        else:
            return guess


def show_victory(word, mistakes):
    print(STAGES[mistakes])
    print(f"\nWord:   {' '.join(word)}")
    print("\n" + "=" * 40)
    print("  🎉  YOU WIN!  🎉")
    print(f"  The word was: {word.upper()}")
    print(f"  Mistakes made: {mistakes}/{MAX_MISTAKES}")
    print("=" * 40)


def show_defeat(word):
    print(STAGES[MAX_MISTAKES])
    print(f"\nWord:   {' '.join(word)}")
    print("\n" + "=" * 40)
    print("  ☠️   GAME OVER  ☠️")
    print(f"  The word was: {word.upper()}")
    print("=" * 40)


def play_round(words):
    """Play a single game of Hangman."""
    word = choose_word(words)
    letters = set(word)
    guessed = set()   # every letter tried (correct or not)
    wrong = set()
    mistakes = 0

    print("\nWelcome to HANGMAN!")
    print(f"I'm thinking of a {len(word)}-letter word. You have {MAX_MISTAKES} mistakes.")

    while mistakes < MAX_MISTAKES and not letters <= guessed:
        display_state(word, guessed, wrong, mistakes)
        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in letters:
            print(f"\n✅ Nice! '{guess}' is in the word.")
        else:
            wrong.add(guess)
            mistakes += 1
            print(f"\n❌ Sorry, '{guess}' is not in the word.")

    if letters <= guessed:
        show_victory(word, mistakes)
    else:
        show_defeat(word)


def play_again():
    answer = input("\nPlay again? (y/n): ").strip().lower()
    return answer in ("y", "yes")


def main():
    words = load_words()
    try:
        while True:
            play_round(words)
            if not play_again():
                break
    except (KeyboardInterrupt, EOFError):
        print()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()