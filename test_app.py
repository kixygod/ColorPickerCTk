import unittest

from app import App, UserImage


class TestApp(unittest.TestCase):
    def test_colors(self):
        app = App()
        self.test_colors_list = app.user_image.colors
        self.assertEqual(len(self.test_colors_list), 0)

    def test_none_image_label(self):
        app = App()
        self.test_image_label = app.user_image.image_label
        self.assertEqual(app.user_image.image_label.cget("image"), None)
