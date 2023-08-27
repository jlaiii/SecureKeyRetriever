# KeySecure Server

KeySecure Server is a simple Python script that provides a secure way to manage and retrieve keys through a basic web interface. It incorporates basic authentication to ensure only authorized users can access the keys.

## Features

- Securely manage and retrieve keys via a web interface.
- Basic authentication for authorized access.
- Easy-to-use interface for getting keys.
- Automatic removal of retrieved keys from the list.
- Option to customize the username and password for access.

## How to Use

1. Clone this repository to your local machine.
2. Customize the username and password in the `_check_credentials` function of the `KeyServerHandler` class in `main.py`.
3. Add the keys you want to manage to the `keys.txt` file.
4. Run the server by executing `main.py` using Python.
5. Access the server by opening a web browser and navigating to `http://localhost:8000`.

## Dependencies

- Python 3.x

## Usage Example

1. Open a web browser and navigate to `http://localhost:8000`.
2. Enter your authorized credentials (username and password) when prompted.
3. The server will display the available keys.
4. Click "Get Another Key" to retrieve a key. The retrieved key will be removed from the list.
5. The keys are stored in the `keys.txt` file.

## Contributing

Contributions to the KeySecure Server project are welcome! Feel free to submit issues, pull requests, or suggestions.
