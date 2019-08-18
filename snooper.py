import requests
import json
from tkinter import *
import webbrowser

# Define Lists
dispoNameList = []
dispoCityList = []
dispoMenuURLList = []
dealTitleList = []
dealBodyList = []
dealExpirationList = []
subregionList = []

# Define Functions
def determineDealExpiration(seconds):
    # Change expiration(seconds) to expiration(hours)
    dealExpiration = round(seconds / 60 / 60,2)
    
    # Return New Deal Expiration
    return str(dealExpiration) + " Hours"

def downloadDeals(subregionID):
    # Define URL for weedmaps API
    url = 'https://api-g.weedmaps.com/discovery/v1/deals?filter%5Bregion_id%5D=' + str(subregionID) + '&filter%5Btypes%5D=organic&filter%5Bcategory%5D=all&page=1&page_size=150'
    
    # Download Data
    r = requests.get(url)
    
    # save data as text
    deals = json.loads(r.text)
    # Parse / Load data with function
    parseDeals(deals)

def parseDeals(deals):
    # Define how many deals are in the subregion listings
    dealCount = deals["meta"]["total_deals"]
    
    # Creation a counter for iteration
    currentCount = 0
    
    # Clear all entries from Deals Selection ListBox
    dealList.delete(0, END)

    # Clear all data out of each List used for dynamic screen text
    del dispoNameList[:]
    del dispoCityList[:]
    del dispoMenuURLList[:]
    del dealTitleList[:]
    del dealBodyList[:]
    del dealExpirationList[0:]

    # Initiate Loop for adding all data to Deals Selection ListBox
    while True:
        # Iterate currentCount
        currentCount = currentCount+1
        # break loop if last dispensary has been reached. (note: the max count, when defined, always returns +1 more than there actually are in the listings. so even though it may seem like it, there will not be any missed dispensary in the listing.)
        if currentCount == dealCount:
            break
        # Define Data, and append that data to its list
        ## Dispensary Name
        dispoName = deals["data"]["deals"][currentCount]["listing"]["name"]
        dispoNameList.append(dispoName)

        # Dispensary City
        dispoCity = deals["data"]["deals"][currentCount]["listing"]["city"]
        dispoCityList.append(dispoCity)

        # Dispensary Menu URL
        dispoMenuURL = deals["data"]["deals"][currentCount]["listing"]["web_url"]
        dispoMenuURLList.append(dispoMenuURL)

        # Deal Title
        dealTitle = deals["data"]["deals"][currentCount]["title"]
        dealTitleList.append(dealTitle)

        # Deal Body (more details)
        dealBody = deals["data"]["deals"][currentCount]["body"]
        dealBodyList.append(dealBody)
        
        # Deal Expiration
        ## Save deal expiration (defined in seconds by weedmaps)
        dealExpirationSeconds = deals["data"]["deals"][currentCount]["expires_in"]
        
        ## Use function to translate the seconds into hours
        dealExpirationHours = determineDealExpiration(dealExpirationSeconds)

        ## Append the newly translated expiration date to its list
        dealExpirationList.append(dealExpirationHours)
        
        # Insert dealTitle at the end of the Deal Selection ListBox
        dealList.insert(END, dealTitle.encode())

def refreshDetails(self):
    # Define dealListSelection as the currently highlighted deal in the Deal Selection ListBox
    dealListSelection = dealList.curselection()[0]
    
    # Clear all entry boxes
    dispoNameEntryBox.delete(0, END)
    dispoCityEntryBox.delete(0,END)
    dispoURLEntryBox.delete(0,END)
    dealExpirationEntryBox.delete(0,END)
    dispoBodyTextBox.delete(1.0,END)
    
    # Insert each entrybox data entry from their respective lists using dealListSelection as the index for the lists
    dispoNameEntryBox.insert(END, dispoNameList[dealListSelection])
    dispoCityEntryBox.insert(END, dispoCityList[dealListSelection])
    dispoURLEntryBox.insert(END, dispoMenuURLList[dealListSelection])
    dealExpirationEntryBox.insert(END, dealExpirationList[dealListSelection])
    dispoBodyTextBox.insert(INSERT, dealBodyList[dealListSelection])

def refreshsubregionDeals(self):
    # Define subregionListSelection as currently highlighted selection in the subregion Selection ListBox
    subregionListSelection = subregionListBox.curselection()[0]

    # Define selectedSubregionID from subregionList using subregionListSelection as index, using the subregion ID downloaded from weedmaps.com
    selectedSubregionID = subregionList[subregionListSelection]['id']

    # Download deals using subregion ID with Function
    downloadDeals(selectedSubregionID)

def openMenuURL():
    # Use dispoURLEntryBox to open URL
    webbrowser.open_new(dispoURLEntryBox.get())

