# Snooper.py

Snooper.py is a Desktop GUI Application for exploring deals on WeedMaps.com

## Installation

Simply download the .exe or .py, and execute it. (.py requires python and required packages installed)

## Software Requirements

## Windows

Nothing, just download the exe and run it!

## Linux (also mac?)

Python 3.7

### Python packages

requests

run the command pip install requests to install this package

Note: in linux, use "sudo python3.7 -m pip install requests"

## Usage

1. Check Software Requirements
2. Download either .exe or .py
3. Open Application & click "Refresh Subregions"
4. Select a subregion
5. Select a deal
6. Find what you need :)


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Notes

### Deal's seem to be where they shouldn't?

Weedmaps.com's backend seems to hiccup at keeping track of where a deal is. Often i find that one store with multiple deals will have
some of those deals spread across several subregions, despite how they show up on the website.

Future updates will hopefully fix this issue by implementing my own sorting routine. Until then, make sure to look at all regions near yours!

### Getting Tk() not defined error

I believe this is caused by the script not operating in Python 3.7, which has tkinter installed by default. 