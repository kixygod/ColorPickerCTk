import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ColorCodeApp:
    def __init__(self, master):
        self.master = master
        master.title("Определение кодировки цвета изображения")

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.load_button = tk.Button(master, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        self.color_label = tk.Label(master, text="Цвета:")
        self.color_label.pack()

        self.color_text = tk.Text(master, width=30, height=10)
        self.color_text.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((300, 300))  # Изменение размера изображения для отображения
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            colors = self.get_image_colors(image)
            self.show_colors(colors)

    def get_image_colors(self, image):
        colors = set()
        pixels = image.load()
        width, height = image.size
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                colors.add(pixel)
        return colors

    def show_colors(self, colors):
        self.color_text.delete(1.0, tk.END)
        for color in colors:
            hex_code = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            self.color_text.insert(tk.END, hex_code + '\n')

root = tk.Tk()
app = ColorCodeApp(root)
root.mainloop()
