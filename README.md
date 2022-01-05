# L'étrange Histoire de Mr. Anderson - The game
A RPG inspired by the Laylow's album *[L'Étrange Histoire de Mr. Anderson](https://fr.wikipedia.org/wiki/L'%C3%89trange_Histoire_de_Mr._Anderson)*.

---

Build by:
 - [@arthur-fontaine](https://github.com/arthur-fontaine)
 - [@idriss667](https://github.com/idriss667)
 - [@malek-zeroual](https://github.com/malek-zeroual)
 - [@sanass98](https://github.com/sanass98)
 - [@ulysse-r](https://github.com/ulysse-r)

## Introduction

L'Étrange Histoire de Mr. Anderson is an album by the French rapper [Laylow](https://fr.wikipedia.org/wiki/Laylow). For a school project where we had to create a game, we decided to create a game based on the album.

## Instructions

_The game is developed using Python 3.9. We cannot guarantee that it will work with other versions of Python._

To install the dependencies, run the following command:
```shell
pip install -r requirements.txt
```

Then, to run the game, run the following command:
```shell
python3 main.py
```

## Documentation

The documentation is available at [DOCUMENTATION.md](/DOCUMENTATION.md).

## Known issues

### Kivy installation on Apple Silicon

On Apple Silicon, Kivy should be rebuilt locally.

```shell
git clone https://github.com/kivy/kivy.git
cd kivy
make
```

Then copy the `kivy` folder to the `/usr/local/lib/python3.x/site-packages` folder.
