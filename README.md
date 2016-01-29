# fotolog-downloader
Simple Python script to download all photos of a user.

## Disclaimer
This script is not test somewhere else but my PC (GNU/Linux where I've installed everything I need), so it may fail in other computers and/or operative systems.

**I do not accept any responsibility or liability for the accuracy, content, completeness, legality, or reliability of this project.** However, you're welcome to contribute if you want to ^_^

# What do you need?
Python 2 installed (usually Python 2.7)

Then, just download this project as ZIP file, extract it and open a Terminal

## Additional libraries?
It uses those libraries:

- urllib2
- urlparse
- bs4 (BeautifulSoup)

# How do I run this marvellous piece of witchcraft?
Just open a Terminal, go to the `fotolog-downloader/crawler/` folder and type (parameters explanation below):

```bash
$ python mosaic_crawler.py user path [offset]
```

## Parameters

### User
It's your Fotolog user display name. If your profile url is http://www.fotolog.com/johndoe/, then the *user* is **johndoe**

### Path
It's where you'd like to save all the images. The folder **must exist and be accessible**. Also you must write it with the trailing slash. Examples:

**Right:**

`/home/myuser/my_image_folder/` for GNU/Linux

`"C:\Documents and Settings\myuser\My Documents\my_image_folder\"` for Windows


**Wrong, notice the trailing slash:**

`/home/myuser/my_image_folder` for GNU/Linux

`"C:\Documents and Settings\myuser\My Documents\my_image_folder"` for Windows

### Offset
it's an optional parameter. The Fotolog pages are grouped by mosaics (30 photos each), so you can run the script from the beginnig (don't write any offset) and, if you stop it for example in `.../mosaic/300`, you can resume it by adding the number `300` afther the save path.

## Full examples, without and with offset:

```bash
# GNU/Linux
$ python mosaic_crawler.py johndoe /home/john/my_image_folder/
$ python mosaic_crawler.py johndoe /home/john/my_image_folder/ 300
```
```bash
# Windows
$ python mosaic_crawler.py johndoe "C:\Documents and Settings\myuser\My Documents\my_image_folder\"
$ python mosaic_crawler.py johndoe "C:\Documents and Settings\myuser\My Documents\my_image_folder\" 300
```

# TO-DO

- Publish it on Pypi
- More portability
- Dunno, something else, I guess...
