# university: Projects prior to graduation

## OCR System project

The OCR System is a desktop application that uses the PyQt5, OpenCV, and pytesseract libraries. Its main functions include:

- Image preprocessing options to improve text recognition results.
- Displaying and saving the recognized text to the Clipboard or to a file.

### Demo

![Demo](https://github.com/vinhgiga/university/blob/master/OCR_System/demo/demo.gif)

### Installation

#### Requirements

- Windows
- Python 3.9

#### Installation on Windows

Clone this repository:

```powershell
> git clone https://github.com/vinhgiga/university
```

Change working directory to OCR_System:

```powershell
> cd OCR_System
```

Create and activate a Python virtual environment (optional):

```powershell
> python -m venv .venv
> .venv\Scripts\activate
```

Install Python modules:

```powershell
> pip install -r requirements.txt
```

Run app:

```powershell
> python main.py
```
