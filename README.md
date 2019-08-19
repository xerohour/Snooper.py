# Snooper.py

Snooper.py is a Desktop GUI Application for exploring deals on WeedMaps.com

## Installation

Simply download the .exe or .py, and execute it. (.py requires python and required packages installed)

## Usage

### Required External Libraries

1. requests

### Windows

1. Download exe from repository
2. Open Application & click "Refresh Subregions"
3. Select a subregion
4. Select a deal
5. Find what you need :)

### Linux

1. Install Python
2. Ensure all required libraries are installed
3. launch the python script

Note: some users getting Tk() not defined error, investigating ...


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Notes

  Weedmaps.com's backend seems to hiccup at keeping track of where a deal is. Often i find that one store with multiple deals will have
some of those deals spread across several subregions, despite how they show up on the website.

  Future updates will hopefully fix this issue by implementing my own sorting routine. Until then, make sure to look at all regions near yours!
