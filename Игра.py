import tkinter as tk
from tkinter import messagebox
import random


class GuessNumberGame:
    def __init__(self, parent=None):
        """Инициализация игры"""
        if parent:
            # Если игра запускается из главного меню
            self.window = tk.Toplevel(parent)
            self.window.title("Угадай число")
            self.window.geometry("550x650")
            self.window.resizable(False, False)
            self.window.transient(parent)
            self.window.grab_set()
        else:
            # Если игра запускается отдельно
            self.window = tk.Tk()
            self.window.title("Угадай число")
            self.window.geometry("550x650")
            self.window.resizable(False, False)
        
        # Цветовая схема
        self.colors = {
            'bg': '#1a1a2e',
            'primary': '#16213e',
            'secondary': '#0f3460',
            'accent': '#e94560',
            'success': '#4caf50',
            'warning': '#ff9800',
            'text': '#eeeeee',
            'button': '#6c5ce7'
        }
        
        self.window.configure(bg=self.colors['bg'])
        
        # Игровые переменные
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 10
        self.min_range = 1
        self.max_range = 100
        self.game_active = False
        self.difficulty = "normal"
        
        self.create_widgets()
        self.new_game()
        
        # Обработка закрытия окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Закрытие окна игры"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти из игры?"):
            self.window.destroy()
    
    def create_widgets(self):
        """Создание интерфейса"""
        # Заголовок
        title_font = ("Helvetica", 26, "bold")
        title_label = tk.Label(
            self.window,
            text="🔢 УГАДАЙ ЧИСЛО 🔢",
            font=title_font,
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(pady=15)
        
        # Фрейм для информации
        self.info_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.info_frame.pack(pady=10)
        
        # Диапазон
        self.range_label = tk.Label(
            self.info_frame,
            text="Диапазон: 1 - 100",
            font=("Helvetica", 14),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.range_label.pack()
        
        # Попытки
        self.attempts_label = tk.Label(
            self.info_frame,
            text="Попыток осталось: 10",
            font=("Helvetica", 14),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.attempts_label.pack(pady=5)
        
        # Индикатор сложности
        self.difficulty_label = tk.Label(
            self.info_frame,
            text="Сложность: Нормальная",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['warning']
        )
        self.difficulty_label.pack()
        
        # Поле для ввода
        self.input_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.input_frame.pack(pady=15)
        
        self.input_label = tk.Label(
            self.input_frame,
            text="Введите число:",
            font=("Helvetica", 14),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.input_label.pack()
        
        self.entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 24),
            width=10,
            justify='center',
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda e: self.check_guess())
        
        # Кнопка проверки
        self.check_btn = tk.Button(
            self.input_frame,
            text="ПРОВЕРИТЬ",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['accent'],
            fg='white',
            activebackground='#ff6b6b',
            activeforeground='white',
            padx=30,
            pady=10,
            command=self.check_guess,
            cursor='hand2'
        )
        self.check_btn.pack(pady=10)
        
        # Фрейм для подсказок
        self.hint_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.hint_frame.pack(pady=15, fill=tk.BOTH, padx=20)
        
        self.hint_label = tk.Label(
            self.hint_frame,
            text="💡 Введите число и нажмите Проверить",
            font=("Helvetica", 11),
            bg=self.colors['primary'],
            fg=self.colors['text'],
            wraplength=450,
            padx=20,
            pady=12
        )
        self.hint_label.pack(fill=tk.BOTH)
        
        # Фрейм для истории
        self.history_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.history_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        history_title = tk.Label(
            self.history_frame,
            text="📜 История попыток:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        history_title.pack()
        
        self.history_text = tk.Text(
            self.history_frame,
            height=8,
            width=40,
            font=("Consolas", 10),
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            state=tk.DISABLED
        )
        self.history_text.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Фрейм для кнопок управления
        self.control_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.control_frame.pack(pady=15)
        
        # Кнопки сложности
        self.easy_btn = self.create_control_button(
            self.control_frame,
            "Легко",
            lambda: self.set_difficulty("easy"),
            hover='#6c5ce7'
        )
        self.easy_btn.pack(side=tk.LEFT, padx=5)
        
        self.normal_btn = self.create_control_button(
            self.control_frame,
            "Нормально",
            lambda: self.set_difficulty("normal"),
            hover='#6c5ce7'
        )
        self.normal_btn.pack(side=tk.LEFT, padx=5)
        
        self.hard_btn = self.create_control_button(
            self.control_frame,
            "Сложно",
            lambda: self.set_difficulty("hard"),
            hover='#6c5ce7'
        )
        self.hard_btn.pack(side=tk.LEFT, padx=5)
        
        # Новая игра
        self.new_game_btn = self.create_control_button(
            self.control_frame,
            "🔄 Новая игра",
            self.new_game,
            self.colors['success'],
            hover='#45a049'
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Подсказка
        self.hint_btn = self.create_control_button(
            self.control_frame,
            "💡 Подсказка",
            self.show_hint,
            self.colors['warning'],
            hover='#fb8c00'
        )
        self.hint_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка выхода
        self.exit_btn = self.create_control_button(
            self.control_frame,
            "🚪 Выход",
            self.on_closing,
            '#e74c3c',
            hover='#c0392b'
        )
        self.exit_btn.pack(side=tk.LEFT, padx=5)
    
    def create_control_button(self, parent, text, command, color=None, hover=None):
        """Создание кнопки управления"""
        if color is None:
            color = self.colors['secondary']
        if hover is None:
            hover = self.colors['accent']
        
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 10, "bold"),
            bg=color,
            fg='white',
            activebackground=hover,
            activeforeground='white',
            padx=15,
            pady=6,
            command=command,
            cursor='hand2'
        )
        return btn
    
    def set_difficulty(self, level):
        """Установка сложности"""
        if self.game_active:
            if messagebox.askyesno("Смена сложности", 
                                   "Игра уже начата. Начать новую игру с новой сложностью?"):
                self.difficulty = level
                self.new_game()
            return
        
        self.difficulty = level
        self.new_game()
    
    def new_game(self):
        """Начало новой игры"""
        # Устанавливаем параметры в зависимости от сложности
        if self.difficulty == "easy":
            self.min_range = 1
            self.max_range = 50
            self.max_attempts = 15
            self.difficulty_label.config(text="Сложность: Легкая 🟢")
        elif self.difficulty == "hard":
            self.min_range = 1
            self.max_range = 200
            self.max_attempts = 7
            self.difficulty_label.config(text="Сложность: Сложная 🔴")
        else:  # normal
            self.min_range = 1
            self.max_range = 100
            self.max_attempts = 10
            self.difficulty_label.config(text="Сложность: Нормальная 🟡")
        
        # Генерируем секретное число
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_active = True
        
        # Обновляем интерфейс
        self.range_label.config(text=f"Диапазон: {self.min_range} - {self.max_range}")
        self.update_attempts_label()
        self.entry.delete(0, tk.END)
        self.entry.config(state=tk.NORMAL)
        self.check_btn.config(state=tk.NORMAL)
        
        # Очищаем историю
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        # Обновляем подсказку
        self.hint_label.config(
            text=f"💡 Я загадал число от {self.min_range} до {self.max_range}. У тебя {self.max_attempts} попыток!",
            bg=self.colors['primary']
        )
        
        # Фокус на поле ввода
        self.entry.focus()
    
    def update_attempts_label(self):
        """Обновление счетчика попыток"""
        remaining = self.max_attempts - self.attempts
        self.attempts_label.config(text=f"Попыток осталось: {remaining}")
        
        # Меняем цвет при малом количестве попыток
        if remaining <= 3:
            self.attempts_label.config(fg=self.colors['accent'])
        else:
            self.attempts_label.config(fg=self.colors['text'])
    
    def check_guess(self):
        """Проверка введенного числа"""
        if not self.game_active:
            messagebox.showinfo("Игра окончена", "Начните новую игру!")
            return
        
        # Получаем число из поля ввода
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите целое число!")
            self.entry.delete(0, tk.END)
            return
        
        # Проверяем диапазон
        if guess < self.min_range or guess > self.max_range:
            messagebox.showwarning("Вне диапазона", 
                                  f"Пожалуйста, введите число от {self.min_range} до {self.max_range}!")
            self.entry.delete(0, tk.END)
            return
        
        self.attempts += 1
        remaining = self.max_attempts - self.attempts
        
        # Добавляем в историю
        self.add_to_history(guess)
        
        # Проверяем угадал ли игрок
        if guess == self.secret_number:
            self.game_won()
            return
        
        # Проверяем закончились ли попытки
        if self.attempts >= self.max_attempts:
            self.game_lost()
            return
        
        # Даем подсказку
        if guess < self.secret_number:
            hint = f"📈 Число {guess} - МАЛЕНЬКОЕ! Попробуй больше."
            self.hint_label.config(text=hint, bg=self.colors['primary'])
        else:
            hint = f"📉 Число {guess} - БОЛЬШОЕ! Попробуй меньше."
            self.hint_label.config(text=hint, bg=self.colors['primary'])
        
        # Обновляем счетчик попыток
        self.update_attempts_label()
        
        # Очищаем поле ввода
        self.entry.delete(0, tk.END)
        self.entry.focus()
        
        # Эффект мигания
        self.flash_hint()
    
    def add_to_history(self, guess):
        """Добавление попытки в историю"""
        self.history_text.config(state=tk.NORMAL)
        
        if guess < self.secret_number:
            arrow = "⬆️"
            hint = "мало"
        elif guess > self.secret_number:
            arrow = "⬇️"
            hint = "много"
        else:
            arrow = "🎯"
            hint = "угадал!"
        
        history_entry = f"Попытка {self.attempts}: {guess:3d} {arrow} ({hint})\n"
        
        self.history_text.insert(1.0, history_entry)
        self.history_text.config(state=tk.DISABLED)
    
    def game_won(self):
        """Победа игрока"""
        self.game_active = False
        self.entry.config(state=tk.DISABLED)
        self.check_btn.config(state=tk.DISABLED)
        
        # Показываем поздравление
        message = f"🎉 ПОЗДРАВЛЯЮ! 🎉\n\nВы угадали число {self.secret_number}!\nКоличество попыток: {self.attempts}\n"
        
        # Оценка результата
        success_rate = self.attempts / self.max_attempts
        if success_rate <= 0.3:
            message += "\n⭐ ИДЕАЛЬНО! Вы гений! ⭐"
        elif success_rate <= 0.6:
            message += "\n🌟 ОТЛИЧНО! Вы хорошо справились! 🌟"
        else:
            message += "\n👍 НЕПЛОХО! В следующий раз будет еще лучше! 👍"
        
        messagebox.showinfo("Победа!", message)
        
        # Обновляем подсказку
        self.hint_label.config(
            text=f"🎉 ПОБЕДА! Загаданное число было {self.secret_number}! 🎉",
            bg=self.colors['success']
        )
    
    def game_lost(self):
        """Поражение игрока"""
        self.game_active = False
        self.entry.config(state=tk.DISABLED)
        self.check_btn.config(state=tk.DISABLED)
        
        message = f"😔 ИГРА ОКОНЧЕНА 😔\n\nЗагаданное число было: {self.secret_number}\n\nПопробуйте еще раз!"
        
        messagebox.showinfo("Попытки закончились", message)
        
        # Обновляем подсказку
        self.hint_label.config(
            text=f"😔 Игра окончена! Загаданное число: {self.secret_number}. Начните новую игру!",
            bg=self.colors['accent']
        )
    
    def show_hint(self):
        """Показать подсказку"""
        if not self.game_active:
            messagebox.showinfo("Подсказка", "Начните новую игру, чтобы получить подсказку!")
            return
        
        # Простая подсказка
        hint_text = f"🔍 Подсказка: число находится между {self.min_range} и {self.max_range}\n\n"
        
        if self.attempts > 0:
            # Анализируем предыдущие попытки
            hint_text += f"📊 Вы уже использовали {self.attempts} из {self.max_attempts} попыток\n"
            hint_text += f"🎯 Попробуйте числа ближе к середине диапазона"
        
        messagebox.showinfo("Подсказка", hint_text)
    
    def flash_hint(self):
        """Эффект мигания подсказки"""
        def reset_color():
            self.hint_label.config(bg=self.colors['primary'])
        
        self.hint_label.config(bg=self.colors['accent'])
        self.window.after(200, reset_color)
    
    def run(self):
        """Запуск игры"""
        self.window.mainloop()


class GameLauncher:
    """Главное меню для запуска игр"""
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Игровой центр")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Цветовая схема
        self.colors = {
            'bg': '#1a1a2e',
            'primary': '#16213e',
            'accent': '#e94560',
            'success': '#4caf50',
            'warning': '#ff9800',
            'text': '#eeeeee'
        }
        
        self.window.configure(bg=self.colors['bg'])
        
        self.create_widgets()
        
        # Обработка закрытия
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Создание интерфейса главного меню"""
        # Заголовок
        title_font = ("Helvetica", 28, "bold")
        title = tk.Label(
            self.window,
            text="🎮 ИГРОВОЙ ЦЕНТР 🎮",
            font=title_font,
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title.pack(pady=30)
        
        # Подзаголовок
        subtitle = tk.Label(
            self.window,
            text="Выберите игру:",
            font=("Helvetica", 16),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        subtitle.pack(pady=10)
        
        # Фрейм для кнопок игр
        games_frame = tk.Frame(self.window, bg=self.colors['bg'])
        games_frame.pack(pady=30)
        
        # Кнопка игры в крестики-нолики
        tictactoe_btn = self.create_game_button(
            games_frame,
            "❌ Крестики-нолики ⭕",
            self.launch_tictactoe,
            self.colors['success']
        )
        tictactoe_btn.pack(pady=10)
        
        # Кнопка игры "Угадай число"
        guess_btn = self.create_game_button(
            games_frame,
            "🔢 Угадай число 🎯",
            self.launch_guess_number,
            self.colors['warning']
        )
        guess_btn.pack(pady=10)
        
        # Кнопка выхода
        exit_btn = self.create_game_button(
            games_frame,
            "🚪 Выход",
            self.on_closing,
            '#e74c3c'
        )
        exit_btn.pack(pady=30)
        
        # Информационная строка
        info = tk.Label(
            self.window,
            text="© 2024 Игровой центр | Все игры бесплатны",
            font=("Helvetica", 9),
            bg=self.colors['bg'],
            fg='#7f8c8d'
        )
        info.pack(side=tk.BOTTOM, pady=10)
    
    def create_game_button(self, parent, text, command, color):
        """Создание стилизованной кнопки игры"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 14, "bold"),
            bg=color,
            fg='white',
            activebackground=self.colors['accent'],
            activeforeground='white',
            width=25,
            height=2,
            command=command,
            cursor='hand2'
        )
        
        # Эффект наведения
        def on_enter(e):
            btn['background'] = self.colors['accent']
        
        def on_leave(e):
            btn['background'] = color
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def launch_tictactoe(self):
        """Запуск игры в крестики-нолики"""
        try:
            # Импортируем игру в крестики-нолики
            from tictactoe_gui import TicTacToeGUI
            TicTacToeGUI(self.window)
        except ImportError:
            # Если игра не найдена, показываем сообщение
            messagebox.showinfo("Информация", 
                               "Игра 'Крестики-нолики' будет доступна после добавления файла tictactoe_gui.py")
    
    def launch_guess_number(self):
        """Запуск игры 'Угадай число'"""
        try:
            guess_game = GuessNumberGame(self.window)
            guess_game.run()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить игру: {str(e)}")
    
    def on_closing(self):
        """Закрытие приложения"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти из игрового центра?"):
            self.window.destroy()
    
    def run(self):
        """Запуск главного меню"""
        self.window.mainloop()


if __name__ == "__main__":
    # Запускаем главное меню
    launcher = GameLauncher()
    launcher.run()