import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
import matplotlib.pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg

Window.clearcolor = (0.1, 0.1, 0.1, 1)

# SQLite Database to store screen time
def init_db():
    conn = sqlite3.connect("screen_time.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS screen_time
                 (name TEXT, date TEXT, screen_time INTEGER)''')
    conn.commit()
    conn.close()

def save_screen_time(name, screen_time):
    conn = sqlite3.connect("screen_time.db")
    c = conn.cursor()
    c.execute("INSERT INTO screen_time (name, date, screen_time) VALUES (?, date('now'), ?)", (name, screen_time))
    conn.commit()
    conn.close()

def get_screen_time_data():
    conn = sqlite3.connect("screen_time.db")
    c = conn.cursor()
    c.execute("SELECT date, screen_time FROM screen_time")
    data = c.fetchall()
    conn.close()
    return data

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.name_input = TextInput(hint_text="Enter your name", multiline=False)
        self.sleep_input = TextInput(hint_text="Sleep Time (e.g. 23:00)", multiline=False)
        self.wake_input = TextInput(hint_text="Wake Time (e.g. 06:00)", multiline=False)
        self.limit_input = TextInput(hint_text="Daily Screen Limit in seconds (e.g. 5)", multiline=False)

        self.result_label = Label(text="")

        self.start_btn = Button(text="Start Simulation", on_press=self.start_simulation)
        self.view_usage_btn = Button(text="View Usage Tracker", on_press=self.view_usage)

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.sleep_input)
        self.layout.add_widget(self.wake_input)
        self.layout.add_widget(self.limit_input)
        self.layout.add_widget(self.start_btn)
        self.layout.add_widget(self.view_usage_btn)
        self.layout.add_widget(self.result_label)

        self.add_widget(self.layout)

    def start_simulation(self, instance):
        try:
            self.screen_limit = int(self.limit_input.text)
        except:
            self.result_label.text = "❌ Invalid screen time limit!"
            return

        self.result_label.text = f"Hi {self.name_input.text}! Starting screen use simulation..."
        simulate_screen = self.manager.get_screen('simulate')
        simulate_screen.start_timer(self.screen_limit)
        self.manager.current = 'simulate'

    def view_usage(self, instance):
        usage_screen = self.manager.get_screen('usage_tracker')
        usage_screen.refresh_tracker(None)
        self.manager.current = 'usage_tracker'

class SimulateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        self.limit = 5
        self.event = None

        self.timer_label = Label(text="Screen Time: 0 sec", font_size=28)
        self.stop_btn = Button(text="Stop Early (Good Behavior)", on_press=self.stop_early)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout.add_widget(self.timer_label)
        self.layout.add_widget(self.stop_btn)
        self.add_widget(self.layout)

    def start_timer(self, limit):
        self.count = 0
        self.limit = limit
        self.timer_label.text = "Screen Time: 0 sec"
        if self.event:
            self.event.cancel()
        self.event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.count += 1
        self.timer_label.text = f"Screen Time: {self.count} sec"
        if self.count >= self.limit:
            if self.event:
                self.event.cancel()
            self.manager.current = 'lock'

    def stop_early(self, instance):
        if self.event:
            self.event.cancel()
        save_screen_time(self.manager.get_screen('home').name_input.text, self.count)
        self.manager.get_screen('success').set_points(10)
        self.manager.current = 'success'

class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="🚫 Screen Limit Exceeded - Social Media Locked!", font_size=20))

        grid = GridLayout(cols=3, spacing=10)
        grid.add_widget(self.animated_icon("instagram.jpg", "Instagram"))
        grid.add_widget(self.animated_icon("youtube.jpg", "YouTube"))
        grid.add_widget(self.animated_icon("facebook.jpg", "Facebook"))

        layout.add_widget(grid)
        layout.add_widget(Label(text="🏆 Points Earned: 0", font_size=18))
        layout.add_widget(Button(text="Back to Home", on_press=self.go_home))
        self.add_widget(layout)

    def animated_icon(self, icon_path, name):
        box = BoxLayout(orientation='vertical')
        img = Image(source=icon_path, opacity=0)
        lbl = Label(text=f"{name}\n🔒 Locked", font_size=14, halign='center')
        box.add_widget(img)
        box.add_widget(lbl)
        Animation(opacity=1, duration=1.5).start(img)
        return box

    def go_home(self, instance):
        self.manager.current = 'home'

class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.msg = Label(text="✅ Great Job! Screen time within limit.", font_size=22)
        self.points = Label(text="🏆 Points Earned: 10", font_size=20)

        self.layout.add_widget(self.msg)
        self.layout.add_widget(self.points)
        self.layout.add_widget(Button(text="Back to Home", on_press=self.go_home))
        self.add_widget(self.layout)

    def set_points(self, points):
        self.points.text = f"🏆 Points Earned: {points}"

    def go_home(self, instance):
        self.manager.current = 'home'

class UsageTrackerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout = layout

        self.usage_label = Label(text="Total Sessions: 0", font_size=20)
        self.usage_times_label = Label(text="No Data", font_size=16)

        self.layout.add_widget(self.usage_label)
        self.layout.add_widget(self.usage_times_label)

        graph_btn = Button(text="Plot Graph", on_press=self.plot_graph)
        self.layout.add_widget(graph_btn)

        go_home_btn = Button(text="Go Back to Home", on_press=self.go_home)
        self.layout.add_widget(go_home_btn)

        self.add_widget(self.layout)

    def refresh_tracker(self, instance):
        data = get_screen_time_data()
        self.usage_label.text = f"Total Sessions: {len(data)}"
        times = "\n".join([f"Session {i+1}: {entry[1]} sec" for i, entry in enumerate(data)])
        self.usage_times_label.text = times if times else "No sessions yet!"

    def plot_graph(self, instance):
        data = get_screen_time_data()
        if not data:
            return

        dates = [entry[0] for entry in data]
        times = [entry[1] for entry in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, times, marker='o', linestyle='-', color='b', label='Screen Time')
        plt.xlabel("Date")
        plt.ylabel("Screen Time (seconds)")
        plt.title("Screen Time Tracker")
        plt.xticks(rotation=45)
        plt.tight_layout()

        graph = FigureCanvasKivyAgg(plt.gcf())
        self.layout.add_widget(graph)

    def go_home(self, instance):
        self.manager.current = 'home'

class SleepApp(App):
    def build(self):
        init_db()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SimulateScreen(name='simulate'))
        sm.add_widget(LockScreen(name='lock'))
        sm.add_widget(SuccessScreen(name='success'))
        sm.add_widget(UsageTrackerScreen(name='usage_tracker'))
        return sm

if __name__ == '__main__':
    SleepApp().run()
