

import tkinter as tk
from tkinter import messagebox
import random


class Memory:
    def __init__(self, root, rows, columns):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.turn = 0
        self.scores = [0, 0]
        self.first_card = None
        self.second_card = None
        self.buttons = []
        self.icons = self.generate_icons()
        self.board = self.generate_board()

        self.create_widgets()
        self.update_status()


    def generate_icons(self):
        icons = []
        for i in range((self.rows * self.columns) // 2):
            icons.append(str(i))
            icons.append(str(i))
        random.shuffle(icons)
        return icons


    def generate_board(self):
        board = []
        for row in range(self.rows):
            board_row = []
            for col in range(self.columns):
                board_row.append(self.icons.pop())
            board.append(board_row)
        return board


    def create_widgets(self):
        for row in range(self.rows):
            button_row = []
            for col in range(self.columns):
                button = tk.Button(self.root, text='', width=10, height=4,
                                   command=lambda r=row, c=col: self.reveal_card(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=self.rows, column=0, columnspan=self.columns)


    def update_status(self):
        self.status_label.config(text=f"Player 1: {self.scores[0]}  Player 2: {self.scores[1]}  Turn: Player {self.turn + 1}")


    def reveal_card(self, row, col):
        if self.buttons[row][col]['text'] == '':
            self.buttons[row][col].config(text=self.board[row][col], state="disabled")
            if self.first_card is None:
                self.first_card = (row, col)
            elif self.second_card is None:
                self.second_card = (row, col)
                self.root.after(50, self.check_match)


    def check_match(self):
        r1, c1 = self.first_card
        r2, c2 = self.second_card
        if self.board[r1][c1] == self.board[r2][c2]:
            self.scores[self.turn] += 1
        else:
            self.buttons[r1][c1].config(text=' ', state="normal")
            self.buttons[r2][c2].config(text=' ', state="normal")
            self.turn = 1 - self.turn
        self.first_card = None
        self.second_card = None
        self.update_status()



class Minesweeper:
    def __init__(self, root, rows, columns, mines):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.board = [[0 for _ in range(columns)] for _ in range(rows)]
        self.buttons = [[None for _ in range(columns)] for _ in range(rows)]
        self.create_board()
        self.create_widgets()


    def create_board(self):
        for _ in range(self.mines):
            while True:
                r = random.randint(0, self.rows - 1)
                c = random.randint(0, self.columns - 1)
                if self.board[r][c] != -1:
                    self.board[r][c] = -1
                    break
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] == -1:
                    continue
                count = 0
                for i in range(max(0, r-1), min(self.rows, r+2)):
                    for j in range(max(0, c-1), min(self.columns, c+2)):
                        if self.board[i][j] == -1:
                            count += 1
                self.board[r][c] = count


    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.columns):
                button = tk.Button(self.root, width=3, command=lambda row=r, col=c: self.click(row, col))
                button.bind("<Button-3>", lambda e, row=r, col=c: self.flag(row, col))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button


    def click(self, row, col):
        if self.board[row][col] == -1:
            self.buttons[row][col].config(text='*', bg='red')
            messagebox.showinfo("Game Over", "You clicked on a mine!")
            self.root.quit()
        else:
            self.reveal(row, col)
        self.check_win()


    def reveal(self, row, col):
        if self.buttons[row][col]['text'] == '':
            self.buttons[row][col].config(text=self.board[row][col])
            if self.board[row][col] == 0:
                for r in range(max(0, row-1), min(self.rows, row+2)):
                    for c in range(max(0, col-1), min(self.columns, col+2)):
                        self.reveal(r, c)


    def flag(self, row, col):
        if self.buttons[row][col]['text'] == '':
            self.buttons[row][col].config(text='F', bg='yellow')
        elif self.buttons[row][col]['text'] == 'F':
            self.buttons[row][col].config(text='', bg='SystemButtonFace')


    def check_win(self):
        count = sum(self.buttons[r][c]['text'] == '' for r in range(self.rows) for c in range(self.columns))
        if count == self.mines:
            messagebox.showinfo("Congratulations!", "You win!")
            self.root.quit()


