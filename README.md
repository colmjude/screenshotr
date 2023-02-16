# Screenshotr

Python script to take screenshots of webpages. Give it a url and it will take a screenshot.

## Set up

It is best to work in a virtualenv. 

Then install dependencies with

```
make init
```

Create a folder for your screenshots, call it `screenshots`.

## How to take screenshots

Take a screenshot of a webpage

```
python screenshotr.py screenshot --url 'https://colmjude.com' --output cj-home
```

**--url** is the url
**--output** is name of the saved file

Dimensions of screenshot will default to a viewport of 1200 width and 1600 height.

Set viewport dimensions with the `--vwidth` and `--vheight` options.

For example set screenshot to 800x1200

```
python screenshotr.py screenshot --url 'https://colmjude.com' --output cj-home-800 --vwidth 800 --vheight 1200
```

Take full length screenshot using the `--fullpage` option.
Beware: this will not work if page continues to load new content as you scroll (e.g. twitter)

E.g.

```
python screenshotr.py screenshot --url 'hhttps://colmjude.com/notes/weeknote/weeknote-30012023/' --output cj-notes-full --vwidth 1200 --fullpage True
```

Take screenshots at iPhone X dimensions

```
python screenshotr.py screenshot --url 'hhttps://colmjude.com/notes/weeknote/weeknote-30012023/' --output cj-notes-320 --vwidth 320 --vheight 568 --fullpage True
```

Take screenshots at iPhone 14 dimensions (I only ignore top notch no go zone)

```
python screenshotr.py screenshot --url 'hhttps://colmjude.com/notes/weeknote/weeknote-30012023/' --output cj-notes-390 --vwidth 390 --vheight 797 --fullpage True
```

Add url to bottom of screenshot using `--saveurl` option. E.g.

```
python screenshotr.py screenshot --url 'https://colmjude.com' --output cj-home --saveurl True
```
