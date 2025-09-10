from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', True)

from tic_tic_boom.ui import TicTacToeApp


if __name__ == '__main__':
    TicTacToeApp().run()
