##############################################################################################
#                  Dylan Maltos | Darian Marvel | Anand Egan | Orlandis Brown                #
#                                         CSChat.py                                          #
#                GUI/Main Program for CS471 Senior Capstone I Project - Chat App             #
##############################################################################################

##############################################################################################
#                                     Library Imports                                        #
##############################################################################################

from .Client import Client

import tkinter as tk
from tkinter import simpledialog, font

class ChatConnection:
    client = Client()
    username = None
    def __init__(self, server_address, username):
        self.username = username
        connected = self.client.connect(server_address, 45000)
        if connected is False:
            print("Could not connect to server!")
            return

        self.client.write(1, self.username)

    def get_next_message(self):
        return self.client.read()

def append_chat_history(chat_history_frame, message):
    if message:
        # Append the message to the chat display.
        chat_history_frame.config(state=tk.NORMAL)
        chat_history_frame.insert(tk.END, message + "\n")
        chat_history_frame.config(state=tk.DISABLED)

        # Scroll to the end of the chat display.
        chat_history_frame.yview(tk.END)


def display_chat(root, connection):
    # Initalize the chatbox for the chatroom.
    chatBox = tk.Frame(root)
    chatBox.grid(row=1, column=0, sticky="nsew")
    chatBox.grid_rowconfigure(0, weight=1)
    chatBox.grid_columnconfigure(0, weight=1)

    # Configure grid.
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Intialize text widget to display chat messages.
    chatDisplay = tk.Text(chatBox, state=tk.DISABLED, wrap=tk.WORD)
    chatDisplay.grid(row=0, column=0, sticky="nsew")

    # Initialize the chatbox's scroll bar.
    scrollBar = tk.Scrollbar(chatBox, command=chatDisplay.yview)
    scrollBar.grid(row=0, column=1, sticky="ne")
    chatDisplay.config(yscrollcommand=scrollBar.set)

    # Initialize the message entry box for the chatroom.
    messageEntry = tk.Entry(root)
    messageEntry.grid(row=2, column=0, sticky="ew")

    def send_my_message():
        if messageEntry.get():
            append_chat_history(chatDisplay, "> " + messageEntry.get())
            connection.client.chat(messageEntry.get())
            # Clear the message entry box after sending the message.
            messageEntry.delete(0, tk.END)

    # Initialize the button to send messages.
    messageSend = tk.Button(root, text="Send", command=send_my_message)
    messageSend.grid(row=3, column=0, sticky="ew")

    # Extend chatbox to fit.
    chatBox.grid_rowconfigure(0, weight=1)
    chatBox.grid_columnconfigure(0, weight=1)

    def get_incoming_message_loop():
        if connection.client.is_connected() is False:
            print('Client disconnected')
            exit(0)

        message = connection.get_next_message()
        if message is not None:
            if message.get_code() == 0:
                message = message.get_message().decode("utf-8").replace("\n", "")
                append_chat_history(chatDisplay, "# " + message)

        root.after(100, get_incoming_message_loop)

    get_incoming_message_loop()

def display_join(root):
    # Initialize the application's welcome window.
    welcome_window = tk.Frame(root)
    welcome_window.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    welcome_window.grid_rowconfigure(0, weight=1)
    welcome_window.grid_rowconfigure(1, weight=3)
    welcome_window.grid_rowconfigure(2, weight=1)
    welcome_window.grid_columnconfigure(0, weight=1)

    # Initialize the title - "Welcome to CSChat" on the application's welcome window.
    title = tk.Label(welcome_window, text="Welcome to CSChat", font=("Arial", 24))
    title.grid(row=0, column=0)
    title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    join_input_frame = tk.Frame(welcome_window)
    join_input_frame.grid(row=1, column=0, sticky="ew", padx=80)
    join_input_frame.grid_rowconfigure(0, weight=1)
    join_input_frame.grid_columnconfigure(0, weight=1)
    join_input_frame.grid_columnconfigure(1, weight=5)

    # Ask the user for server address.
    server_address_label = tk.Label(join_input_frame, text = 'Server:')
    server_address_label.grid(row=0, column=0)
    server_address = tk.Entry(join_input_frame)
    server_address.grid(row=0, column=1, sticky="ew", pady=5)
    server_address.insert(0, 'localhost')

    # Ask the user for username.
    username_label = tk.Label(join_input_frame, text = 'Username:')
    username_label.grid(row=1, column=0)
    username = tk.Entry(join_input_frame)
    username.grid(row=1, column=1, sticky="ew")
    username.insert(0, 'Guest')

    def join_server(server_address, username):
        def callback():
            if server_address.get() and username.get():
                welcome_window.grid_remove()
                connection = ChatConnection(server_address.get(), username.get())
                display_chat(root, connection)
        return callback

    # Initialize the join button on the application's welcome window.
    join_button = tk.Button(welcome_window, text="Join", command=join_server(server_address, username))
    join_button.grid(row=2, column=0, sticky='n', pady=1)  # Directly below the title label

def init(root):
    display_join(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSChat")
    font.nametofont("TkDefaultFont").configure(
        family="Arial",
        size=14
    )
    font.nametofont("TkTextFont").configure(
        family="Arial",
        size=14
    )
    root.geometry("640x480")
    root.resizable(True, True)
    root.eval('tk::PlaceWindow . center')
    init(root)
    root.mainloop()
