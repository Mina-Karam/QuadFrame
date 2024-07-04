# QuadFrame

QuadFrame is a web application that converts videos into pseudo-hologram videos suitable for hologram projection devices.

## Overview

This project aims to provide a simple web interface for users to upload videos and convert them into pseudo-hologram format. It utilizes OpenCV for video processing and Flask for the web framework.

## Features

- Upload video files in various formats (supported formats listed below).
- Convert uploaded videos to pseudo-hologram format.
- Option to configure hologram parameters such as length, d, and padding.
- Supports both screen above and below the hologram pyramid configurations.
- Downloads the converted video automatically once processing is complete.

## Supported Video Formats

The application supports the following video formats:
- png, webm, mkv, flv, vob, ogv, ogg, drc
- gif, gifv, mng, avi, mov, qt, wmv, rm, rmvb
- asf, mp4, m4p, m4v, mpg, mp2, mpeg, mpe, mpv, m2v
- svi, 3gp, 3g2, mxf, roq, nsv, flv, f4v, f4p, f4a, f4b, yuv

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Mina-Karam/QuadFrame.git
   cd QuadFrame
   ```

2. Install dependencies:
   - Ensure Python 3.x is installed.
   - Create a virtual environment (optional but recommended):
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install dependencies from requirements.txt:
     ```
     pip install -r requirements.txt
     ```
    - **Install `ffmpeg` on Windows:**
        - Download `ffmpeg` from [ffmpeg.org](https://ffmpeg.org/download.html).
        - Extract the contents of the downloaded zip file.
        - Add the `bin` directory of `ffmpeg` to your system's PATH environment variable:
            - Right-click on "This PC" or "Computer" -> Properties -> Advanced System Settings -> Environment Variables.
            - Under System Variables, find the "Path" variable, select it, and click Edit.
            - Add the full path to the `bin` directory of `ffmpeg` (e.g., `C:\path\to\ffmpeg\bin`).
            - Click OK to save.
3. Run the application:
   ```
   python app.py
   ```
   Open your web browser and navigate to `http://localhost:5000`.

## Usage

1. Upload a video file using the provided form.
2. Enter the desired parameters: length, d, padding, and optionally select "Screen up" if placing the device above the hologram pyramid.
3. Click the "Submit" button to start the conversion process.
4. The converted video will be automatically downloaded once processing is complete.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create a GitHub issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
