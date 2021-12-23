from __future__ import annotations

from typing import Optional, Callable, Union

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle, Line
from kivy.modules import inspector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
# from kivy.core.text import FontContextManager as FCM
#
# FCM.create('system://myapp')
# fonts = {
#     'PressStart2P-Regular': FCM.add_font('assets/fonts/PressStart2P-Regular.ttf')
# }

import re


class Element(Widget):
    events: dict[str, Optional[list[dict[str, Union[Callable, float]]]]] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.emit('keydown_' + keycode[1])

    def _on_keyboard_up(self, keyboard, keycode):
        self.emit('keyup_' + keycode[1])

    def on(self, event_name: str, callback: Callable[[Sprite], None], min_wait: float = 0):
        if event_name in self.events:
            self.events[event_name].append({'callback': callback, 'min_wait': min_wait})
        else:
            self.events[event_name] = [{'callback': callback, 'min_wait': min_wait}]

    def emit(self, event_name: str, *args):
        if event_name in self.events:
            for event in self.events[event_name]:
                if event['min_wait'] != 0:
                    if 'last_emit' not in event:
                        event['last_emit'] = 0
                        event['callback'](self, *args)
                    else:
                        if event['last_emit'] + event['min_wait'] < Clock.get_time():
                            event['callback'](self, *args)
                            event['last_emit'] = Clock.get_time()
                else:
                    event['callback'](self, *args)


