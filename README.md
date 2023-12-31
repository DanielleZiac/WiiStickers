# WiiStickers

A `stickerbooth` app that includes computer vision and promotes Sustainable Development Goals.

## Table of Contents
- [Features](#features)
- [Packages Installation](#packages-installation)
- [Usage](#usage)
- [Credits](#credits)

## Features
- [ ] Computer Vision (webcam connection)
- [ ] Camera Capture (save)
- [ ] Avatar Creation (image layering)
- [ ] Face Analysis (eyes, mouth)
- [ ] Color Detection (shirt color)
- [ ] Educational game (SDG quiz)
- [ ] QR code generation (link to web)
- [ ] Local storage (image storage)
- [ ] Web application (stickers deployment)
- [ ] Transaction History (database)

## Python
`python` and `pip`must be installed to start this program. Should use python@3.10 for package compatibility, especially with kivy not compatible with latest python version (3.12 at the time).

## Setup environment (one-time only)
```
python -m venv env
```

## Activate environment (always activate)
```
source env/bin/activate
```

## Packages Installation

```
pip install opencv-python
pip install imutils
pip install dlib
pip install "kivy[full]"
pip install qrcode
pip install autopep8 # for code formatting
```

## Format before commit
```
autopep8 [file.py]
```

## Usage

run 'python main.py'

## Credits

- Developer: Danielle Ziac Abril
- Course: CS 211 (Object-oriented Programming)
- Course Facilitator: Fatima Marie Agdon