def refreshSubregions():
    # Define Subregions URL ()
    subregionsURL = 'https://api-g.weedmaps.com/wm/v1/regions/oklahoma/subregions'

    # Download json data from subregions url
    subregionsJSON = requests.get(subregionsURL)

    # Parse / Load data into varaible as text string from json
    subregions = json.loads(subregionsJSON.text)

    # Define subregionsCount as len of subregions element
    subregionsCount = len(subregions["data"]["subregions"])

    # Define count to be used as subregion index in an iterated loop
    currentSubregionCount = 0

    # clear subregion Selection ListBox
    subregionListBox.delete(0, END)

    # Init Iterated Loop
    while True:
        # If currentSubregionCount (index counter) equals subregionsCount (sum of subregion json elements), break the loop. (note: subregion len always returns the amount + 1, so breaking while the index count equals the sum count is fine, and nothing is missed.)
        if currentSubregionCount == subregionsCount:
            break
        
        # Define variable to contain the data to be parsed
        subregionData = subregions["data"]["subregions"][currentSubregionCount]

        # Define Subregion ID
        subregionID = subregionData["id"]

        # Define Subregion Name
        subregionName = subregionData["name"]

        # Append all subregion data in a list to be called later
        subregionList.append(subregionData)

        # Insert stored subregion data into the subregion Selection ListBox
        subregionListBox.insert(END, subregionList[currentSubregionCount]['name'].encode())

        # Iterate currentSubregionCount by 1 (index count)
        currentSubregionCount = currentSubregionCount + 1

# Create Windows
mainWindow = Tk()
mainWindow.title("OK Deals - Now with 75% less weedmaps!")
mainWindow.geometry("850x450")
mainWindow.resizeable=(0,0)

# Create Frames
topFrame = Frame(mainWindow)
topFrame.pack(side=TOP)

bottomFrame = Frame(mainWindow)
bottomFrame.pack(side=BOTTOM)

leftFrame = Frame(topFrame)
leftFrame.pack(side=LEFT)

rightFrame = Frame(topFrame)
rightFrame.pack(side=RIGHT, padx=10)

bottomrightFrame = Frame(bottomFrame)
bottomrightFrame.pack(side=RIGHT)

bottomleftFrame = Frame(bottomFrame)
bottomleftFrame.pack(side=LEFT)

# Create Labels

## Subregion Selector Label
subregionListLabel = Label(leftFrame, text='OK Subregions:')
subregionListLabel.grid(row=0, column=0, sticky=W, padx=10)

## Deal Selector Label
dealListLabel = Label(leftFrame, text='Deals:')
dealListLabel.grid(row=0,column=3, sticky=W, padx=10)

# Dispensary Name Label
dispoNameLabel = Label(rightFrame, text='Dispensary:')
dispoNameLabel.grid(row=0, column=0)

# Dispensary City Label
dispoCityLabel = Label(rightFrame, text='City:')
dispoCityLabel.grid(row=1, column=0)

# Dispensary Menu Label
dispoURLLabel = Label(rightFrame, text='Click for Menu:')
dispoURLLabel.grid(row=2, column=0)

# Deal Expiration Label
dealExpirationLabel = Label(rightFrame, text='Expires in (Hours):')
dealExpirationLabel.grid(row=3,column=0)

# Deal Body Label
dealBodyLabel = Label(bottomleftFrame, text='More Info:')
dealBodyLabel.grid(row=0, column=0, sticky=W, padx=10)


# Create Entry Widgets

## Dispensary Name Entry Box
dispoNameEntryBox = Entry(rightFrame)
dispoNameEntryBox.grid(row=0, column=1, padx=10)

## Dispensary City Entry Box
dispoCityEntryBox = Entry(rightFrame)
dispoCityEntryBox.grid(row=1, column=1, padx=10)

## Dispensary URL Entry Box
dispoURLEntryBox = Entry(rightFrame, cursor="hand2")
dispoURLEntryBox.grid(row=2, column=1, padx=10)

## Deal Expiration Entry Box
dealExpirationEntryBox = Entry(rightFrame)
dealExpirationEntryBox.grid(row=3, column=1)

# Create Text Box (for deal body details)
dispoBodyTextBox = Text(bottomleftFrame, height=10, width=75)
dispoBodyTextBox.grid(row=1,column=0,padx=10, pady=10, sticky=NW)

# Create buttons

## Refresh Subregion Selection
subregionRefreshButton = Button(rightFrame, text="Refresh Subregions", width=26, command=refreshSubregions)
subregionRefreshButton.grid(row=6, column=0, columnspan=10, ipady=5)

## Close Window
closeButton = Button(rightFrame, text="Close", width=26, command=mainWindow.destroy)
closeButton.grid(row=7,column=0,columnspan=10, ipady=5)

# Create ListBox's
## Deals Selector ListBox
dealList = Listbox(leftFrame, height=10, width=50)
dealList.grid(row=1, column=3, padx=10, pady=10, sticky=NW)

## Subregion Selector ListBox
subregionListBox = Listbox(leftFrame, height=10, width=35)
subregionListBox.grid(row=1, column=0, padx=10, pady=10, sticky=NW)

# Create Scrollbar (dealList)
dealScroller = Scrollbar(leftFrame)
dealScroller.grid(row=1, column=4, sticky=W)
dealList.configure(yscrollcommand=dealScroller.set)
dealScroller.configure(command=dealList.yview)

# Create Scrollbar (subregionListBox)
subregionScroller = Scrollbar(leftFrame)
subregionScroller.grid(row=1, column=2, sticky=W)
subregionListBox.configure(yscrollcommand=subregionScroller.set)
subregionScroller.configure(command=subregionListBox.yview)

# Create Click Bindings
## Refresh Deal / Dispensary Details when a deal is clicked
dealList.bind('<<ListboxSelect>>', refreshDetails)

## Refresh Deals listing when a subregion is selected
subregionListBox.bind('<<ListboxSelect>>', refreshsubregionDeals)

## Open Menu when entrybox is clicked
dispoURLEntryBox.bind("<Button-1>", lambda e: openMenuURL())

# Initiate mainWindow
mainWindow.mainloop()