class Sprite(FloatLayout, Element):
    def __init__(self, sprite_image_path: str, **kwargs):
        super().__init__(**kwargs)

        default_costume = self.__make_sprite_image(sprite_image_path)
        self.costumes = {
            "default": default_costume
        }
        self.costume_name = "default"

        self.base_size = self.size

    def build(self):
        self.clear_widgets()
        self.add_widget(self.current_costume)

    @property
    def current_costume(self) -> Widget:
        """
        :return: The current costume to be displayed
        """
        return self.costumes[self.costume_name]

    @property
    def scale_x(self) -> float:
        """
        :return: The sprite's x scale

        @example
        ```python
        sprite.scale_x # Returns the sprite's x scale
        ```
        """
        return self.size[0] / self.base_size[0]

    @property
    def scale_y(self) -> float:
        """
        :return: The sprite's y scale

        @example
        ```python
        sprite.scale_y # Returns the sprite's y scale
        ```
        """
        return self.size[1] / self.base_size[1]

    @staticmethod
    def __make_sprite_image(sprite_image_path: str) -> Image:
        """
        :param sprite_image_path: The path to the image to be displayed
        :return: The image to be displayed
        """
        image = Image(source=sprite_image_path, size_hint=(1, 1),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5}, allow_stretch=True)
        image.texture.mag_filter = 'nearest'
        return image

    def add_costume(self, costume_name: str, costume_image_path: str):
        """
        :param costume_name: The name of the costume
        :param costume_image_path: The path to the image to be displayed

        @example
        ```python
        sprite.add_costume("run", "path/to/image.png") # Adds a costume called "run" with the image "path/to/image.png"
        ```
        """
        new_costume = self.__make_sprite_image(costume_image_path)
        self.costumes[costume_name] = new_costume

    def switch_costume(self, costume_name: str):
        """
        :param costume_name: The name of the costume to switch to

        @example
        ```python
        sprite.switch_costume("run") # Switches to the run costume
        ```
        """
        self.costume_name = costume_name
        self.build()

    def set_x_to(self, x: float):
        """
        :param x: The x position to set the sprite to

        @example
        ```python
        sprite.set_x_to(100) # Sets the sprite's x position to 100
        ```
        """
        try:
            pixel_hint = 100 / self.parent.size[0] / 100
            self.pos_hint = {'center_x': x * pixel_hint,
                             'center_y': self.pos_hint['center_y'] if 'center_y' in self.pos_hint else 0.5}
        except ZeroDivisionError:
            pass

    def set_y_to(self, y: float):
        """
        :param y: The y position to set the sprite to

        @example
        ```python
        sprite.set_y_to(100) # Sets the sprite's y position to 100
        ```
        """
        try:
            pixel_hint = 100 / self.parent.size[1] / 100
            self.pos_hint = {'center_x': self.pos_hint['center_x'] if 'center_x' in self.pos_hint else 0.5,
                             'center_y': y * pixel_hint}
        except ZeroDivisionError:
            pass

    def change_x_by(self, x: float):
        """
        :param x: The x position to change the sprite by

        @example
        ```python
        sprite.change_x_by(100) # Adds 100 to the current x position
        ```
        """
        self.set_x_to(self.center_x + x)

    def change_y_by(self, y: float):
        """
        :param y: The y position to change the sprite by

        @example
        ```python
        sprite.change_y_by(100) # Adds 100 to the current y position
        ```
        """
        self.set_y_to(self.center_y + y)

    def set_position_to(self, x: float, y: float):
        """
        :param x: The x position to set the sprite to
        :param y: The y position to set the sprite to

        @example
        ```python
        sprite.set_position_to(100, 100) # Sets the sprite to 100, 100
        ```
        """
        self.set_x_to(x)
        self.set_y_to(y)

    def change_position_by(self, x: float, y: float):
        """
        :param x: The x position to change the sprite by
        :param y: The y position to change the sprite by

        @example
        ```python
        sprite.change_position_by(100, 200) # Adds 100 to the x position and 200 to the y position
        ```
        """
        self.change_x_by(x)
        self.change_y_by(y)

    def go_to_in_seconds(self, x: float, y: float, seconds: float):
        """
        :param x: The x position to go to
        :param y: The y position to go to
        :param seconds: The amount of time to take to get to the position

        @example
        ```python
        sprite.go_to_in_seconds(100, 100, 1) # Goes to x=100, y=100 in 1 second
        ```
        """
        try:
            pixel_hint_x = 100 / self.parent.size[0] / 100
            pixel_hint_y = 100 / self.parent.size[1] / 100

            anim = Animation(pos_hint={'center_x': x * pixel_hint_x, 'center_y': y * pixel_hint_y}, duration=seconds)
            anim.start(self)
        except ZeroDivisionError:
            pass

    def set_x_scale_to(self, x: float):
        """
        :param x: The x scale to set the sprite to

        @example
        ```python
        sprite.set_x_scale_to(0.5) # Sets the sprite's x scale to 0.5
        ```
        """
        try:
            pixel_hint = 100 / self.parent.size[0] / 100
            new_size_hint_x = x * self.base_size[0] * pixel_hint
            self.size_hint_x = new_size_hint_x
        except ZeroDivisionError:
            pass

    def set_y_scale_to(self, y: float):
        """
        :param y: The y scale to set the sprite to

        @example
        ```python
        sprite.set_y_scale_to(0.5) # Sets the sprite's y scale to 0.5
        ```
        """
        try:
            pixel_hint = 100 / self.parent.size[1] / 100
            new_size_hint_y = y * self.base_size[1] * pixel_hint
            self.size_hint_y = new_size_hint_y
        except ZeroDivisionError:
            pass

    def set_scale_to(self, percent_scale: float):
        """
        :param percent_scale: The percent scale to set the sprite to

        @example
        ```python
        sprite.set_scale_to(2) # Sets the sprite to double its size
        ```
        """
        self.set_x_scale_to(percent_scale)
        self.set_y_scale_to(percent_scale)

    def change_x_scale_by(self, x: float):
        """
        :param x: The x scale to change the sprite by

        @example
        ```python
        sprite.change_x_scale_by(0.5) # Adds 0.5 to the current x scale
        ```
        """
        self.set_x_scale_to(self.scale_x + x)

    def change_y_scale_by(self, y: float):
        """
        :param y: The y scale to change the sprite by

        @example
        ```python
        sprite.change_y_scale_by(0.5) # Adds 0.5 to the current y scale
        ```
        """
        self.set_y_scale_to(self.scale_y + y)

    def change_scale_by(self, percent_scale: float):
        """
        :param percent_scale: The percent scale to change the sprite by

        @example
        ```python
        sprite.change_scale_by(2) # Adds 2 to the current percent scale
        ```
        """
        self.change_x_scale_by(percent_scale)
        self.change_y_scale_by(percent_scale)

    def set_scale_to_in_seconds(self, percent_scale: float, seconds: float):
        """
        :param percent_scale: The percent scale to set the sprite to
        :param seconds: The amount of time to take to get to the scale

        @example
        ```python
        sprite.set_scale_to_in_seconds(2, 1) # Sets the sprite to double its size in 1 second
        ```
        """
        try:
            pixel_hint_x = 100 / self.parent.size[0] / 100
            pixel_hint_y = 100 / self.parent.size[1] / 100

            new_size = (percent_scale * self.base_size[0] * pixel_hint_x,
                        percent_scale * self.base_size[1] * pixel_hint_y)
            anim = Animation(size_hint=new_size, duration=seconds)
            anim.start(self)
        except ZeroDivisionError:
            pass

    def set_x_scale_to_in_seconds(self, x: float, seconds: float):
        """
        :param x: The x scale to set the sprite to
        :param seconds: The amount of time to take to get to the scale

        @example
        ```python
        sprite.set_x_scale_to_in_seconds(0.5, 1) # Sets the sprite's x scale to 0.5 in 1 second
        ```
        """
        try:
            pixel_hint = 100 / self.parent.size[0] / 100
            new_size_hint_x = x * self.base_size[0] * pixel_hint
            anim = Animation(size_hint_x=new_size_hint_x, duration=seconds)
            anim.start(self)
        except ZeroDivisionError:
            pass

    def set_y_scale_to_in_seconds(self, y: float, seconds: float):
        """
        :param y: The y scale to set the sprite to
        :param seconds: The amount of time to take to get to the scale

        @example
        ```python
        sprite.set_y_scale_to_in_seconds(0.5, 1) # Sets the sprite's y scale to 0.5 in 1 second
        ```
        """
        try:
            pixel_hint = 100 / self.parent.size[1] / 100
            new_size_hint_y = y * self.base_size[1] * pixel_hint
            anim = Animation(size_hint_y=new_size_hint_y, duration=seconds)
            anim.start(self)
        except ZeroDivisionError:
            pass

    def set_opacity_to(self, opacity: float):
        """
        :param opacity: The opacity to set the sprite to

        @example
        ```python
        sprite.set_opacity_to(0.5) # Sets the sprite to 50% opacity
        ```
        """
        self.opacity = opacity

    def change_opacity_by(self, opacity: float):
        """
        :param opacity: The opacity to change the sprite by

        @example
        ```python
        sprite.change_opacity_by(0.5) # Adds 50% to the current opacity
        ```
        """
        self.set_opacity_to(self.opacity + opacity)

    def set_opacity_to_in_seconds(self, opacity: float, seconds: float):
        """
        :param opacity: The opacity to set the sprite to
        :param seconds: The amount of time to take to get to the opacity

        @example
        ```python
        sprite.set_opacity_to_in_seconds(0.5, 1) # Sets the sprite to 50% opacity in 1 second
        ```

        @example
        ```python
        sprite.set_opacity_to_in_seconds(0, 1) # Makes the sprite invisible in 1 second
        ```
        """
        anim = Animation(opacity=opacity, duration=seconds)
        anim.start(self)


