#Color Picker

![Dark theme](screenshots\dark.png)
![Light theme](screenshots\light.png)
Данное приложение было разработано на языке Python с помощью библиотеки Custom Tkinter. Основная задача данного приложения помощь в подбирании цветов с любой фотографии.
Руководство использования:

1. Перейдите во вкладку 'Pick the color';
2. Далее нажмите на кнопку в правом верхнем углу 'Upload photo';
3. После этого мы можете кликнуть в любом месте загруженной фотографии, чтобы узнать код цвета.

Данное приложение было разработано для учебы, в частности для предмета 'Объектно-ориентированнео программирование', студентом 421-4 группы, Алимьевым Иваном

##How to run

```bash
cd ColorPickerCTk
pip install virtualenv
.\env\Scripts\activate
pip install -r .\requirements.txt
python -u .\app.py
```

Чтобы использовать тесты

```bash
python -m unittest .\test_app.py
```