class Blackjack:
    def __init__(self, root, Deck, Hand):
        self.root = root
        self.root.title("Blackjack")
        
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        self.winner = None

        self.deal_initial_cards()

        self.create_widgets()

 
    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.draw_card())
            self.dealer_hand.add_card(self.deck.draw_card())


    def create_widgets(self):
        self.player_label = tk.Label(self.root, text="Player's Hand: " + str(self.player_hand))
        self.player_label.pack(pady=10)

        self.dealer_label = tk.Label(self.root, text="Dealer's Hand: " + str(self.dealer_hand.cards[0]) + ", [Hidden]")
        self.dealer_label.pack(pady=10)

        self.hit_button = tk.Button(self.root, text="Hit", command=self.player_hit)
        self.hit_button.pack(pady=5)

        self.stand_button = tk.Button(self.root, text="Stand", command=self.dealer_play)
        self.stand_button.pack(pady=5)


    def update_labels(self):
        self.player_label.config(text="Player's Hand: " + str(self.player_hand))
        if self.game_over:
            self.dealer_label.config(text="Dealer's Hand: " + str(self.dealer_hand))
        else:
            self.dealer_label.config(text="Dealer's Hand: " + str(self.dealer_hand.cards[0]) + ", [Hidden]")


    def player_hit(self):
        if not self.game_over:
            self.player_hand.add_card(self.deck.draw_card())
            if self.player_hand.get_value() > 21:
                self.game_over = True
                self.winner = 'dealer'
                messagebox.showinfo("Game Over", "Player busts! Dealer wins.")
            self.update_labels()


    def dealer_play(self):
        if not self.game_over:
            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.draw_card())
            if self.dealer_hand.get_value() > 21 or self.player_hand.get_value() > self.dealer_hand.get_value():
                self.winner = 'player'
                messagebox.showinfo("Game Over", "Player wins!")
            else:
                self.winner = 'dealer'
                messagebox.showinfo("Game Over", "Dealer wins!")
            self.game_over = True
            self.update_labels()


class Solitaire:
    def __init__(self, root, Deck):
        self.root = root
        self.root.title("Solitaire")
        
        self.deck = Deck()
        self.stock = []
        self.waste = []
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]

        self.deal_cards()

        self.create_widgets()


    def deal_cards(self):
        for i in range(7):
            for j in range(i, 7):
                card = self.deck.draw_card()
                self.tableau[j].append(card)


    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='green')
        self.canvas.pack()

        self.draw_piles()


    def draw_piles(self):
        x, y = 50, 50
        for i, pile in enumerate(self.tableau):
            for j, card in enumerate(pile):
                self.canvas.create_text(x + i*100, y + j*20, text=str(card), fill='white')


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.turn = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_widgets()


    def create_widgets(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text='', width=10, height=5,
                                   command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button


    def click(self, row, col):
        if not self.buttons[row][col]['text'] and not self.check_winner():
            self.board[row][col] = self.turn
            self.buttons[row][col].config(text=self.turn)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.turn} wins!")
            elif all(self.board[r][c] for r in range(3) for c in range(3)):
                messagebox.showinfo("Game Over", "It's a draw!")
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'


    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '' or self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False


class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.player_choice = None
        self.computer_choice = random.choice(self.choices)

        self.create_widgets()


    def create_widgets(self):
        self.player_label = tk.Label(self.root, text="Choose: Rock, Paper, or Scissors")
        self.player_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        for choice in self.choices:
            button = tk.Button(self.root, text=choice, width=10, height=2,
                               command=lambda c=choice: self.make_choice(c))
            button.pack(pady=5)


    def make_choice(self, choice):
        self.player_choice = choice
        self.computer_choice = random.choice(self.choices)
        self.determine_winner()
        self.update_result()


    def determine_winner(self):
        if self.player_choice == self.computer_choice:
            self.result = "It's a draw!"
        elif (self.player_choice == 'Rock' and self.computer_choice == 'Scissors') or \
             (self.player_choice == 'Paper' and self.computer_choice == 'Rock') or \
             (self.player_choice == 'Scissors' and self.computer_choice == 'Paper'):
            self.result = "You win!"
        else:
            self.result = "Computer wins!"


    def update_result(self):
        self.result_label.config(text=f"You chose: {self.player_choice}\nComputer chose: {self.computer_choice}\n{self.result}")


class NumberGuessing:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        
        self.number = random.randint(1, 100)

        self.create_widgets()


    def create_widgets(self):
        self.label = tk.Label(self.root, text="Guess the number (between 1 and 100):3")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        self.button = tk.Button(self.root, text="Guess", command=self.check_guess)
        self.button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=('Helvetica', 16))
        self.result_label.pack(pady=10)


    def check_guess(self):
        guess = int(self.entry.get())
        if guess < self.number:
            self.result_label.config(text="Too low!")
        elif guess > self.number:
            self.result_label.config(text="Too high!")
        else:
            self.result_label.config(text="Correct! You guessed the number!")


