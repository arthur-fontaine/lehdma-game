from kivy.core.window import Window
from kivy.config import Config
from lib.game.Game import Game
from scenes.pre.pre import pre

Window.size = (800, 600)
Config.set('graphics', 'resizable', False)

if __name__ == '__main__':
    game = Game()
    game.title = 'L\'Étrange Histoire de Mr Anderson - Le jeu'
    game.icon = 'assets/logo.png'

    game.add_scene(pre(game), 'pre')
    game.change_scene('pre', True)

    game.play_song('assets/musics/stuntmen-instru.mp3', volume=0.1, loop=True)

    game.run()
