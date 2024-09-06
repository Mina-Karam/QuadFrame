import os
import uuid
import numpy as np
import cv2
import subprocess as sp
import shutil
from flask import Flask, render_template, request, send_from_directory

# Check dependencies function
def check_dependencies():
    try:
        import flask
        import numpy
        import cv2
    except ImportError as e:
        print(f"Missing dependency: {e.name}")
        return False
    return True

# Check dependencies and install if necessary
if not check_dependencies():
    print("Installing dependencies...")
    os.system("install_dependencies.bat")
    if not check_dependencies():
        raise Exception("Failed to install dependencies. Please install them manually.")
    else:
        print("Dependencies installed successfully.")

# Your existing Flask application code starts here

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {
    'png', 'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'drc',
    'gif', 'gifv', 'mng', 'avi', 'mov', 'qt', 'wmv', 'rm', 'rmvb',
    'asf', 'mp4', 'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv',
    'm2v', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv',
    'f4v', 'f4p', 'f4a', 'f4b', 'yuv'
}  # Source: https://en.wikipedia.org/wiki/Video_file_format

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # File size limit = 100MB

def hologram(infile, outfile, screen_below_pyramid=False):
    '''Transforms infile video into a hologram video with no audio track and saves it to outfile.'''
    capture = cv2.VideoCapture(infile)
    
    if capture.isOpened():
        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)  # Width of the video
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Height of the video
        fps = capture.get(cv2.CAP_PROP_FPS)  # Frames per second
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames

    # Retrieve form data from Flask request
    length = int(request.form['length'])
    d = int(request.form['d'])
    padding = int(request.form['padding'] or 0)

    # Validate input values
    assert 0 < length <= 5000, 'Length must be within (0, 5000].'
    assert 0 < d < length / 2, 'd must be within (0, length/2).'
    assert 0 <= 2 * padding < min(2 * d, length / 2 - d), 'Padding is too large.'

    # Ensure length is even for convenience
    if length % 2:
        length += 1

    # Open the input video file again
    cap = cv2.VideoCapture(infile)
    bgd = np.zeros((length, length, 3), np.uint8)  # Black background image
    new_wid = 2 * d - 2 * padding  # Width of the hologram area
    new_hgt = int(float(new_wid) / width * height)  # Height of the hologram area

    # Adjust height if necessary to fit within the defined limits
    if new_hgt + d + 2 * padding > length / 2:
        new_hgt = int(length / 2 - d - 2 * padding)
        new_wid = int(float(new_hgt) / height * width)

    # Ensure dimensions are even for compatibility
    if new_wid % 2:
        new_wid -= 1
    if new_hgt % 2:
        new_hgt -= 1

    # Define video codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outfile, fourcc, fps, (length, length))

    # Initialize frame counter
    frame_count = 0

    # Process each frame of the input video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to fit the hologram area
        resized_frame = cv2.resize(frame, (new_wid, new_hgt))

        # Arrange resized frames according to hologram pyramid geometry
        if screen_below_pyramid:
            resized_frame = cv2.flip(resized_frame, 0)
        bgd[length // 2 + d + padding:length // 2 + d + new_hgt + padding, length // 2 - new_wid // 2:length // 2 + new_wid // 2] = resized_frame
        bgd[length // 2 - d - padding - new_hgt:length // 2 - d - padding, length // 2 - new_wid // 2:length // 2 + new_wid // 2] = cv2.flip(resized_frame, -1)
        bgd[length // 2 - new_wid // 2:length // 2 + new_wid // 2, length // 2 + d + padding:length // 2 + d + new_hgt + padding] = cv2.flip(cv2.transpose(resized_frame), 0)
        bgd[length // 2 - new_wid // 2:length // 2 + new_wid // 2, length // 2 - d - padding - new_hgt:length // 2 - d - padding] = cv2.flip(cv2.transpose(resized_frame), 1)

        # Write the frame to the output video
        out.write(bgd)

        # Increment frame counter and display progress
        frame_count += 1
        progress_percentage = (frame_count / total_frames) * 100
        print(f"Processing: {progress_percentage:.2f}% complete", end="\r")

    # Release resources
    cap.release()
    out.release()

def allowed_file(filename):
    '''Checks if the filename has an allowed extension.'''
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

# Define a route for the default URL, which loads the upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Create a unique directory for each upload using UUID
            upload_dirname = str(uuid.uuid4())  # Generate new UUID for directory
            my_dir = os.path.abspath(os.path.dirname(__file__))
            uploadpath = os.path.join(my_dir, app.config['UPLOAD_FOLDER'], upload_dirname)
            os.makedirs(uploadpath, exist_ok=True)

            # Generate unique filenames using UUID
            filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[-1]}"
            filepath = os.path.join(uploadpath, filename)
            file.save(filepath)

            # Check if 'screen_below_pyramid' option is selected
            screen_below_pyramid = 'upsidedown' in request.form

            # Define output paths using UUID
            outpath = os.path.join(uploadpath, f"{uuid.uuid4()}.mp4")
            output_filename = f"{uuid.uuid4()}.mp4"

            # Call the hologram function to transform the video
            hologram(filepath, outpath, screen_below_pyramid=screen_below_pyramid)

            # Use ffmpeg to add an audio track (if available) and create final output
            sp.call(['ffmpeg', '-i', outpath, '-i', filepath, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0?', os.path.join(uploadpath, output_filename)])

            # Return the final video as an attachment for download
            return send_from_directory(uploadpath, output_filename, as_attachment=True)

    # Render the upload form template by default
    return render_template('form_submit.html')

# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