class Scene(FloatLayout, Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = None

        def hide_text(_):
            if self.text is not None:
                self.text = None
                self.build()

        self.on('keydown_spacebar', hide_text)

        self.sprites = []
        self.background = None

    def build(self):
        self.clear_widgets()
        if self.background is not None:
            self.add_widget(self.background)
            self.size = self.background.size

        for sprite in self.sprites:
            sprite.build()
            self.add_widget(sprite)

        if self.text is not None:
            self.add_widget(self.text)

    def __set_background(self, background):
        """
        :param background: The background to set the scene to
        """
        self.background = background

    def set_background_image(self, background_image_path: str):
        """
        :param background_image_path: The path to the image to use as the background

        @example
        ```python
        scene.set_background_image('background.png') # Sets the background to the image at background.png
        ```
        """
        background_image = Image(source=background_image_path)
        self.__set_background(background_image)

    def add_sprite(self, sprite: Sprite):
        """
        :param sprite: The sprite to add to the scene

        @example
        ```python
        scene.add_sprite(sprite) # Adds the sprite to the scene
        ```
        """
        self.sprites.append(sprite)

    def display_text(self, text: str, **events: Callable):
        """
        :param text: The text to display
        :param events: The events to listen when a ref is clicked

        @example
        ```python
        scene.display_text('Hello World') # Displays the text 'Hello World'
        ```

        @example
        ```python
        scene.display_text('Hello [ref=world]World[/ref]', on_world_click=lambda: print('Hello World'))
        # Displays the text 'Hello World' and sets the "world" reference to call the
        # function print('Hello World') when clicked
        """

        regex = r"(\[ref=.+?\].+?\[\/ref\])"
        subst = "[u]\\1[/u]"
        text = re.sub(regex, subst, text, 0, re.MULTILINE)

        def event_handler(instance, value):
            if f'on_{value}_click' in events:
                events[f'on_{value}_click'](instance)

        size_hint = (.9, .2)
        pos_hint = {'center_x': .5, 'y': .05}

        layout = FloatLayout(size_hint=size_hint, pos_hint=pos_hint)
        background_color = Widget(pos_hint={'center_x': .5, 'center_y': .5})
        with background_color.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(size=(Window.size[0] * size_hint[0], Window.size[1] * size_hint[1]),
                             pos=((1 - size_hint[0]) * Window.size[0] * pos_hint['center_x'],
                                  (1 - size_hint[1]) * Window.size[1] * pos_hint['y']))
            Color(0, 0, 0, 1)
            Line(rounded_rectangle=(
                (1 - size_hint[0]) * Window.size[0] * pos_hint['center_x'] + 5,
                (1 - size_hint[1]) * Window.size[1] * pos_hint['y'] + 5,
                Window.size[0] * size_hint[0] - 10,
                Window.size[1] * size_hint[1] - 10,
                10),
                width=1.2)
        layout.add_widget(background_color)

        label = Label(text=f'[color=000000]{text}[/color]', markup=True, size_hint=(1, 1),
                      pos_hint={'x': 0, 'y': 0},
                      # font_context='system://myapp',
                      # familly=fonts['PressStart2P-Regular'],
                      )
        label.bind(on_ref_press=event_handler)

        layout.add_widget(label)

        self.text = layout


class Game(App, Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = None
        self.scenes = []
        self.scene = None

    def build(self) -> Widget:
        if self.scene is not None:
            root = BoxLayout()
            self.scene.build()
            root.add_widget(self.scene)

            inspector.create_inspector(Window, root)

            return root
        else:
            raise Exception("No scene has been set")

    def add_scene(self, scene: Scene):
        """
        :param scene: The scene to add to the game

        @example
        ```python
        game.add_scene(scene) # Adds the scene to the game
        ```
        """
        self.scenes.append(scene)

        if self.scene is None:
            self.scene = self.scenes[0]

    def on_start(self):
        # if self.events.get('start') is not None:
        #     for event in self.events['start']:
        #         event(self)
        self.emit('start')

    def change_scene(self, scene: Scene):
        """
        :param scene: The scene to change to

        @example
        ```python
        game.change_scene(scene) # Changes the scene to the given scene
        ```
        """
        self.scene = scene

    def play_song(self, song_path: str):
        """
        :param song_path: The path to the song to play

        @example
        ```python
        game.play_song('song.mp3') # Plays the song at song.mp3
        ```
        """
        self.sound = SoundLoader.load(song_path)
        self.sound.play()

    def stop_song(self):
        """
        Stops the current song

        @example
        ```python
        game.stop_song() # Stops the current song
        ```
        """
        self.sound.stop()

    def seek_song_to(self, seconds: float):
        """
        :param seconds: The amount of seconds to seek to

        @example
        ```python
        game.seek_song(5) # Seeks to the given amount of seconds
        ```
        """
        self.sound.seek(seconds)

    @staticmethod
    def wait_for_seconds(seconds: float):
        """
        :param seconds: The amount of time to wait

        @example
        ```python
        game.wait(1) # Waits for 1 second
        ```
        """
        Clock.usleep(seconds * 1000000)

    @staticmethod
    def wait_then(seconds: float, function: Callable):
        """
        :param seconds: The amount of time to wait
        :param function: The function to run after the wait

        @example
        ```python
        game.wait_then(1, lambda: print('Hello')) # Waits for 1 second, then prints 'Hello'
        ```
        """
        Clock.schedule_once(function, seconds)

    @staticmethod
    def wait_until(condition: bool):
        """
        :param condition: The condition to wait for

        @example
        ```python
        game.wait_until(True) # Waits until the condition is true
        ```
        """
        while not condition:
            Game.wait(0.01)

    @staticmethod
    def repeat_every_seconds(seconds: float, function):
        """
        :param seconds: The amount of time to wait between each call of the function
        :param function: The function to call every `seconds` seconds

        @example
        ```python
        game.repeat_every(1, function) # Calls the function every second
        ```
        """
        Clock.schedule_interval(function, seconds)
