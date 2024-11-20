import tkinter as tk
from tkinter import messagebox
import random

class Galgje:
    def __init__(self, root):
        self.root = root
        self.root.title("Galgje")

        self.word_list = ["python", "programmeren", "ontwikkelaar", "algoritme", "debuggen"]  # Lijst met woorden
        self.reset_game()

        # GUI-elementen
        self.label_word = tk.Label(self.root, text=" ".join(self.hidden_word), font=("Arial", 20))
        self.label_word.pack(pady=10)

        self.entry_guess = tk.Entry(self.root, font=("Arial", 16))
        self.entry_guess.pack(pady=5)

        self.button_submit = tk.Button(self.root, text="Gok", command=self.check_guess, font=("Arial", 14))
        self.button_submit.pack(pady=10)

        self.label_attempts = tk.Label(self.root, text=f"Pogingen over: {self.remaining_attempts}", font=("Arial", 16))
        self.label_attempts.pack(pady=10)

        self.label_guessed = tk.Label(self.root, text=f"Gegokte letters: {', '.join(self.guessed_letters)}", font=("Arial", 12))
        self.label_guessed.pack(pady=10)

    def reset_game(self):
        self.word = random.choice(self.word_list)  # Kies een willekeurig woord
        self.hidden_word = ["_"] * len(self.word)
        self.guessed_letters = []
        self.remaining_attempts = 6

        # Update GUI-elementen
        if hasattr(self, 'label_word'):
            self.label_word.config(text=" ".join(self.hidden_word))
        if hasattr(self, 'label_attempts'):
            self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")
        if hasattr(self, 'label_guessed'):
            self.label_guessed.config(text="Gegokte letters: ")

    def check_guess(self):
        guess = self.entry_guess.get().lower()
        self.entry_guess.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Fout", "Voer één letter in.")
            return

        if guess in self.guessed_letters:
            messagebox.showwarning("Let op", "Deze letter is al geraden!")
            return

        self.guessed_letters.append(guess)

        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.hidden_word[i] = guess
            self.label_word.config(text=" ".join(self.hidden_word))
        else:
            self.remaining_attempts -= 1
            self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")

        self.label_guessed.config(text=f"Gegokte letters: {', '.join(self.guessed_letters)}")

        if "_" not in self.hidden_word:
            messagebox.showinfo("Gefeliciteerd", f"Je hebt het woord geraden: {self.word}!")
            self.reset_game()
        elif self.remaining_attempts == 0:
            messagebox.showerror("Verloren", f"Je hebt verloren! Het woord was: {self.word}.")
            self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = Galgje(root)
    root.mainloop()
