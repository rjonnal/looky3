## looky: a pygame-based fixation target for vision experiments

### Prerequisites

An easy way to avoid version conflicts is to use a Python distribution with a repository and/or package manager, such as [Anaconda](https://docs.continuum.io/anaconda/).

After installing Anaconda, install pygame using `pip install pygame`.

If you have a pre-existing Python installation you want to use, or if you want a lightweight installation without all of Anaconda, you need the following:

1. [Python 2.7.x](https://www.python.org/downloads/)

2. [Pygame](http://www.pygame.org/download.shtml). Make sure you get the version matching your Python installation.

### Installation and use

1. Clone this repository with git: `git clone https://github.com/rjonnal/looky` or download the zip file and unzip.

2. In the resulting directory, copy `looky_config_template.py` to `looky_config.py`, and edit it the latter as you wish. In particular, the distance between the viewer and screen (`SCREEN_DISTANCE_M`) must be set, as well as `VERTICAL_ORIENTATION` and `HORIZONTAL_ORIENTATION`.

3. Run **calibrate** or issue `python calibrate.py`. Stick a standard (3-inch square) Post-It note to your screen and click two adjacent corners. This measures and records the monitor's pitch (DPI) in a file called `dpi.txt`.

4. Run **looky** (or **looky.bat** on Windows) or issue `python __init__.py`.

5. To toggle the help menu, press the `/` key.

6. Use the 'm' key to cycle through display modes until the window size matches your monitor resolution. Note the display mode number (not the actual resolution, but the mode number), in case you want to enter this number in `looky_config.py` as a default display mode.