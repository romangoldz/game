from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import random

Window.size = (400, 600)  # Розмір вікна для зручності

class ClickerGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)
        
        # Рядок з рахунком та рекордом
        score_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        self.score_label = Label(text='Рахунок: 0', font_size='28sp', bold=True)
        self.record_label = Label(text='Рекорд: 0', font_size='20sp', color=(0.8, 0.8, 0, 1))
        score_layout.add_widget(self.score_label)
        score_layout.add_widget(self.record_label)
        self.add_widget(score_layout)
        
        # Кнопка для кліків (головний елемент)
        self.click_btn = Button(
            text='ТИСНИ МЕНЕ!',
            font_size='32sp',
            background_color=(0.2, 0.6, 1, 1),
            size_hint=(1, 0.5)
        )
        self.click_btn.bind(on_press=self.on_click)
        self.add_widget(self.click_btn)
        
        # Інформаційна панель
        info_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        self.combo_label = Label(text='Комбо: 1x', font_size='20sp')
        self.timer_label = Label(text='Час: 0.0с', font_size='20sp')
        info_layout.add_widget(self.combo_label)
        info_layout.add_widget(self.timer_label)
        self.add_widget(info_layout)
        
        # Кнопки керування
        control_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        reset_btn = Button(text='Скинути', font_size='18sp', background_color=(1, 0.3, 0.3, 1))
        reset_btn.bind(on_press=self.reset_game)
        control_layout.add_widget(reset_btn)
        
        self.auto_btn = Button(text='Авто-клік: Вимк.', font_size='18sp', background_color=(0.4, 0.4, 0.4, 1))
        self.auto_btn.bind(on_press=self.toggle_auto)
        control_layout.add_widget(self.auto_btn)
        self.add_widget(control_layout)
        
        # Стан гри
        self.score = 0
        self.record = 0
        self.combo = 1
        self.time = 0.0
        self.is_auto = False
        self.auto_event = None
        self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)
        
        # Завантажуємо рекорд (зберігається в пам'яті)
        self.load_record()
    
    def on_click(self, instance):
        """Обробка кліку по кнопці"""
        self.score += self.combo
        self.combo += 0.2  # Поступове збільшення комбо
        self.update_score()
        
        # Візуальний ефект - зміна кольору
        self.click_btn.background_color = (
            random.uniform(0.2, 0.8),
            random.uniform(0.4, 1),
            random.uniform(0.2, 0.8),
            1
        )
        # Повертаємо колір через 0.1с
        Clock.schedule_once(lambda dt: setattr(self.click_btn, 'background_color', (0.2, 0.6, 1, 1)), 0.1)
    
    def update_score(self):
        """Оновлює відображення рахунку та рекорду"""
        self.score_label.text = f'Рахунок: {int(self.score)}'
        self.combo_label.text = f'Комбо: {self.combo:.1f}x'
        if self.score > self.record:
            self.record = self.score
            self.record_label.text = f'Рекорд: {int(self.record)}'
            self.save_record()
    
    def update_timer(self, dt):
        """Оновлює таймер гри"""
        self.time += dt
        self.timer_label.text = f'Час: {self.time:.1f}с'
    
    def reset_game(self, instance):
        """Скидання гри"""
        self.score = 0
        self.combo = 1
        self.time = 0.0
        self.click_btn.background_color = (0.2, 0.6, 1, 1)
        self.update_score()
        self.timer_label.text = 'Час: 0.0с'
        self.combo_label.text = 'Комбо: 1x'
        
        # Якщо авто-клік увімкнено - вимикаємо
        if self.is_auto:
            self.toggle_auto(None)
    
    def toggle_auto(self, instance):
        """Вмикає/вимикає автоматичний клік"""
        self.is_auto = not self.is_auto
        self.auto_btn.text = f'Авто-клік: {"Увімк." if self.is_auto else "Вимк."}'
        self.auto_btn.background_color = (0.2, 0.8, 0.2, 1) if self.is_auto else (0.4, 0.4, 0.4, 1)
        
        if self.is_auto:
            self.auto_event = Clock.schedule_interval(lambda dt: self.on_click(None), 0.3)
        else:
            if self.auto_event:
                self.auto_event.cancel()
                self.auto_event = None
    
    def load_record(self):
        """Завантажує рекорд (тут просто ініціалізація)"""
        # В реальному додатку тут було б завантаження з файлу
        self.record = 0
        self.record_label.text = f'Рекорд: {self.record}'
    
    def save_record(self):
        """Зберігає рекорд (тут просто заглушка)"""
        # В реальному додатку тут було б збереження в файл
        pass

class MyGameApp(App):
    def build(self):
        return ClickerGame()

if __name__ == '__main__':
    MyGameApp().run()