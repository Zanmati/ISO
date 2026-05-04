import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = "trainings.json"

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")

        self.trainings = []

        # === Форма ===
        tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Тип тренировки").grid(row=1, column=0)
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=1, column=1)

        tk.Label(root, text="Длительность (мин)").grid(row=2, column=0)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1)

        tk.Button(root, text="Добавить тренировку", command=self.add_training)\
            .grid(row=3, column=0, columnspan=2)

        # === Фильтры ===
        tk.Label(root, text="Фильтр по типу").grid(row=4, column=0)
        self.filter_type = tk.Entry(root)
        self.filter_type.grid(row=4, column=1)

        tk.Label(root, text="Фильтр по дате").grid(row=5, column=0)
        self.filter_date = tk.Entry(root)
        self.filter_date.grid(row=5, column=1)

        tk.Button(root, text="Применить фильтр", command=self.apply_filter)\
            .grid(row=6, column=0, columnspan=2)

        # === Таблица ===
        self.tree = ttk.Treeview(root, columns=("date", "type", "duration"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность")

        self.tree.grid(row=7, column=0, columnspan=2)

        # === Кнопки JSON ===
        tk.Button(root, text="Сохранить", command=self.save_data)\
            .grid(row=8, column=0)
        tk.Button(root, text="Загрузить", command=self.load_data)\
            .grid(row=8, column=1)

    # === Проверка данных ===
    def validate(self, date, duration):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            messagebox.showerror("Ошибка", "Неверный формат даты!")
            return False

        if not duration.isdigit() or int(duration) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return False

        return True

    # === Добавление ===
    def add_training(self):
        date = self.date_entry.get()
        t_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate(date, duration):
            return

        training = {
            "date": date,
            "type": t_type,
            "duration": duration
        }

        self.trainings.append(training)
        self.update_table(self.trainings)

    # === Обновление таблицы ===
    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for t in data:
            self.tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))

    # === Фильтрация ===
    def apply_filter(self):
        t_type = self.filter_type.get()
        date = self.filter_date.get()

        filtered = self.trainings

        if t_type:
            filtered = [t for t in filtered if t_type.lower() in t["type"].lower()]

        if date:
            filtered = [t for t in filtered if date in t["date"]]

        self.update_table(filtered)

    # === Сохранение ===
    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.trainings, f, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены!")

    # === Загрузка ===
    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.trainings = json.load(f)
            self.update_table(self.trainings)
        except:
            messagebox.showerror("Ошибка", "Файл не найден!")

# === Запуск ===
root = tk.Tk()
app = TrainingPlanner(root)
root.mainloop()