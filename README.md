# 💬 CSChat
A Chat App for CS471 Senior Capstone I

## Project Description
CSChat is a real-time chat room application that allows multiple users to communicate simultaneously. Users can join different chat rooms, send messages, and view messages from other users. The application employs encryption for secure communication between clients and the server.

## Features
- Real-time messaging
- Self-assigned usernames (no authentication required)
- Join existing chat rooms
- View messages from other users
- Encrypted communication for enhanced security

# Basic Guide
This section is intended for:
- Users who downloaded the basic standalone executable application.
- Server hosters who do not wish to modify the code to create a custom chat room.

## Installation Instructions
Download the [latest release files](https://github.com/RootCellar/chat-app/releases/tag/v1.0.0) and run them as standalone executables.

## Basic User Guide
1. **Open the application**: Launch the executable file
2. **Joining a Chat Room**: Enter the following information, provided by the chat room host:
   - **Server**: The IP address or hostname of the server.
   - **Port**: The port number the server is listening on (default is 45000).
   - **Username**: Your desired username to use in the chat room.
3. **Join the Chat Room**: Click "Join" at the bottom of the application window.
4. **Send Messages**: Type your message in the input field and press "Enter" or click the "Send" button.
5. **Recieve Messages**: Messages from other users will automatically appear in the chat window.

## Basic Server Host Guide
To host a chat room using the standalone server executable:

1. **Launch the Server Executable**: 
   - Open the server executable file
   - The server listens on a default port of `45000`.

2. **Provide Connection Information**:
   - Share your computer's **IP address** and the **port number** (default is `45000`) with users who wish to connect. 
   - Users can find your local IP address by using commands such as `ipconfig` (Windows) or `ifconfig` (Linux/Mac) in the terminal.

3. **Inform Users**: Let users know they need to enter the server IP address and port in their client application to connect to your chat room.

# Advanced Guide 
This section is intended for those who wish to modify the code to create a custom client and server. 

## Cloning the repository to modify the source code
To get the source code in order to modify, go into a desired file location, enter the following command:
```
https://github.com/RootCellar/chat-app.git
```

## Build Instructions 
After modifying the source code, you must follow the following steps to compile the client and server executables

### Install PyInstaller
To build the application from source, first install PyInstaller:
```
python3 -m pip install pyinstaller
```
### Build (Windows)
```
.\bin\build.bat
```
### Build (Linux)
```
bin/build.sh
```

## Finding/Opening the Executable
The executable files will be found in `dist`, which can be used in a number of ways, such as:
1. Shared and distributed, which can be opened with ease.
2. Enter the following commands in a terminal to open the executables from the terminal.
```
dist/server
...
dist/client
```

## Advanced User Instructions
If the client code was not modified, the instructions for the user will be no difference than the unmodified experience.
1. **Open the application**: Launch the executable file
2. **Joining a Chat Room**: Enter the following information, provided by the chat room host:
   - **Server**: The IP address or hostname of the server.
   - **Port**: The port number the server is listening on (default is 45000).
   - **Username**: Your desired username to use in the chat room.
3. **Join the Chat Room**: Click "Join" at the bottom of the application window.
4. **Send Messages**: Type your message in the input field and press "Enter" or click the "Send" button.
5. **Recieve Messages**: Messages from other users will automatically appear in the chat window.

## Advanced Server Host Instructions
If the server code was not modified, the instructions for the host will be no difference than the unmodified experience

1. **Launch the Custom Server Executable**: 
   - Open the server executable file
   - The server listens on a default port of `45000`.

2. **Provide Connection Information**:
   - Share your computer's **IP address** and the **port number** (default is `45000`) with users who wish to connect. 
   - Users can find your local IP address by using commands such as `ipconfig` (Windows) or `ifconfig` (Linux/Mac) in the terminal.

3. **Inform Users**: Let users know they need to enter the server IP address and port in their client application to connect to your chat room.

# Acknowledgments
1. **Contributors:** Thanks to everyone who has contributed to the project. Contributers include:
   - Darian Marvel
   - Orlandis Brown
   - Dylan Maltos
   - Anand Egan
2. **Python:** The programming language used to build this application.
3. **NaCl (Networking and Cryptography Library):** For providing secure encryption features used in the chat application.
4. **Socket Programming:** For enabling real-time communication between clients and the server.