class Hangman:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.word_list = ["python", "java", "hangman", "challenge", "tkinter"]
        self.word = random.choice(self.word_list)
        self.guessed_letters = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

        self.create_widgets()
        self.update_display()


    def create_widgets(self):
        self.word_label = tk.Label(self.root, text="", font=('Helvetica', 16))
        self.word_label.pack(pady=10)

        self.letter_entry = tk.Entry(self.root)
        self.letter_entry.pack(pady=10)

        self.guess_button = tk.Button(self.root, text="Guess", command=self.guess_letter)
        self.guess_button.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts_left}")
        self.attempts_label.pack(pady=10)


    def update_display(self):
        display_word = ''.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        self.word_label.config(text=display_word)


    def guess_letter(self):
        letter = self.letter_entry.get().lower()
        self.letter_entry.delete(0, tk.END)
        if letter in self.guessed_letters or not letter.isalpha() or len(letter) != 1:
            return
        self.guessed_letters.add(letter)
        if letter not in self.word:
            self.attempts_left -= 1
        self.update_display()
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")

        if all(letter in self.guessed_letters for letter in self.word):
            messagebox.showinfo("Hangman", "Congratulations! You guessed the word!")
            self.root.quit()
        elif self.attempts_left == 0:
            messagebox.showinfo("Hangman", f"Game Over! The word was: {self.word}")
            self.root.quit()


class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.rows = 6
        self.columns = 7
        self.board = [['' for _ in range(self.columns)] for _ in range(self.rows)]
        self.turn = 'Red'
        self.create_widgets()


    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg='blue')
        self.canvas.pack()

        for row in range(self.rows):
            for col in range(self.columns):
                self.canvas.create_oval(col * 100, row * 100, col * 100 + 100, row * 100 + 100, fill='white')

        self.canvas.bind("<Button-1>", self.handle_click)


    def handle_click(self, event):
        col = event.x // 100
        if self.board[0][col] != '':
            return
        row = self.get_available_row(col)
        self.board[row][col] = self.turn
        self.draw_piece(row, col, self.turn)
        if self.check_winner(row, col):
            messagebox.showinfo("Connect Four", f"{self.turn} wins!")
            self.root.quit()
        self.turn = 'Yellow' if self.turn == 'Red' else 'Red'


    def get_available_row(self, col):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == '':
                return row


    def draw_piece(self, row, col, color):
        self.canvas.create_oval(col * 100, row * 100, col * 100 + 100, row * 100 + 100, fill=color)


    def check_winner(self, row, col):
        return self.check_direction(row, col, 1, 0) or self.check_direction(row, col, 0, 1) or self.check_direction(row, col, 1, 1) or self.check_direction(row, col, 1, -1)


    def check_direction(self, row, col, row_offset, col_offset):
        count = 0
        color = self.board[row][col]
        for i in range(-3, 4):
            r, c = row + i * row_offset, col + i * col_offset
            if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False


class Snake:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='black')
        self.canvas.pack()
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.place_food()
        self.direction = 'Down'
        self.running = True
        self.root.bind('<KeyPress>', self.change_direction)
        self.update()


    def place_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        return x, y


    def change_direction(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            self.direction = event.keysym


    def update(self):
        if not self.running:
            return

        head_x, head_y = self.snake[-1]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 20)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 20)
        elif self.direction == 'Left':
            new_head = (head_x - 20, head_y)
        else:
            new_head = (head_x + 20, head_y)

        if new_head[0] < 0 or new_head[0] >= 400 or new_head[1] < 0 or new_head[1] >= 400 or new_head in self.snake:
            messagebox.showinfo("Game Over", "You lost!")
            self.running = False
            return

        self.snake.append(new_head)
        if new_head == self.food:
            self.food = self.place_food()
        else:
            self.snake.pop(0)

        self.canvas.delete('all')
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill='green')
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill='red')

        self.root.after(100, self.update)


class Pong:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='black')
        self.canvas.pack()

        self.paddle1 = self.canvas.create_rectangle(20, 150, 30, 250, fill='white')
        self.paddle2 = self.canvas.create_rectangle(570, 150, 580, 250, fill='white')
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill='white')

        self.ball_dx = 3
        self.ball_dy = 3
        self.paddle1_dy = 0
        self.paddle2_dy = 0

        self.root.bind('<KeyPress>', self.key_down)
        self.root.bind('<KeyRelease>', self.key_up)

        self.update()


    def key_down(self, event):
        if event.keysym == 'w':
            self.paddle1_dy = -5
        elif event.keysym == 's':
            self.paddle1_dy = 5
        elif event.keysym == 'Up':
            self.paddle2_dy = -5
        elif event.keysym == 'Down':
            self.paddle2_dy = 5


    def key_up(self, event):
        if event.keysym in ['w', 's']:
            self.paddle1_dy = 0
        elif event.keysym in ['Up', 'Down']:
            self.paddle2_dy = 0


    def update(self):
        self.canvas.move(self.paddle1, 0, self.paddle1_dy)
        self.canvas.move(self.paddle2, 0, self.paddle2_dy)

        paddle1_coords = self.canvas.coords(self.paddle1)
        if paddle1_coords[1] < 0 or paddle1_coords[3] > 400:
            self.canvas.move(self.paddle1, 0, -self.paddle1_dy)

        paddle2_coords = self.canvas.coords(self.paddle2)
        if paddle2_coords[1] < 0 or paddle2_coords[3] > 400:
            self.canvas.move(self.paddle2, 0, -self.paddle2_dy)

        ball_coords = self.canvas.coords(self.ball)
        if ball_coords[1] <= 0 or ball_coords[3] >= 400:
            self.ball_dy = -self.ball_dy

        if self.collide(paddle1_coords, ball_coords) or self.collide(paddle2_coords, ball_coords):
            self.ball_dx = -self.ball_dx

        if ball_coords[0] <= 0 or ball_coords[2] >= 600:
            self.canvas.coords(self.ball, 290, 190, 310, 210)
            self.ball_dx = 3
            self.ball_dy = 3

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        self.root.after(20, self.update)

    def collide(self, paddle_coords, ball_coords):
        return paddle_coords[0] < ball_coords[2] and paddle_coords[2] > ball_coords[0] and paddle_coords[1] < ball_coords[3] and paddle_coords[3] > ball_coords[1]


