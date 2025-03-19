# Mematic - Meme, GIF & Sticker Generator 🎨

A powerful web application built with Streamlit that allows users to:
- Create memes using templates or custom images
- Generate GIFs from images or videos
- Create stickers with optional background removal
- Add custom text to all creations

## Features
- 🖼️ Meme Generator with templates and custom image upload
- 🎞️ GIF Creator supporting both image sequences and video input
- 🧩 Sticker Maker with background removal capability
- Text customization with color picker
- Easy download options for all generated content

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-directory>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure you have the Impact font file (`impact.ttf`) in your project directory

## Running Locally

Run the application using:
```bash
streamlit run gothilla.py
```

## Deployment Options

### Deploy on Streamlit Cloud (Recommended)
1. Create an account on [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. Deploy directly from the Streamlit Cloud dashboard

### Deploy on Heroku
1. Create a `Procfile`:
```
web: streamlit run gothilla.py
```
2. Initialize git and push to Heroku:
```bash
git init
heroku create your-app-name
git add .
git commit -m "Initial commit"
git push heroku main
```

## Requirements
See `requirements.txt` for a full list of dependencies.

## Note
- For the background removal feature in Sticker Maker, ensure you have sufficient computational resources
- Some features may require additional memory depending on image/video size 