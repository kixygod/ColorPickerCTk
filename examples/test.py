import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")

        # Создание кнопки "Открыть изображение"
        self.btn_open = tk.Button(
            self.root, text="Открыть изображение", command=self.open_image)
        self.btn_open.pack()

        # Создание холста для отображения изображения
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack(side=tk.LEFT)

        # Создание фрейма для списка нажатых цветов
        self.frame_colors = tk.Frame(self.root)
        self.frame_colors.pack(side=tk.RIGHT, padx=10)

        # Список для хранения нажатых цветов
        self.clicked_colors = []

    def open_image(self):
        # Открыть диалоговое окно для выбора изображения
        self.image_path = filedialog.askopenfilename(initialdir="./", title="Выберите изображение",
                                                     filetypes=(("Файлы изображений", "*.png;*.jpg;*.jpeg"),))

        # Отобразить изображение на холсте
        if self.image_path:
            image = Image.open(self.image_path)
            image = image.resize((400, 400))
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def get_color(self, event):
        if self.image_path:
            # Получить координаты щелчка мыши
            x = event.x
            y = event.y

            # Загрузить изображение и получить цвет пикселя
            image = Image.open(self.image_path)
            rgb = image.convert("RGB").getpixel((x, y))

            # Преобразовать RGB-значение в шестнадцатеричный код цвета
            color_code = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

            # Добавить цвет в список нажатых цветов
            self.clicked_colors.append(color_code)

            # Создать квадратик с выбранным цветом
            self.create_color_square(color_code)

    def create_color_square(self, color_code):
        # Создать фрейм для отображения цвета
        frame = tk.Frame(self.frame_colors, padx=5, pady=5)
        frame.pack(anchor="w")

        # Создать квадратик с цветом
        square = tk.Label(frame, width=10, height=3, bg=color_code)
        square.pack(side=tk.LEFT)

        # Создать метку с кодом цвета
        lbl_code = tk.Label(frame, text=color_code)
        lbl_code.pack(side=tk.LEFT)

    def clear_clicked_colors(self):
        # Очистить список нажатых цветов
        self.clicked_colors = []

        # Удалить все фреймы с цветами
        for child in self.frame_colors.winfo_children():
            child.destroy()

    def save_clicked_colors(self):
        # Сохранить список нажатых цветов в файл
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=(
                                                    ("Текстовые файлы", "*.txt"),),
                                                initialdir="./",
                                                title="Сохранить список нажатых цветов")

        if filename:
            with open(filename, "w") as file:
                file.write("\n".join(self.clicked_colors))


# Создание экземпляра класса приложения Tkinter
root = tk.Tk()

# Создание экземпляра приложения ColorPickerApp
app = ColorPickerApp(root)

# Создание кнопок для очистки списка нажатых цветов и сохранения списка
btn_clear = tk.Button(
    root, text="Очистить список", command=app.clear_clicked_colors)
btn_clear.pack()

btn_save = tk.Button(
    root, text="Сохранить список", command=app.save_clicked_colors)
btn_save.pack()

# Привязка обработчика событий щелчка мыши на холсте
app.canvas.bind("<Button-1>", app.get_color)

# Запуск главного цикла событий
root.mainloop()
