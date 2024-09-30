##############################################################################################
#                  Dylan Maltos | Darian Marvel | Anand Egan | Orlandis Brown                #
#                                         CSChat.py                                          #
#                GUI/Main Program for CS471 Senior Capstone I Project - Chat App             #
##############################################################################################

##############################################################################################
#                                     Library Imports                                        #
##############################################################################################

import tkinter as tk
from tkinter import simpledialog, font


##############################################################################################
#                           class CSChat - Main for Tkinter GUI                              #
##############################################################################################

class CSChat:
    # Initialize the Tkinter GUI application.
    def __init__(self, root):
        self.root = root
        self.root.title("CSChat")
        self.root.geometry("1920x1080")  
        self.root.resizable(True, True)  

        # Initialize the application's welcome window.
        self.welcomeWindow = tk.Frame(root)
        self.welcomeWindow.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.welcomeWindow.grid_rowconfigure(0, weight=1)
        self.welcomeWindow.grid_rowconfigure(2, weight=1)
        self.welcomeWindow.grid_columnconfigure(0, weight=1)

        # Initialize the title - "Welcome to CSChat" on the application's welcome window.
        self.title = tk.Label(self.welcomeWindow, text="Welcome to CSChat", font=("Arial", 24))
        self.title.grid(row=0, column=0, pady=100)

        # Initialize the join button on the application's welcome window.
        self.join = tk.Button(self.welcomeWindow, text="Join", font=("Arial", 16), command=self.askUsername)
        self.join.grid(row=1, column=0)  # Directly below the title label

    ##########################################################################################
    #            Function askUsername() - Dialog window prompting for a username.            #
    ##########################################################################################

    def askUsername(self):
        # Configure default font for dialog.
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=15)  # Set the size to 16 or any suitable size

        # Ask the user for a username.
        self.username = simpledialog.askstring("Username", "Enter your username:")

        if self.username:
            # If username is entered, hide the welcome frame and show the chatroom.
            self.welcomeWindow.grid_remove()  
            self.createRoom()

        # Reset the font size to default after dialog is closed.
        default_font.configure(size=12)  

    ##########################################################################################
    #                   Function createRoom() - Window for the chatroom.                     #
    ##########################################################################################

    def createRoom(self):
        # Initalize the chatbox for the chatroom.
        self.chatBox = tk.Frame(self.root)
        self.chatBox.grid(row=1, column=0, sticky="nsew")
        self.chatBox.grid_rowconfigure(0, weight=1)
        self.chatBox.grid_columnconfigure(0, weight=1)

        # Configure grid.
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Intialize text widget to display chat messages.
        self.chatDisplay = tk.Text(self.chatBox, font=("Arial", 14), state=tk.DISABLED, wrap=tk.WORD)
        self.chatDisplay.grid(row=0, column=0, sticky="nsew")

        # Initialize the chatbox's scroll bar.
        self.scrollBar = tk.Scrollbar(self.chatBox, command=self.chatDisplay.yview)
        self.scrollBar.grid(row=0, column=1, sticky="ne")
        self.chatDisplay.config(yscrollcommand=self.scrollBar.set)

        # Initialize the message entry box for the chatroom.
        self.messageEntry = tk.Entry(self.root, font=("Arial", 14))
        self.messageEntry.grid(row=2, column=0, sticky="ew")

        # Initialize the button to send messages.
        self.messageSend = tk.Button(self.root, text="Send", font=("Arial", 14), command=self.sendMessage)
        self.messageSend.grid(row=3, column=0, sticky="ew")

        # Extend chatbox to fit.
        self.chatBox.grid_rowconfigure(0, weight=1)
        self.chatBox.grid_columnconfigure(0, weight=1)

    ##########################################################################################
    #        Function enterMessage() - Inserts user input into the message entry box.        #
    ##########################################################################################

    def enterMessage(self, symbol):
        # Insert the selected symbol into the message entry
        self.messageEntry.insert(tk.END, symbol)

    ##########################################################################################
    #           Function sendMessage() - Sends message input to the chat display.            #
    ##########################################################################################

    def sendMessage(self):
        # Get the message from the message entry box.
        message = self.messageEntry.get()

        if message:
            # Append the message to the chat display.
            self.chatDisplay.config(state=tk.NORMAL)
            self.chatDisplay.insert(tk.END, f"{self.username}: {message}\n")
            self.chatDisplay.config(state=tk.DISABLED)

            # Scroll to the end of the chat display.
            self.chatDisplay.yview(tk.END)

            # Clear the message entry box after sending the message.
            self.messageEntry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSChat(root)
    root.mainloop()

##############################################################################################
#                                                                                            #
##############################################################################################
