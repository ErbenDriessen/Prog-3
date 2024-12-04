import tkinter as tk
from tkinter import messagebox
import random

# Hoofd menu
class GalgjeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spellen")
        self.current_frame = None

        self.show_main_menu()

    def show_main_menu(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(pady=20)

        tk.Label(self.current_frame, text="Hoofd Menu", font=("Arial", 20)).pack(pady=10)
        tk.Button(self.current_frame, text="Speel Galgje", font=("Arial", 14), command=self.start_galgje).pack(pady=10)
        tk.Button(self.current_frame, text="Speel Raad het Getal", font=("Arial", 14), command=self.start_raad_getal).pack(pady=10)
        tk.Button(self.current_frame, text="Afsluiten", font=("Arial", 14), command=self.root.quit).pack(pady=10)

    def start_galgje(self):
        self.current_frame.destroy()
        Galgje(self)

    def start_raad_getal(self):
        self.current_frame.destroy()
        RaadHetGetal(self)

# Galgje spel
class Galgje:
    def __init__(self, app):
        self.app = app
        self.root = app.root

        self.word_list = ["python", "programmeren", "ontwikkelaar", "algoritme", "debuggen"] # lijst aan woorden die het spel gebruikt
        self.reset_game()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Galgje", font=("Arial", 20)).pack(pady=10)
        self.label_word = tk.Label(self.frame, text=" ".join(self.hidden_word), font=("Arial", 20))
        self.label_word.pack(pady=10)

        self.entry_guess = tk.Entry(self.frame, font=("Arial", 16))
        self.entry_guess.pack(pady=5)

        self.button_submit = tk.Button(self.frame, text="Gok", command=self.check_guess, font=("Arial", 14))
        self.button_submit.pack(pady=10)

        self.label_attempts = tk.Label(self.frame, text=f"Pogingen over: {self.remaining_attempts}", font=("Arial", 16))
        self.label_attempts.pack(pady=10)

        self.label_guessed = tk.Label(self.frame, text="Gegokte letters: ", font=("Arial", 12))
        self.label_guessed.pack(pady=10)

        tk.Button(self.frame, text="Terug naar hoofdmenu", command=self.return_to_menu, font=("Arial", 14)).pack(pady=10)

    def reset_game(self):
        self.word = random.choice(self.word_list) # Kies willekeurig woord uit de lijst
        self.hidden_word = ["_"] * len(self.word) # Begin met alle letters verborgen
        self.guessed_letters = [] # Lege lijst voor geraden letters
        self.remaining_attempts = 6 # maximaal aantal four gokken

    def check_guess(self):
        guess = self.entry_guess.get().lower()
        self.entry_guess.delete(0, tk.END)

        # Controle of gebruikers invoer geldig is
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Fout", "Voer één letter in.")
            return
        
        #controle of de letter al geraden is
        if guess in self.guessed_letters:
            messagebox.showwarning("Let op", "Deze letter is al geraden!")
            return

        self.guessed_letters.append(guess) # Voeg letter toe aan lijst gegokkte

        #controleer of de gok correct is
        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.hidden_word[i] = guess
            self.label_word.config(text=" ".join(self.hidden_word))
        else:
            self.remaining_attempts -= 1
            self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")

        self.label_guessed.config(text=f"Gegokte letters: {', '.join(self.guessed_letters)}")

        # win/loss conditie
        if "_" not in self.hidden_word:
            messagebox.showinfo("Gefeliciteerd", f"Je hebt het woord geraden: {self.word}!")
            self.reset_game()
            self.label_word.config(text=" ".join(self.hidden_word))
            self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")
            self.label_guessed.config(text="Gegokte letters: ")
        elif self.remaining_attempts == 0:
            messagebox.showerror("Verloren", f"Je hebt verloren! Het woord was: {self.word}.")
            self.reset_game()
            self.label_word.config(text=" ".join(self.hidden_word))
            self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")
            self.label_guessed.config(text="Gegokte letters: ")

    def return_to_menu(self):
        self.frame.destroy()
        self.app.show_main_menu()

# Getal Spel
class RaadHetGetal:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.number_to_guess = random.randint(1, 100)
        self.remaining_attempts = 10

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Raad het Getal", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.frame, text="Raad het getal tussen 1 en 100", font=("Arial", 16)).pack(pady=5)

        self.entry_guess = tk.Entry(self.frame, font=("Arial", 16))
        self.entry_guess.pack(pady=5)

        self.button_submit = tk.Button(self.frame, text="Gok", command=self.check_guess, font=("Arial", 14))
        self.button_submit.pack(pady=10)

        self.label_attempts = tk.Label(self.frame, text=f"Pogingen over: {self.remaining_attempts}", font=("Arial", 16))
        self.label_attempts.pack(pady=10)

        tk.Button(self.frame, text="Terug naar hoofdmenu", command=self.return_to_menu, font=("Arial", 14)).pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.entry_guess.get())
            self.entry_guess.delete(0, tk.END)

            if guess < 1 or guess > 100:
                messagebox.showerror("Fout", "Voer een getal in tussen 1 en 100.")
                return

            if guess == self.number_to_guess:
                messagebox.showinfo("Gefeliciteerd", "Je hebt het juiste getal geraden!")
                self.reset_game()
            elif guess < self.number_to_guess:
                messagebox.showinfo("Fout", "Het getal is hoger.")
            else:
                messagebox.showinfo("Fout", "Het getal is lager.")

            self.remaining_attempts -= 1
            self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")

            if self.remaining_attempts == 0:
                messagebox.showerror("Verloren", f"Je hebt verloren! Het juiste getal was: {self.number_to_guess}.")
                self.reset_game()
        except ValueError:
            messagebox.showerror("Fout", "Voer een geldig getal in.")

    def reset_game(self):
        self.number_to_guess = random.randint(1, 100)
        self.remaining_attempts = 10
        self.label_attempts.config(text=f"Pogingen over: {self.remaining_attempts}")

    def return_to_menu(self):
        self.frame.destroy()
        self.app.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = GalgjeApp(root)
    root.mainloop()
