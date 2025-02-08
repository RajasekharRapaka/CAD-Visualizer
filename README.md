# CAD-Visualizer
This project is a Flask-based web application that allows users to upload CAD files and generate photorealistic images using the Google Gemini API. Users can customize the generated images by selecting different environments, lighting conditions, and angles. 

# Photorealistic Image Generation Web App

## Description

This project is a Flask-based web application that allows users to upload CAD files and generate photorealistic images using the Google Gemini API. Users can customize the generated images by selecting different environments, lighting conditions, and angles. The application also includes functionality to display generated images directly in the browser, leveraging libraries like PIL and Matplotlib for additional image processing and visualization.

## Features

- Upload CAD files (e.g., DWG, DXF).
- Generate photorealistic images based on user-defined parameters.
- Customize image generation with options for environment, lighting, and angle.
- Display generated images directly in the browser.
- Use of PIL and Matplotlib for additional image processing.

## Technologies Used

- Python
- Flask
- Google Gemini API
- PIL (Pillow)
- Matplotlib
- HTML/CSS

## Installation

2. Create a virtual environment:
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   pip install -r requirements.txt

4. Create a file named api_key.txt in the root directory and add your Google Gemini API key.

5. Run the application:
    python app.py

6. Open your web browser and go to http://127.0.0.1:5000.

Usage
Upload a CAD file using the upload form.
Select the desired environment, lighting, and angle for the image generation.
Click "Generate Image" to create and view the photorealistic image.
Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Google Gemini API
Flask
Pillow
Matplotlib   
