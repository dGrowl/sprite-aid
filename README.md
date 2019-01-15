# SSVA: Sprite Sheet Visual Aid

### Goal
To enhance the user's ability to quickly and accurately identify the coordinates of each frame in a sprite sheet.

### Usage
General:
```
$ python ssva.py [path_to_image] [width_of_frame] [height_of_frame] [mode]
```
Example:
```
$ python ssva.py my_spritesheet.png 50 30 ribbon
```
Output is stored in the same directory as the input file with _AID appended to its path.

### Future

* Output format that matches input
* Automatic detection/approximation of optimal frame size

### Issues

The image processing library (Pillow) seems to have problems matching coordinates exactly. The program still serves its purpose just fine, but imprecision is bad.
