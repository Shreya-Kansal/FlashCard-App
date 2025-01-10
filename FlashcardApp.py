import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime, timedelta

# Load flashcards from a JSON file
def load_flashcards(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save flashcards to a JSON file
def save_flashcards(file_path, flashcards):
    with open(file_path, 'w') as file:
        json.dump(flashcards, file)

# Spaced repetition logic: Adjust intervals
def adjust_review(card, difficulty):
    if difficulty == "Easy":
        card["interval"] *= 2
    elif difficulty == "Medium":
        card["interval"] += 1
    elif difficulty == "Hard":
        card["interval"] = 1
    card["next_review"] = (datetime.now() + timedelta(days=card["interval"])).strftime('%Y-%m-%d')

# Show the next flashcard
def show_next_card():
    global current_card
    for card in flashcards:
        if datetime.strptime(card["next_review"], '%Y-%m-%d') <= datetime.now():
            current_card = card
            question_label.config(text=card["question"])
            answer_label.config(text="")  # Hide the answer initially
            return
    messagebox.showinfo("Done", "No cards to review right now!")

# Show the answer
def show_answer():
    answer_label.config(text=current_card["answer"])

# Handle user rating
def handle_rating(difficulty):
    adjust_review(current_card, difficulty)
    save_flashcards("flashcards.json", flashcards)
    show_next_card()

# Add a new flashcard
def add_flashcard():
    question = simpledialog.askstring("New Flashcard", "Enter the question:")
    if not question:
        return
    answer = simpledialog.askstring("New Flashcard", "Enter the answer:")
    if not answer:
        return

    new_card = {
        "question": question,
        "answer": answer,
        "interval": 1,
        "next_review": datetime.now().strftime('%Y-%m-%d')
    }
    flashcards.append(new_card)
    save_flashcards("flashcards.json", flashcards)
    messagebox.showinfo("Success", "Flashcard added successfully!")

# Edit an existing flashcard
def edit_flashcard():
    questions = [card["question"] for card in flashcards]
    selected = simpledialog.askstring("Edit Flashcard", f"Select a flashcard to edit:\n\n{', '.join(questions)}")
    
    if not selected:
        return

    for card in flashcards:
        if card["question"] == selected:
            new_question = simpledialog.askstring("Edit Flashcard", "Edit the question:", initialvalue=card["question"])
            if not new_question:
                return
            new_answer = simpledialog.askstring("Edit Flashcard", "Edit the answer:", initialvalue=card["answer"])
            if not new_answer:
                return
            card["question"] = new_question
            card["answer"] = new_answer
            save_flashcards("flashcards.json", flashcards)
            messagebox.showinfo("Success", "Flashcard updated successfully!")
            return

    messagebox.showerror("Error", "Flashcard not found.")

# Initialize app
flashcards = load_flashcards("flashcards.json")
current_card = None

# Tkinter GUI setup
root = tk.Tk()
root.title("Spaced Repetition Flashcards")

question_label = tk.Label(root, text="", font=("Arial", 18), wraplength=400)
question_label.pack(pady=20)

answer_label = tk.Label(root, text="", font=("Arial", 16), fg="blue")
answer_label.pack(pady=20)

show_answer_btn = tk.Button(root, text="Show Answer", command=show_answer)
show_answer_btn.pack(pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

easy_btn = tk.Button(buttons_frame, text="Easy", command=lambda: handle_rating("Easy"))
easy_btn.pack(side=tk.LEFT, padx=10)

medium_btn = tk.Button(buttons_frame, text="Medium", command=lambda: handle_rating("Medium"))
medium_btn.pack(side=tk.LEFT, padx=10)

hard_btn = tk.Button(buttons_frame, text="Hard", command=lambda: handle_rating("Hard"))
hard_btn.pack(side=tk.LEFT, padx=10)

# Add menu for additional features
menu = tk.Menu(root)
root.config(menu=menu)

manage_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Manage Flashcards", menu=manage_menu)
manage_menu.add_command(label="Add Flashcard", command=add_flashcard)
manage_menu.add_command(label="Edit Flashcard", command=edit_flashcard)

# Start the app
show_next_card()
root.mainloop()