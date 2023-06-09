import os
import tkinter as tk
from tkinter import filedialog

import customtkinter
from PIL import Image


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")
        self.minsize(300, 150)
        self.maxsize(300, 150)
        self.title("Color Picker - About")

        self.about_text = customtkinter.CTkTextbox(
            self,
            font=(tuple, 14),
            fg_color="transparent",
            activate_scrollbars=False,
        )
        self.about_text.pack()
        self.about_text.insert(
            "0.0",
            "Данное приложение было разработано для учебы, в частности для предмета 'Объектно-ориентированнео программирование', студентом 421-4 группы, Алимьевым Иваном",
        )
        self.about_text.configure(state="disabled")


class About:
    def __init__(self, parent_frame, roditel_frame):
        self.parent_frame = parent_frame
        self.roditel_frame = roditel_frame
        self.frame_2_button = customtkinter.CTkButton(
            self.parent_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="About",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.open_toplevel,
        )
        self.frame_2_button.grid(row=3, column=0, sticky="nsew")

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self.roditel_frame)
        else:
            self.toplevel_window.focus()
        self.toplevel_window.focus()


class UserImage:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.right_panel = customtkinter.CTkFrame(self.parent_frame, corner_radius=0)
        self.right_panel.grid(
            row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        self.upload_photo_button = customtkinter.CTkButton(
            self.right_panel, text="Upload photo", command=self.load_image
        )
        self.upload_photo_button.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.right_panel, label_text="Цвета"
        )
        self.scrollable_frame.grid(
            row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.about_button = About(self.right_panel, parent_frame)
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.right_panel,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.set("System")
        self.appearance_mode_menu.grid(row=2, column=0, padx=20, pady=20, sticky="s")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.colors = []
        self.scrollable_frame_boxes = []

        self.photo_frame = customtkinter.CTkFrame(self.parent_frame, corner_radius=0)
        self.photo_frame.grid(
            row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        self.photo_frame.grid_rowconfigure(0, weight=1)
        self.photo_frame.grid_columnconfigure(0, weight=1)

        self.image_label = customtkinter.CTkLabel(self.photo_frame, text="")
        self.image_label.grid(row=0, column=0, pady=0, padx=0)
        self.image_label.bind("<Button-1>", self.get_color)
        self.index_line = 0

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")]
        )
        if self.file_path:
            self.image = Image.open(self.file_path)

            self.parent_frame_width = self.photo_frame.winfo_width()
            self.parent_frame_height = self.photo_frame.winfo_height()
            print(f"self.parent_frame_width = {self.parent_frame_width}")
            print(f"self.parent_frame_height = {self.parent_frame_height}")
            self.parent_frame_aspect_ratio = (
                self.parent_frame_width / self.parent_frame_height
            )

            # Определение желаемой ширины и высоты картинки с сохранением пропорций
            if self.image.width / self.image.height >= self.parent_frame_aspect_ratio:
                self.desired_width = self.parent_frame_width
                self.desired_height = int(
                    self.parent_frame_width / self.image.width * self.image.height
                )
            else:
                self.desired_height = self.parent_frame_height
                self.desired_width = int(
                    self.parent_frame_height / self.image.height * self.image.width
                )

            self.photo = customtkinter.CTkImage(
                light_image=self.image,
                dark_image=self.image,
                size=(self.desired_width, self.desired_height),
            )
            self.image_label.configure(image=self.photo)
            self.resized_image = self.image.resize(
                (self.desired_width, self.desired_height), Image.BICUBIC
            )
            print(self.desired_width)
            print(self.desired_height)

    def get_color(self, event):
        if self.file_path:
            x = event.x
            y = event.y
            print(f"x = {x}")
            print(f"y = {y}")
            print(f"image_label_x = {self.image_label.winfo_x()}")
            print(f"image_label_y = {self.image_label.winfo_y()}")
            rgb = self.resized_image.convert("RGB").getpixel((x, y))
            color_code = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
            self.colors.append(color_code)
            self.create_line(color_code)

    def create_line(self, color_code):
        color_label = customtkinter.CTkLabel(
            self.scrollable_frame, bg_color=color_code, text="", width=70, height=50
        )
        color_label.grid(
            row=self.index_line, column=0, padx=(10, 10), pady=(10, 10), sticky="w"
        )
        code_label = customtkinter.CTkLabel(self.scrollable_frame, text=color_code)
        code_label.grid(
            row=self.index_line, column=1, padx=(10, 10), pady=(10, 10), sticky="e"
        )
        self.index_line += 1


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Picker")
        self.geometry("1280x720")
        self.minsize(800, 600)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        customtkinter.set_default_color_theme("green")

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        self.about_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "about_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "about_light.png")),
            size=(20, 20),
        )
        self.color_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "color-picker_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "color-picker_light.png")),
            size=(20, 20),
        )

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.user_image = UserImage(self.home_frame)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")

    def home_button_event(self):
        self.select_frame_by_name("home")


if __name__ == "__main__":
    app = App()
    app.mainloop()
