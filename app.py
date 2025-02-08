from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import replicate
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np
import requests
import logging

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
GENERATED_FOLDER = 'static/generated/'  # Save generated images in the static folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Function to read the Replicate API key from a file
def read_api_key():
    with open('api_key.txt', 'r') as file:
        return file.read().strip()

# Read the API key
api_key = read_api_key()
os.environ["REPLICATE_API_TOKEN"] = api_key

# Ensure the uploads and generated directories exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Redirect to the generate page with the file path
    return render_template('generate.html', file_path=file_path)

@app.route('/generate', methods=['POST'])
def generate():
    environment = request.form['environment']
    lighting = request.form['lighting']
    angle = request.form['angle']
    file_path = request.form['file_path']
    
    # Generate the image using Replicate API (Stable Diffusion)
    image_url = generate_image_from_api(file_path, environment, lighting, angle)
    
    return render_template('results.html', image_url=image_url)

def generate_image_from_api(file_path, environment, lighting, angle):
    # Create a prompt for the image generation
    prompt = f"A 4K wallpaper like full sized photorealistic image of the CAD model located at {file_path} in a {environment} with {lighting} lighting from a {angle} angle."
    
    # Call the Replicate API to generate the image
    try:
        logging.debug(f"Sending prompt to Replicate API: {prompt}")
        
        # Use the Stable Diffusion model on Replicate
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={"prompt": prompt}
        )
        
        # Log the API response
        logging.debug(f"Replicate API response: {output}")
        
        # Check if the output is valid
        if output and len(output) > 0:
            image_url = output[0]  # The first URL in the output list
            logging.debug(f"Generated image URL: {image_url}")
            
            # Download the image and save it to the generated folder
            generated_image_path = os.path.join(app.config['GENERATED_FOLDER'], 'generated_image.png')
            download_image(image_url, generated_image_path)
            
            # Return the URL to the generated image
            return url_for('static', filename='generated/generated_image.png')
        else:
            logging.error("No image URL found in the API response.")
            return None
    except replicate.exceptions.ReplicateError as e:
        logging.error(f"Replicate API error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return None

def download_image(url, save_path):
    """Download an image from a URL and save it to the specified path."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            logging.debug(f"Image saved to {save_path}")
        else:
            logging.error(f"Failed to download image from {url}. Status code: {response.status_code}")
            raise Exception(f"Failed to download image from {url}")
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        raise

@app.route('/generate_image')
def generate_image():
    # Create an image using PIL
    img = Image.new('RGB', (200, 200), color='blue')
    
    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)  # Move to the beginning of the BytesIO object
    
    return send_file(img_io, mimetype='image/png')

@app.route('/generate_plot')
def generate_plot():
    # Create a simple plot
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure()
    plt.plot(x, y)
    plt.title('Sine Wave')

    # Save the plot to a BytesIO object
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)  # Move to the beginning of the BytesIO object
    plt.close()  # Close the plot to free memory

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)