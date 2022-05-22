from tkinter import poop
import random
import time

game = Tk()
game.wm_title("Wordle")
player_guess = ''

game.geometry("700x700")
game.configure(bg="black")
game.resizable(False, False)

playing = True
guessesfile = open('guesses.txt','r')
possible_guesses = []


for line in guessesfile:
    splitList = line.split()
    splitList = ''.join(splitList)
    possible_guesses.append(splitList)

answersfile = open('answers.txt','r')
possible_answers = []
for line in answersfile:
    splitList = line.split()
    splitList = ''.join(splitList)
    possible_answers.append(splitList)


text = Label(game, text="Wordle", font = ("Arial bold",40),fg="white",bg="black")
text.place(relx=0.5, rely=0.15, anchor=CENTER)

can = Canvas(game, width=360,height=430,bg='black',borderwidth=0, highlightthickness=0)
can.place(relx=0.5, rely=0.5, anchor=CENTER)
squares = []
letters = []

for i in range(0,30):
    row = i%5
    col = i//5
    squares.append(can.create_rectangle((60*row+(row*10))+10,(60*col+(col*10))+10,(60*(row+1)+(row*10))+10,(60*(col+1)+(col*10))+10, fill="black", outline = 'grey',width=3))
for i in range(0,30):
    row = i%5
    col = i//5
    letters.append(can.create_text((60*row+(row*10))+40,(60*(col+1)+(col*10))-15,text="", font = ("Arial bold",32),fill="white"))


text = Label(game, text="Enter your guess:", font = ("Arial bold",12),fg="white",bg="black")
text.place(relx=0.3535, rely=0.85, anchor=CENTER)
    
entry = Entry(game, width= 30)
entry.place(relx= .59, rely= 0.85, anchor= CENTER)

notif = Label(game, text="", font = ("Arial bold",12),fg="white",bg="black")
notif.place(relx=0.5, rely=0.9, anchor=CENTER)


answer = possible_answers[random.randint(0,len(possible_answers))]
guesses = 0
setup = True
def gameOver():
    text.place(relx=0.5, rely=0.85, anchor=CENTER)
    text.config(text="Run game again to play again!")
    entry.place_forget()
    game.update()
    
def process(event=None):
    global setup
    if setup:
        player_guess = entry.get()
        entry.delete(0,END)
        result = []
        if len(player_guess) >= 6 or player_guess not in possible_guesses:
            notif.config(text="Not in word list!")
            game.update()
        else:
            notif.config(text="")
            global guesses
            game.update()
            list_answer = list(answer)
            for char in range(0,5):
                if player_guess[char] in list_answer and player_guess[char] != list_answer[char]:
                    for i in range(0,5):
                        if player_guess[char] == list_answer[i]:
                            list_answer[i]=''
                    result.append("#b69f3a")
                elif player_guess[char] == list_answer[char]:
                    list_answer[char] = ''
                    result.append("green")
                else:
                    result.append("grey")
            for i in range(0,len(result)):
                f=result[i]
                t=player_guess[i]
                can.itemconfig(i+1+guesses * 5,fill=f,outline=f)
                can.itemconfig(i+31+guesses * 5,text=t.upper())
            guesses += 1

            player_guess = ''
            if result == ['green','green','green','green','green']:
                notif.config(text="You guessed the word!")
                setup = False
                gameOver()
                game.update()
            else:
                if guesses == 6:
                    notif.config(text=f"You did not get the word, the word was: {answer}")
                    gameOver()
                    setup = False
                    game.update()
    else:
        gameOver()
        
entry.bind('<Return>', process)

game.mainloop()
