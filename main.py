import webbrowser
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from createAvatars import Start1Screen, Start2Screen, Start3Screen
from createStickers import QuizScreen, FinalScreen, Database

db_name = "user_stickers.db"
max_user_data = 14

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def open_link(self, link):
        webbrowser.open(link)

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)

    def open_link(self, link):
        webbrowser.open(link)

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.ids.row_col.text = self.get_table_text()

    def get_table_text(self):
        db = Database(db_name)
        data = db.get_all_data()

        table_text = "  ----------------------------------------------------------------------------\n"
        for row in data:
            table_text += self.trim(f"\n{datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')}    {row[2] },   {row[3] },   {row[4] },   {row[5] } {'sticker' if row[5] <= 1 else 'stickers'}")

        if len(data) < max_user_data:
            for i in range(max_user_data - len(data)):
                table_text += f"\n"
        
        return table_text

    def trim(self, text):
        if len(text) > 150:
            return text[:147] + "..."
        
        return text

class WiiStickersApp(App):
    def build(self):
        Window.maximize()

        sm = ScreenManager()

        # Create screens
        home_screen = HomeScreen(name='home')
        about_screen = AboutScreen(name='about')
        contact_screen = ContactScreen(name='contact')
        history_screen = HistoryScreen(name='history')
        start1_screen = Start1Screen(name='start1')
        start2_screen = Start2Screen(name='start2')
        start3_screen = Start3Screen(name='start3')
        quiz_screen = QuizScreen(name='quiz')
        final_screen = FinalScreen(name='final')

        sm.add_widget(home_screen)
        sm.add_widget(about_screen)
        sm.add_widget(contact_screen)
        sm.add_widget(history_screen)
        sm.add_widget(start1_screen)
        sm.add_widget(start2_screen)
        sm.add_widget(start3_screen)
        sm.add_widget(quiz_screen)
        sm.add_widget(final_screen)

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(sm)

        return root_layout

if __name__ == '__main__':
    WiiStickersApp().run()