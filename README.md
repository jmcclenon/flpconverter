# fplconverter

fplconverter is a web application built with Flask to convert flight plan files between the .fpl (Garmin XML format) and .fms (X-Plane) formats. The application offers a simple, user-friendly interface for uploading your flight plan files and downloading the converted results.

## Features

- Converts .fpl files to .fms format
- Easy-to-use web interface
- Supports both Garmin and X-Plane flight plan files

## Installation

### Requirements

- Python 3.8+
- Flask 2.0.1+
- SQLAlchemy 1.4.15+

### Installation Steps

Clone the repository:

```
git clone https://github.com/jmcclenon/fplconverter.git
```

Change into the cloned repository:

```
cd fplconverter
```

Create a virtual environment:

```
python3 -m venv venv
```

Activate the virtual environment:

On Unix or MacOS, run:

```
source venv/bin/activate
```

On Windows, run:

```
.\venv\Scripts\activate
```

Install the required packages:

```
pip install -r requirements.txt
```

Run the application:

```
flask run
```

You can now access the application at `http://127.0.0.1:5000`.

## Usage

To use fplconverter:

1. Click the "Choose File" button and select the flight plan file you want to convert.
2. Click the "Convert" button.
3. The app will process the file and offer a download link for the converted file.

## Contributing

We welcome contributions! Please see the issues section to find something you'd like to work on. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.