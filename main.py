import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

class MyApp(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))
        label = toga.Label("Hello, BeeWare!", style=Pack(padding=10))
        main_box.add(label)
        self.main_window = toga.MainWindow(title="My App")
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return MyApp()