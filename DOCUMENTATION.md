# Documentation

The development of this game is based on a self-made game library inspired by [Scratch](https://scratch.mit.edu/).

## How to create a game

### Step 1: Create a scene

First, we need to create the scenes. A scene is a collection of sprites.

Follow the steps below:
 1. If there is not a directory named `scenes`, create one.
 2. Create a directory named `scene_name`.
 3. Create a file named `scene_name.py`.
 4. In this file, create a function named `scene_name`.

### Step 2: Create a sprite

 1. If there is not a directory named `sprites`, create one.
 2. Create a directory named `sprite_name`.
 3. Create a file named `sprite_name.py`.
 4. In this file, create a function named `sprite_name`.
 5. Add as many costumes and actions as you want.

### Step 3: Add a sprite to a scene

 1. In the scene file, import the sprite file.
 2. Initialize the sprite and add it to the scene.
 3. Add as many events and actions as you want.

### Step 4: Create and run the game

 1. Once you have created the scenes and sprites, create a file named `main.py`.
 2. In this file, import all the scenes files.
 3. Create a function named `main`.
 4. Initialize the scenes.
 5. Initialize the game.
 6. Add as many events as you want.
 7. Run the game.

### Example

`/sprites/student.py`
```python
from game.Game import Sprite, Game

def student(game: Game):
    sprite = Sprite('assets/sprites/student/costumes/default.png')
    sprite.add_costume('run1', 'assets/sprites/student/costumes/run1.png')
    sprite.add_costume('run2', 'assets/sprites/student/costumes/run2.png')
    
    def animate_sprite_run(variant: str, duration: float):
        if variant == 'run2':
            sprite.switch_variant('run2')
            game.wait_then(duration, lambda _: animate_sprite_run('run1', duration))
        else:
            sprite.switch_variant('run1')
            game.wait_then(duration, lambda _: animate_sprite_run('run2', duration))
            
    sprite.on('keydown_d', lambda _: animate_sprite_run('run1', 0.5))

    return sprite
```

`/sprites/cat.py`
```python
from game.Game import Sprite, Game

def cat(game: Game):
    sprite = Sprite('assets/sprites/cat/costumes/default.png')
    sprite.add_costume('sleep', 'assets/sprites/cat/costumes/sleep.png')

    return sprite
```

`/scenes/school/school.py`
```python
from game.Game import Scene, Game
from sprites.student import student

def school(game):
    scene = Scene()
    scene.add_sprite(student(game))
    
    return scene
```

`/scenes/home/home.py`
```python
from game.Game import Scene, Game
from sprites.student import student
from sprites.cat import cat

def home(game: Game):
    scene = Scene()
    scene.add_sprite(student(game))
    scene.add_sprite(cat(game))
    
    cat.switch_costume('sleep')
    
    return scene
```

`/main.py`
```python
from game.Game import Game
from scenes.school.school import school
from scenes.home.home import home

def main():
    game = Game()
    
    game.add_scene(school(game))
    game.add_scene(home(game))
    
    game.on('start', lambda _: print("Game started!"))
    
    game.run()

if __name__ == '__main__':
    main()
```

## API

### Element (inherits from [kivy.uix.widget.Widget](https://kivy.org/docs/api-kivy.uix.widget.html#kivy.uix.widget.Widget))

#### Methods

 - `on(event_name, callback)`: Bind an event to the element.
 - `emit(event_name, *args)`: Emit an event.

### Sprite (inherits from [Element](#element) and [kivy.uix.floatlayout.FloatLayout](https://kivy.org/docs/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout))

```python
from game.Game import *

sprite = Sprite('assets/sprite/default.png')
sprite.add_costume('run', 'assets/sprite/run.png')
```

#### Methods

 - `add_costume(costume_name, image_path)`: Add a costume to the sprite.
 - `switch_costume(costume_name)`: Switch to the costume.
 - `set_x_to(x)`: Set the x position of the sprite.
 - `set_y_to(y)`: Set the y position of the sprite.
 - `change_x_by(dx)`: Change the x position of the sprite by dx.
 - `change_y_by(dy)`: Change the y position of the sprite by dy.
 - `set_position_to(x, y)`: Set the position of the sprite.
 - `change_position_by(dx, dy)`: Change the position of the sprite by dx and dy.
 - `go_to_in_seconds(x, y, duration)`: Move the sprite to x, y in duration seconds.
 - `set_x_scale_to(x_scale)`: Set the x scale of the sprite.
 - `set_y_scale_to(y_scale)`: Set the y scale of the sprite.
 - `set_scale_to(scale)`: Set the scale of the sprite.
 - `change_x_scale_by(dx_scale)`: Change the x scale of the sprite by dx_scale.
 - `change_y_scale_by(dy_scale)`: Change the y scale of the sprite by dy_scale.
 - `change_scale_by(d_scale)`: Change the scale of the sprite by d_scale.
 - `set_scale_to_in_seconds(scale, duration)`: Set the scale of the sprite to scale in duration seconds.
 - `set_x_scale_to_in_seconds(x_scale, duration)`: Set the x scale of the sprite to x_scale in duration seconds.
 - `set_y_scale_to_in_seconds(y_scale, duration)`: Set the y scale of the sprite to y_scale in duration seconds.
 - `set_opacity_to(opacity)`: Set the opacity of the sprite.
 - `change_opacity_by(d_opacity)`: Change the opacity of the sprite by d_opacity.
 - `set_opacity_to_in_seconds(opacity, duration)`: Set the opacity of the sprite to opacity in duration seconds.

#### Properties

 - `current_costume`: The current costume of the sprite.
 - `scale_x`: The x scale of the sprite.
 - `scale_y`: The y scale of the sprite.
 
### Scene (inherits from [Element](#element) and [kivy.uix.floatlayout.FloatLayout](https://kivy.org/docs/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout))

```python
from game.Game import *

sprite = Sprite('assets/sprite/default.png')
sprite.add_costume('run', 'assets/sprite/run.png')

scene = Scene()
scene.set_background_image("assets/background.jpeg")
scene.add_sprite(sprite)
```

#### Methods

 - `set_background_image(background_image_path)`: Set the background image of the scene.
 - `add_sprite(sprite)`: Add a sprite to the scene.

### Game (inherits from [kivy.uix.widget.Widget](https://kivy.org/docs/api-kivy.uix.widget.html#kivy.uix.widget.Widget) and [kivy.app.App](https://kivy.org/docs/api-kivy.app.html#kivy.app.App))

```python
from game.Game import *

sprite = Sprite('assets/sprite/default.png')
sprite.add_costume('run', 'assets/sprite/run.png')

scene = Scene()
scene.set_background_image("assets/background.jpeg")
scene.add_sprite(sprite)

game = Game(scene)
game.run()
```

#### Methods

 - `change_scene(scene)`: Change the scene of the game.
 - `wait_for_seconds(duration)`: Wait for duration seconds.
 - `wait_then(duration, function)`: Wait for duration seconds and then execute function.
 - `wait_until(condition)`: Wait until condition is true.
 - `repeat_every_seconds(duration, function)`: Repeat function every duration seconds.