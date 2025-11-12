import random
import tkinter as tk
from tkinter import ttk

def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(player, computer):
    if player == computer:
        return "tie"
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'paper' and computer == 'rock') or \
         (player == 'scissors' and computer == 'paper'):
        return "player"
    else:
        return "computer"

def console_game():
    """Simple text-based Rock-Paper-Scissors game (original game behavior)."""
    print("Rock, Paper, Scissors — Console Mode")
    print("Enter 'rock', 'paper' or 'scissors' to play. Enter 'q' to quit.")
    player_score = 0
    computer_score = 0
    rounds = 0
    while True:
        choice = input("Your move (rock/paper/scissors or q to quit): ").strip().lower()
        if choice == 'q':
            print("Thanks for playing.")
            break
        if choice not in ('rock', 'paper', 'scissors'):
            print("Invalid choice. Try again.")
            continue
        comp = get_computer_choice()
        winner = determine_winner(choice, comp)
        rounds += 1
        if winner == "tie":
            print(f"Round {rounds}: You chose {choice}, computer chose {comp}. It's a tie.")
        elif winner == "player":
            player_score += 1
            print(f"Round {rounds}: You chose {choice}, computer chose {comp}. You win this round!")
        else:
            computer_score += 1
            print(f"Round {rounds}: You chose {choice}, computer chose {comp}. Computer wins this round.")
        print(f"Score -> You: {player_score}  Computer: {computer_score}\n")

def create_gui():
    root = tk.Tk()
    root.title("Rock Paper Scissors")
    root.resizable(True, True)
    padding = {"padx": 10, "pady": 6}

    player_score = tk.IntVar(value=0)
    computer_score = tk.IntVar(value=0)

    
    score_frame = ttk.Frame(root)
    score_frame.grid(row=0, column=0, columnspan=3, **padding)
    ttk.Label(score_frame, text="Player:").grid(row=0, column=0, sticky="e")
    player_score_lbl = ttk.Label(score_frame, textvariable=player_score, width=3)
    player_score_lbl.grid(row=0, column=1, sticky="w")
    ttk.Label(score_frame, text="Computer:").grid(row=0, column=2, sticky="e")
    computer_score_lbl = ttk.Label(score_frame, textvariable=computer_score, width=3)
    computer_score_lbl.grid(row=0, column=3, sticky="w")

    
    status_frame = ttk.Frame(root)
    status_frame.grid(row=1, column=0, columnspan=3, **padding)
    player_choice_var = tk.StringVar(value="Player chose: -")
    computer_choice_var = tk.StringVar(value="Computer chose: -")
    result_var = tk.StringVar(value="Make a move")

    ttk.Label(status_frame, textvariable=player_choice_var).grid(row=0, column=0, columnspan=3, sticky="w")
    ttk.Label(status_frame, textvariable=computer_choice_var).grid(row=1, column=0, columnspan=3, sticky="w")
    ttk.Label(status_frame, textvariable=result_var, font=("Segoe UI", 10, "bold")).grid(row=2, column=0, columnspan=3, sticky="w")

    
    def play(choice):
        comp = get_computer_choice()
        player_choice_var.set(f"Player chose: {choice}")
        computer_choice_var.set(f"Computer chose: {comp}")
        winner = determine_winner(choice, comp)
        if winner == "tie":
            result_var.set("It's a tie!")
        elif winner == "player":
            result_var.set("You win!")
            player_score.set(player_score.get() + 1)
        else:
            result_var.set("Computer wins!")
            computer_score.set(computer_score.get() + 1)


    btn_frame = ttk.Frame(root)
    btn_frame.grid(row=2, column=0, columnspan=3, **padding)
    ttk.Button(btn_frame, text="Rock", command=lambda: play("rock"), width=12).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Paper", command=lambda: play("paper"), width=12).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Scissors", command=lambda: play("scissors"), width=12).grid(row=0, column=2, padx=5)

    
    control_frame = ttk.Frame(root)
    control_frame.grid(row=3, column=0, columnspan=3, **padding)
    def reset_scores():
        player_score.set(0)
        computer_score.set(0)
        player_choice_var.set("Player chose: -")
        computer_choice_var.set("Computer chose: -")
        result_var.set("Make a move")
    ttk.Button(control_frame, text="Reset", command=reset_scores).grid(row=0, column=0, padx=5)
    ttk.Button(control_frame, text="Quit", command=root.destroy).grid(row=0, column=1, padx=5)

    root.mainloop()

if __name__ == "__main__":
    choice = input("Enter 'g' to run GUI, anything else to run console version: ").strip().lower()
    if choice == 'g':
        create_gui()
    else:
        console_game()
