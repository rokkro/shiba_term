# shiba_term
Output a shiba to your terminal. Gets shibas from https://shibe.online/ 

![Shiba pic](/../main/shibe.png)


# Install dependencies
Requires python 3.8+

`pip3 install pillow colr requests`

# Run it
`python3 path/to/shiba_term.py`


# Args

```
usage: shiba_term.py [--help] [--count COUNT] [--height HEIGHT]
                        [--width WIDTH] [--invert] [--aspect]

optional arguments:
  --help                Show this help message.
  --count COUNT, -c COUNT
                        Count of shibas to display: 1-100. (Default 1)
  --height HEIGHT, -h HEIGHT
                        Height of shiba to output. (Defaults to console size)
  --width WIDTH, -w WIDTH
                        Width shiba to output. (Defaults to console size)
  --invert, -i          If passed, invert the output colors.
  --aspect, -ar         If passed, image aspect ratio is maintained with 128x128 max resolution.
```
