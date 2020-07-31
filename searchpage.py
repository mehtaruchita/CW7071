# Importing Libraries
import tkinter as tk
import webbrowser
from functools import partial
from tkinter import *
from tkinter import scrolledtext

from Query_Processor import queryresult
from tkHyperlinkManager import HyperlinkManager


# Define all the functions
def search(searchQuery, resultText, resultQuery, resultFrame, mainFrame):
    searchresults = queryresult(searchQuery)
    resultText.delete("1.0", "end")
    hyperlink = HyperlinkManager(resultText)
    if len(searchresults) > 0:
        for key, value in searchresults.items():
            # Showing hyperlink in result
            resultText.insert(END, key, hyperlink.add(partial(webbrowser.open, key)))
            resultText.insert(END, "\n")
            # Showing Name of Professors in the result
            resultText.insert(END, "Name: " + value[0][0])
            resultText.insert(END, "\n")
            # Showing Title of Professor in the result
            resultText.insert(END, "Title: " + value[0][1])
            resultText.insert(END, "\n")
            # Showing Contact details of Professor in the result
            resultText.insert(END, "Contact: " + value[0][2])
            resultText.insert(END, "\n")
            # Showing Professor Info of 200 characters in the result
            resultText.insert(END, value[0][4][:200] + "...")
            resultText.insert(END, "\n")
            resultText.insert(END, "\n")
            resultText.insert(END, "\n")
    # Allowes user to delete query once got the result
    resultQuery.delete(0, END)
    # Allows user to put new query in result window
    resultQuery.insert(END, searchQuery)
    mainFrame.grid_forget()
    resultFrame.grid(row=0, column=0)


# I'm feeling lucky result fetching
def openfirstsearch(searchQuery):
    searchresults = queryresult(searchQuery)
    if len(searchresults) > 0:
        for key, value in searchresults.items():
            webbrowser.open(key)
            return


# Return back to home page by clicking Data Science Search Engine Button
def returnhome(resultFrame, mainFrame):
    resultFrame.grid_forget()
    mainFrame.grid(row=0, column=0)


# Graphical user interface using Tkinter
# Search Engine Home Page
window = tk.Tk()
window.title("Ruchita's Search Engine")

# Add the search frame
searchFrame = tk.Frame(window)
searchFrame.grid(row=0, column=0)

# Add a Label
lblSearch = tk.Label(searchFrame, text="Data Science Search Engine", font=("Product Sans", 15), foreground="blue")
lblSearch.grid(row=0, column=0, padx=10, pady=10)

# Add a Entry box for search query
queryEntry = tk.Entry(searchFrame, width=75)
queryEntry.grid(row=1, column=0, padx=10, pady=10)

# Add a Frame for search & I'm Feeling lucky button
frame = tk.Frame(searchFrame)
frame.grid(row=2, column=0)

# Add a Button
tk.Button(frame, text="Search", font=("Product Sans", 12),
          command=lambda: search(queryEntry.get(), textw, queryEntry2, searchResultFrame, searchFrame),
          width=20).grid(row=0, column=0, padx=10, pady=10)
tk.Button(frame, text="I'm Feeling Lucky",
          font=("Product Sans", 12),
          command=lambda: openfirstsearch(queryEntry.get()),
          width=20).grid(row=0, column=1, padx=10, pady=10)

# Add a search result Frame
searchResultFrame = tk.Frame(window)

# Add logo
lblSearch2Btn = tk.Button(searchResultFrame, text="Data Science Search Engine",
                          command=lambda: returnhome(searchResultFrame, searchFrame),
                          font=("Product Sans", 10), foreground="blue",
                          wraplength=100, justify="left")
lblSearch2Btn.grid(row=0, column=0, padx=10, pady=10)

# Add a frame
resultsbtnFrame = tk.Frame(searchResultFrame)
resultsbtnFrame.grid(row=0, column=1)

# Add a Entry box for search results page
queryEntry2 = tk.Entry(resultsbtnFrame, width=75)
queryEntry2.grid(row=0, column=0, padx=10, pady=10, sticky=W)

# Add a search button on search results page
photo = PhotoImage(file=r"C:\Users\Ruchita\PycharmProjects\CW-7071\search-icon.png").subsample(6, 6)
lblSearchResBtn = tk.Button(resultsbtnFrame,
                            command=lambda: search(queryEntry2.get(), textw, queryEntry2, searchResultFrame,
                                                   searchFrame),
                            image=photo)
lblSearchResBtn.grid(row=0, column=1, padx=10, pady=10)

# Add a scroll bar text widget for search result
textw = scrolledtext.ScrolledText(searchResultFrame, width=100)
textw.config(font=("Product Sans", 12), wrap='word')
textw.grid(row=1, column=1, padx=10, pady=10, sticky=N + S + E + W)

window.mainloop()
