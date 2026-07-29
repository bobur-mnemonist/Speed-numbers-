"""
Xotira Sport - Raqamlar va Kartalar Yodlash
Termux'da yozilgan, GitHub Actions orqali APK'ga yig'iladi.
"""

import random
import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

STATS_FILE = 'memory_stats.json'

CARD_NAMES = [f'{r}{s}' for s in ['♠', '♥', '♦', '♣'] for r in
              ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]


def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {'sessions': []}


def save_session(mode, digit_count, time_limit, correct, total, percent):
    stats = load_stats()
    stats['sessions'].append({
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'mode': mode,
        'size': digit_count,
        'time_limit': time_limit,
        'correct': correct,
        'total': total,
        'percent': percent
    })
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        layout.add_widget(Label(text='Xotira Sport', font_size=34, size_hint=(1, 0.2), bold=True))

        self.mode = 'numbers'
        self.digit_count = 20
        self.time_limit = 60

        self.mode_label = Label(text='Rejim: Raqamlar', font_size=18, size_hint=(1, 0.1))
        layout.add_widget(self.mode_label)

        mode_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        btn_num = Button(text='Raqamlar')
        btn_num.bind(on_press=lambda x: self.set_mode('numbers'))
        btn_card = Button(text='Kartalar')
        btn_card.bind(on_press=lambda x: self.set_mode('cards'))
        mode_row.add_widget(btn_num)
        mode_row.add_widget(btn_card)
        layout.add_widget(mode_row)

        self.difficulty_label = Label(text='20 ta / 60 soniya', font_size=16, size_hint=(1, 0.1))
        layout.add_widget(self.difficulty_label)

        diff_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=8)
        btn_easy = Button(text='Oson')
        btn_easy.bind(on_press=lambda x: self.set_difficulty(10, 30))
        btn_med = Button(text="O'rta")
        btn_med.bind(on_press=lambda x: self.set_difficulty(20, 60))
        btn_hard = Button(text='Qiyin')
        btn_hard.bind(on_press=lambda x: self.set_difficulty(40, 120))
        diff_row.add_widget(btn_easy)
        diff_row.add_widget(btn_med)
        diff_row.add_widget(btn_hard)
        layout.add_widget(diff_row)

        start_btn = Button(text='Boshlash', font_size=22, size_hint=(1, 0.16),
                            background_color=(0.2, 0.7, 0.3, 1))
        start_btn.bind(on_press=self.start_exercise)
        layout.add_widget(start_btn)

        stats_btn = Button(text='Statistika', font_size=16, size_hint=(1, 0.1))
        stats_btn.bind(on_press=self.show_stats)
        layout.add_widget(stats_btn)

        self.add_widget(layout)

    def set_mode(self, mode):
        self.mode = mode
        self.mode_label.text = 'Rejim: Raqamlar' if mode == 'numbers' else 'Rejim: Kartalar'
        if mode == 'cards' and self.digit_count > 52:
            self.digit_count = 52

    def set_difficulty(self, count, seconds):
        if self.mode == 'cards':
            count = min(count, 52)
        self.digit_count = count
        self.time_limit = seconds
        self.difficulty_label.text = f'{count} ta / {seconds} soniya'

    def start_exercise(self, instance):
        memorize_screen = self.manager.get_screen('memorize')
        memorize_screen.setup(self.mode, self.digit_count, self.time_limit)
        self.manager.current = 'memorize'

    def show_stats(self, instance):
        stats_screen = self.manager.get_screen('stats')
        stats_screen.load_and_display()
        self.manager.current = 'stats'


class MemorizeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)
        self.sequence = []
        self.mode = 'numbers'
        self.remaining_time = 0
        self.event = None

    def setup(self, mode, count, time_limit):
        self.mode = mode
        self.layout.clear_widgets()
        self.remaining_time = time_limit

        if mode == 'numbers':
            self.sequence = [str(random.randint(0, 9)) for _ in range(count)]
        else:
            shuffled = CARD_NAMES.copy()
            random.shuffle(shuffled)
            self.sequence = shuffled[:count]

        self.timer_label = Label(text=f'Vaqt: {self.remaining_time}', font_size=20, size_hint=(1, 0.12))
        self.layout.add_widget(self.timer_label)

        scroll = ScrollView(size_hint=(1, 0.68))
        if mode == 'numbers':
            grouped = ' '.join([''.join(self.sequence[i:i+5]) for i in range(0, len(self.sequence), 5)])
            content_label = Label(text=grouped, font_size=26, size_hint_y=None, halign='center')
            content_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1] + 20))
            content_label.text_size = (Window.width - 60, None)
        else:
            content_label = Label(text='  '.join(self.sequence), font_size=24, size_hint_y=None)
            content_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1] + 20))
            content_label.text_size = (Window.width - 60, None)
        scroll.add_widget(content_label)
        self.layout.add_widget(scroll)

        done_btn = Button(text="Tugatdim, yozaman", font_size=18, size_hint=(1, 0.2))
        done_btn.bind(on_press=self.go_to_recall)
        self.layout.add_widget(done_btn)

        if self.event:
            self.event.cancel()
        self.event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.remaining_time -= 1
        self.timer_label.text = f'Vaqt: {self.remaining_time}'
        if self.remaining_time <= 0:
            self.event.cancel()
            self.go_to_recall(None)

    def go_to_recall(self, instance):
        if self.event:
            self.event.cancel()
        recall_screen = self.manager.get_screen('recall')
        recall_screen.setup(self.mode, self.sequence)
        self.manager.current = 'recall'


class RecallScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        self.add_widget(self.layout)
        self.mode = 'numbers'
        self.correct_sequence = []

    def setup(self, mode, correct_sequence):
        self.mode = mode
        self.layout.clear_widgets()
        self.correct_sequence = correct_sequence

        hint = 'raqamlarni ketma-ket kiriting (bo\'sh joysiz)' if mode == 'numbers' else \
               'kartalarni vergul bilan ajratib yozing (masalan: AS, 10H, KD)'
        self.layout.add_widget(Label(text=f'Eslaganingizni kiriting:\n{hint}', font_size=15, size_hint=(1, 0.15)))

        self.input_field = TextInput(multiline=True, font_size=20, size_hint=(1, 0.4))
        self.layout.add_widget(self.input_field)

        check_btn = Button(text='Tekshirish', font_size=20, size_hint=(1, 0.18),
                            background_color=(0.2, 0.5, 0.8, 1))
        check_btn.bind(on_press=self.check_answer)
        self.layout.add_widget(check_btn)

        self.result_label = Label(text='', font_size=15, size_hint=(1, 0.27))
        self.layout.add_widget(self.result_label)

    def check_answer(self, instance):
        raw = self.input_field.text.strip()

        if self.mode == 'numbers':
            user_seq = list(raw.replace(' ', '').replace(',', ''))
        else:
            user_seq = [c.strip().upper() for c in raw.split(',') if c.strip()]

        correct_count = 0
        for i in range(min(len(user_seq), len(self.correct_sequence))):
            if user_seq[i] == self.correct_sequence[i]:
                correct_count += 1
            else:
                break

        total = len(self.correct_sequence)
        percent = int((correct_count / total) * 100) if total > 0 else 0
        correct_str = ''.join(self.correct_sequence) if self.mode == 'numbers' else ', '.join(self.correct_sequence)

        self.result_label.text = f"To'g'ri: {correct_count}/{total} ({percent}%)\nJavob: {correct_str}"

        save_session(self.mode, total, 0, correct_count, total, percent)

        again_btn = Button(text='Bosh menyuga', font_size=18, size_hint=(1, 0.18))
        again_btn.bind(on_press=self.go_home)
        self.layout.add_widget(again_btn)

    def go_home(self, instance):
        self.manager.current = 'menu'


class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def load_and_display(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Statistika', font_size=26, size_hint=(1, 0.12), bold=True))

        stats = load_stats()
        sessions = stats.get('sessions', [])[-15:]
        sessions.reverse()

        scroll = ScrollView(size_hint=(1, 0.68))
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        if not sessions:
            grid.add_widget(Label(text="Hali mashq qilinmagan", size_hint_y=None, height=40))
        else:
            for s in sessions:
                mode_name = 'Raqamlar' if s['mode'] == 'numbers' else 'Kartalar'
                text = f"{s['date']} | {mode_name} | {s['size']} ta | {s['percent']}%"
                grid.add_widget(Label(text=text, size_hint_y=None, height=35, font_size=14))

        scroll.add_widget(grid)
        self.layout.add_widget(scroll)

        back_btn = Button(text='Orqaga', font_size=18, size_hint=(1, 0.15))
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

    def go_back(self, instance):
        self.manager.current = 'menu'


class MemoryApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.98, 1)
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MemorizeScreen(name='memorize'))
        sm.add_widget(RecallScreen(name='recall'))
        sm.add_widget(StatsScreen(name='stats'))
        return sm


if __name__ == '__main__':
    MemoryApp().run()
