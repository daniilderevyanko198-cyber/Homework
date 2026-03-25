import tkinter as tk
from tkinter import messagebox, font
import random


class TicTacToe:
    def __init__(self):
        """Инициализация игровой логики"""
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
    
    def available_moves(self):
        """Возвращает список доступных ходов"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        """Проверка, остались ли пустые клетки"""
        return ' ' in self.board
    
    def make_move(self, square, letter):
        """Выполнение хода"""
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        """Проверка победы"""
        # Проверка строк
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Проверка столбцов
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Проверка диагоналей
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False
    
    def reset(self):
        """Сброс игры"""
        self.board = [' ' for _ in range(9)]
        self.current_winner = None


class TicTacToeGUI:
    def __init__(self):
        """Инициализация графического интерфейса"""
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.geometry("500x650")
        self.window.resizable(False, False)
        
        # Настройка цветовой схемы
        self.colors = {
            'bg': '#2c3e50',
            'board': '#34495e',
            'cell': '#ecf0f1',
            'x': '#e74c3c',
            'o': '#3498db',
            'button': '#27ae60',
            'button_hover': '#229954'
        }
        
        self.window.configure(bg=self.colors['bg'])
        
        # Игровые переменные
        self.game = TicTacToe()
        self.buttons = []
        self.mode = None  # 'friend' или 'computer'
        self.player_letter = None  # 'X' или 'O'
        self.computer_letter = None
        self.player_turn = True
        self.game_active = False
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Заголовок
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(
            self.window,
            text="КРЕСТИКИ-НОЛИКИ",
            font=title_font,
            bg=self.colors['bg'],
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Фрейм для информации
        self.info_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.info_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            self.info_frame,
            text="Выберите режим игры",
            font=("Helvetica", 14),
            bg=self.colors['bg'],
            fg='white'
        )
        self.status_label.pack()
        
        # Фрейм для игрового поля
        self.board_frame = tk.Frame(self.window, bg=self.colors['board'])
        self.board_frame.pack(pady=20, padx=20)
        
        # Создание кнопок игрового поля
        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text='',
                font=("Helvetica", 32, "bold"),
                width=3,
                height=1,
                bg=self.colors['cell'],
                activebackground='#bdc3c7',
                relief=tk.RAISED,
                bd=3,
                command=lambda idx=i: self.make_move(idx)
            )
            button.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(button)
        
        # Фрейм для кнопок управления
        self.control_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.control_frame.pack(pady=20)
        
        # Кнопки режимов игры
        self.friend_btn = self.create_button(
            self.control_frame,
            "Игра с другом",
            lambda: self.start_game('friend')
        )
        self.friend_btn.pack(side=tk.LEFT, padx=10)
        
        self.computer_btn = self.create_button(
            self.control_frame,
            "Игра с компьютером",
            lambda: self.start_computer_game()
        )
        self.computer_btn.pack(side=tk.LEFT, padx=10)
        
        # Кнопка сброса
        self.reset_btn = self.create_button(
            self.control_frame,
            "Новая игра",
            self.reset_game,
            bg='#e67e22',
            hover='#d35400'
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
    def create_button(self, parent, text, command, bg='#27ae60', hover='#229954'):
        """Создание стилизованной кнопки"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg=bg,
            fg='white',
            activebackground=hover,
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2',
            command=command
        )
        
        # Эффект наведения
        def on_enter(e):
            btn['background'] = hover
        
        def on_leave(e):
            btn['background'] = bg
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def start_computer_game(self):
        """Начало игры с компьютером - выбор символа и очередности"""
        # Создаем окно выбора
        choice_window = tk.Toplevel(self.window)
        choice_window.title("Настройки игры")
        choice_window.geometry("350x250")
        choice_window.configure(bg=self.colors['bg'])
        choice_window.resizable(False, False)
        
        # Центрируем окно
        choice_window.transient(self.window)
        choice_window.grab_set()
        
        # Заголовок
        tk.Label(
            choice_window,
            text="Настройки игры",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['bg'],
            fg='white'
        ).pack(pady=15)
        
        # Выбор символа
        tk.Label(
            choice_window,
            text="Выберите символ:",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg='white'
        ).pack(pady=5)
        
        symbol_frame = tk.Frame(choice_window, bg=self.colors['bg'])
        symbol_frame.pack(pady=5)
        
        def set_symbol(symbol):
            self.player_letter = symbol
            self.computer_letter = 'O' if symbol == 'X' else 'X'
            symbol_btn_x.config(state=tk.DISABLED)
            symbol_btn_o.config(state=tk.DISABLED)
            enable_first_move()
        
        symbol_btn_x = tk.Button(
            symbol_frame,
            text="X (крестик)",
            font=("Helvetica", 11),
            bg='#e74c3c',
            fg='white',
            padx=15,
            pady=5,
            command=lambda: set_symbol('X')
        )
        symbol_btn_x.pack(side=tk.LEFT, padx=10)
        
        symbol_btn_o = tk.Button(
            symbol_frame,
            text="O (нолик)",
            font=("Helvetica", 11),
            bg='#3498db',
            fg='white',
            padx=15,
            pady=5,
            command=lambda: set_symbol('O')
        )
        symbol_btn_o.pack(side=tk.LEFT, padx=10)
        
        # Выбор очередности
        first_frame = tk.Frame(choice_window, bg=self.colors['bg'])
        first_frame.pack(pady=15)
        
        tk.Label(
            first_frame,
            text="Кто ходит первым:",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg='white'
        ).pack()
        
        first_buttons = tk.Frame(first_frame, bg=self.colors['bg'])
        first_buttons.pack(pady=5)
        
        def set_first_move(player_first):
            self.player_turn = player_first
            self.start_game('computer')
            choice_window.destroy()
        
        def enable_first_move():
            # Активируем кнопки выбора очередности только после выбора символа
            player_btn = tk.Button(
                first_buttons,
                text="Игрок",
                font=("Helvetica", 11),
                bg=self.colors['button'],
                fg='white',
                padx=15,
                pady=5,
                state=tk.NORMAL,
                command=lambda: set_first_move(True)
            )
            player_btn.pack(side=tk.LEFT, padx=10)
            
            computer_btn = tk.Button(
                first_buttons,
                text="Компьютер",
                font=("Helvetica", 11),
                bg=self.colors['button'],
                fg='white',
                padx=15,
                pady=5,
                state=tk.NORMAL,
                command=lambda: set_first_move(False)
            )
            computer_btn.pack(side=tk.LEFT, padx=10)
        
        # Изначально кнопки выбора очередности неактивны
        player_btn = tk.Button(
            first_buttons,
            text="Игрок",
            font=("Helvetica", 11),
            bg=self.colors['button'],
            fg='white',
            padx=15,
            pady=5,
            state=tk.DISABLED,
            command=lambda: set_first_move(True)
        )
        player_btn.pack(side=tk.LEFT, padx=10)
        
        computer_btn = tk.Button(
            first_buttons,
            text="Компьютер",
            font=("Helvetica", 11),
            bg=self.colors['button'],
            fg='white',
            padx=15,
            pady=5,
            state=tk.DISABLED,
            command=lambda: set_first_move(False)
        )
        computer_btn.pack(side=tk.LEFT, padx=10)
    
    def start_game(self, mode):
        """Начало игры"""
        self.mode = mode
        self.game_active = True
        self.reset_game(keep_mode=True)
        
        # Обновляем статус
        if mode == 'friend':
            self.status_label.config(text="Игрок X ходит первым")
        else:
            if self.player_turn:
                self.status_label.config(text=f"Ваш ход ( {self.player_letter} )")
            else:
                self.status_label.config(text="Ход компьютера...")
                self.window.after(500, self.computer_move)
    
    def make_move(self, position):
        """Обработка хода игрока"""
        if not self.game_active:
            return
        
        # Проверка, чей ход
        current_letter = None
        if self.mode == 'friend':
            # Определяем, чей ход по количеству ходов
            x_count = self.game.board.count('X')
            o_count = self.game.board.count('O')
            current_letter = 'X' if x_count == o_count else 'O'
        else:
            if not self.player_turn:
                return
            current_letter = self.player_letter
        
        # Проверяем, свободна ли клетка
        if self.game.board[position] != ' ':
            return
        
        # Делаем ход
        self.game.make_move(position, current_letter)
        self.buttons[position].config(text=current_letter)
        
        # Меняем цвет текста
        if current_letter == 'X':
            self.buttons[position].config(fg=self.colors['x'])
        else:
            self.buttons[position].config(fg=self.colors['o'])
        
        self.buttons[position].config(state=tk.DISABLED)
        
        # Проверяем победу или ничью
        if self.game.current_winner:
            self.end_game(f"Победил {current_letter}!")
            return
        elif not self.game.empty_squares():
            self.end_game("Ничья!")
            return
        
        # Меняем ход
        if self.mode == 'friend':
            next_letter = 'O' if current_letter == 'X' else 'X'
            self.status_label.config(text=f"Ход игрока {next_letter}")
        else:
            self.player_turn = False
            self.status_label.config(text="Ход компьютера...")
            self.window.after(500, self.computer_move)
    
    def computer_move(self):
        """Ход компьютера"""
        if not self.game_active or self.player_turn or self.game.current_winner:
            return
        
        # Простой AI для компьютера
        move = self.get_computer_move()
        
        if move is not None:
            self.game.make_move(move, self.computer_letter)
            self.buttons[move].config(text=self.computer_letter)
            
            if self.computer_letter == 'X':
                self.buttons[move].config(fg=self.colors['x'])
            else:
                self.buttons[move].config(fg=self.colors['o'])
            
            self.buttons[move].config(state=tk.DISABLED)
            
            # Проверяем победу или ничью
            if self.game.current_winner:
                self.end_game(f"Компьютер победил!")
                return
            elif not self.game.empty_squares():
                self.end_game("Ничья!")
                return
            
            self.player_turn = True
            self.status_label.config(text=f"Ваш ход ( {self.player_letter} )")
    
    def get_computer_move(self):
        """Выбор хода компьютера"""
        # 1. Проверить, может ли компьютер выиграть
        for move in self.game.available_moves():
            if self.game.make_move(move, self.computer_letter):
                if self.game.current_winner == self.computer_letter:
                    self.game.board[move] = ' '
                    self.game.current_winner = None
                    return move
                self.game.board[move] = ' '
        
        # 2. Проверить, может ли игрок выиграть (заблокировать)
        for move in self.game.available_moves():
            if self.game.make_move(move, self.player_letter):
                if self.game.current_winner == self.player_letter:
                    self.game.board[move] = ' '
                    self.game.current_winner = None
                    return move
                self.game.board[move] = ' '
        
        # 3. Занять центр, если свободен
        if 4 in self.game.available_moves():
            return 4
        
        # 4. Занять угол
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if c in self.game.available_moves()]
        if available_corners:
            return random.choice(available_corners)
        
        # 5. Занять любую доступную клетку
        if self.game.available_moves():
            return random.choice(self.game.available_moves())
        
        return None
    
    def end_game(self, message):
        """Завершение игры"""
        self.game_active = False
        self.status_label.config(text=message)
        
        # Блокируем все кнопки
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        
        # Показываем сообщение
        if "Ничья" in message:
            messagebox.showinfo("Игра окончена", message)
        else:
            messagebox.showinfo("Победа!", message)
    
    def reset_game(self, keep_mode=False):
        """Сброс игры"""
        self.game.reset()
        
        # Очищаем кнопки
        for button in self.buttons:
            button.config(text='', state=tk.NORMAL, fg='black')
        
        if not keep_mode:
            self.mode = None
            self.game_active = False
            self.status_label.config(text="Выберите режим игры")
            # Разблокируем кнопки выбора режима
            self.friend_btn.config(state=tk.NORMAL)
            self.computer_btn.config(state=tk.NORMAL)
        else:
            self.game_active = True
            # Блокируем кнопки выбора режима во время игры
            self.friend_btn.config(state=tk.DISABLED)
            self.computer_btn.config(state=tk.DISABLED)
            
            if self.mode == 'friend':
                self.status_label.config(text="Игрок X ходит первым")
            else:
                if self.player_turn:
                    self.status_label.config(text=f"Ваш ход ( {self.player_letter} )")
                else:
                    self.status_label.config(text="Ход компьютера...")
                    self.window.after(500, self.computer_move)
    
    def run(self):
        """Запуск приложения"""
        self.window.mainloop()


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()