class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")

        self.board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                      [6, 0, 0, 1, 9, 5, 0, 0, 0],
                      [0, 9, 8, 0, 0, 0, 0, 6, 0],
                      [8, 0, 0, 0, 6, 0, 0, 0, 3],
                      [4, 0, 0, 8, 0, 3, 0, 0, 1],
                      [7, 0, 0, 0, 2, 0, 0, 0, 6],
                      [0, 6, 0, 0, 0, 0, 2, 8, 0],
                      [0, 0, 0, 4, 1, 9, 0, 0, 5],
                      [0, 0, 0, 0, 8, 0, 0, 7, 9]]

        self.create_widgets()


    def create_widgets(self):
        self.entries = [[tk.Entry(self.root, width=3, font=('Helvetica', 18), justify='center') for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                self.entries[row][col].grid(row=row, column=col)
                if self.board[row][col] != 0:
                    self.entries[row][col].insert(0, self.board[row][col])
                    self.entries[row][col].config(state='disabled')

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.grid(row=9, column=0, columnspan=9)


    def solve(self):
        if self.solve_board():
            for row in range(9):
                for col in range(9):
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, self.board[row][col])
        else:
            messagebox.showinfo("Sudoku", "No solution exists")


    def solve_board(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num
                if self.solve_board():
                    return True
                self.board[row][col] = 0
        return False


    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None


    def is_valid(self, num, row, col):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True


class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")

        self.create_widgets()


    def create_widgets(self):
        tk.Button(self.root, text="Memory Game", command=self.launch_memory).pack(pady=10)
        tk.Button(self.root, text="Tic Tac Toe", command=self.launch_tic_tac_toe).pack(pady=10)
        tk.Button(self.root, text="Rock Paper Scissors", command=self.launch_rock_paper_scissors).pack(pady=10)
        tk.Button(self.root, text="Number Guessing Game", command=self.launch_number_guessing).pack(pady=10)
        tk.Button(self.root, text="Hangman", command=self.launch_hangman).pack(pady=10)
        tk.Button(self.root, text="Connect Four", command=self.launch_connect_four).pack(pady=10)
        tk.Button(self.root, text="Snake", command=self.launch_snake).pack(pady=10)
        tk.Button(self.root, text="Pong", command=self.launch_pong).pack(pady=10)
        tk.Button(self.root, text="Sudoku", command=self.launch_sudoku).pack(pady=10)
        tk.Button(self.root, text="Minesweeper", command=self.launch_minesweeper).pack(pady=10)


    def launch_memory(self):
        top = tk.Toplevel(self.root)
        Memory(top,10,10)


    def launch_tic_tac_toe(self):
        top = tk.Toplevel(self.root)
        TicTacToe(top)


    def launch_rock_paper_scissors(self):
        top = tk.Toplevel(self.root)
        RockPaperScissors(top)


    def launch_number_guessing(self):
        top = tk.Toplevel(self.root)
        NumberGuessing(top)


    def launch_hangman(self):
        top = tk.Toplevel(self.root)
        Hangman(top)


    def launch_connect_four(self):
        top = tk.Toplevel(self.root)
        ConnectFour(top)


    def launch_snake(self):
        top = tk.Toplevel(self.root)
        Snake(top)


    def launch_pong(self):
        top = tk.Toplevel(self.root)
        Pong(top)


    def launch_sudoku(self):
        top = tk.Toplevel(self.root)
        Sudoku(top)
     
    def launch_minesweeper(self):
        top = tk.Toplevel(self.root)
        Minesweeper(top,10,10,25)

if __name__ == "__main__":
    root = tk.Tk()
    game_launcher = GameLauncher(root)
    root.mainloop()



