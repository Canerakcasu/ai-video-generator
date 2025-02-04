# AI Video Generator

## Description
AI Video Generator is a web application that allows users to generate videos based on a given topic using AI technology. The application leverages OpenAI's GPT model to create scripts and uses Pexels for fetching relevant images. MoviePy is used to combine these images with the script to generate a video.

## Features
- **AI-powered Script Generation**: The application uses OpenAI's GPT-4 model to generate scripts based on the input topic.
- **Image Fetching from Pexels**: Relevant images are fetched using the Pexels API to complement the generated script.
- **Video Creation**: The application combines the generated script with the fetched images and produces a video using MoviePy.
- **User Interface**: A simple and user-friendly interface where users can input a topic and generate a video.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **AI Model**: OpenAI GPT-4 (for script generation)
- **Image Source**: Pexels API (for fetching images)
- **Video Creation**: MoviePy (for video generation)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Install the required libraries:
  ```bash
  pip install openai requests moviepy flask

OPENAI_API_KEY=your_openai_api_key
PEXELS_API_KEY=your_pexels_api_key


git clone <repository_url>
cd ai-video-generator
python app.py

Open your browser and go to http://127.0.0.1:5000.
Usage
Enter a topic in the input field.
Click "Generate Video".
Wait for the AI to generate the video, and the video will be displayed once ready.
License
This project is licensed under the MIT License.

Author
caner akcasu
