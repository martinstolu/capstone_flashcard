import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"

current_word = {}
word_to_print = {}

try:
    wrong_words_file = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    word_to_print = original_data.to_dict(orient="records")
else:
    word_to_print = wrong_words_file.to_dict(orient="records")


def back_flash():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(translated_word, text=current_word["English"], fill="white")
    canvas.itemconfig(title_word, text="English", fill="white")


def switch_word():
    global current_word
    current_word = random.choice(word_to_print)
    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(translated_word, text=current_word["French"], fill="black")
    canvas.itemconfig(title_word, text="French", fill="black")
    window.after(3000, back_flash)


def is_known():
    word_to_print.remove(current_word)
    wrong_words = pandas.DataFrame(word_to_print)
    wrong_words.to_csv("data/words_to_learn.csv", index=False)
    switch_word()


# UI Setup
window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

front_img = PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_img)

back_img = PhotoImage(file="./images/card_back.png")

title_word = canvas.create_text(400, 150, text="Title", font=("Arial", 55, "italic"))
translated_word = canvas.create_text(400, 250, text="Word", font=("Arial", 55, "bold"))

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=switch_word)
right_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=is_known)
wrong_button.grid(column=0, row=1)

switch_word()


window.update_idletasks()
w = window.winfo_width()
h = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (w // 2)
y = (window.winfo_screenheight() // 2) - (h // 2)
window.geometry(f'+{x}+{y}')

window.iconphoto(False, right_img)
window.mainloop()
