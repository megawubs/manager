Manager
=======

This little program uses the awesome guessit library to manage your downloaded files.

# Installation

Clone this repo using git.

# Usage:

Before you use it, set the varibles in manager/__main__.py

```python
	extentions = ['*.mkv', '*.avi', '*.mp4', '*.srt']
	m = Manager(pathToDownloads, pathToMovies,pathToShows, extentions)
```

When you want to run it simply run this in the folder you did your git clone command:

```bash
	$ python manager
```

## Requirements

This program requires guessit to be installed