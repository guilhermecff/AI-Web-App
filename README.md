# Video to Blog App

This Django application automates the process of converting video content into written blog posts. It accepts video links, downloads the videos in MP4 format, transcribes the audio using AssemblyAI, and then generates a well-crafted blog post using OpenAI's ChatGPT. The application's data is managed with PostgreSQL, hosted on Supabase, ensuring scalability and easy access.

## Features

- **Video Conversion:** 
  - **Link Input:** Users can input video links from platforms like YouTube.
  - **Download & Conversion:** The application uses Pytube and yt_dlp to download videos and convert them into MP4 format, ensuring compatibility and quality.
  
- **Automatic Transcription:** 
  - The audio from the video is automatically transcribed using the AssemblyAI API, producing accurate and detailed transcriptions.

- **Blog Post Generation:** 
  - The transcription is analyzed by ChatGPT, which generates a coherent and engaging blog post based on the video content. This feature allows content creators to quickly repurpose video content into written format for blogs, newsletters, and more.

- **Data Storage:**
  - All data, including video links, transcriptions, and blog posts, are securely stored in a PostgreSQL database hosted on Supabase. This ensures that the data is readily accessible and easy to manage.

## Use Case

This application is particularly useful for content creators, marketers, educators, and bloggers who frequently produce video content and want to extend their reach by converting their videos into written blog posts. By automating the transcription and content generation process, this app saves time and effort, allowing users to focus on creating more content and engaging with their audience.

## Requirements

- Python 3.x
- Django 3.x or higher
- PostgreSQL
- Supabase account
- AssemblyAI API key
- OpenAI API key
- Pytube library (for video downloading)
- yt_dlp library (for enhanced video downloading)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/guilhermecff/AI-Web-App.git
   cd AI-Web-App

2. Install the dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Set up the PostgreSQL database on Supabase and configure the Django settings to connect to it. Update the DATABASES setting in settings.py with your Supabase credentials.

4. Add your AssemblyAI and OpenAI API keys to the environment variables:

5. Run database migrations:
   ```bash
   python manage.py migrate

6. Start the server
   ```bash
   python manage.py runserver

## Usage

1. Navigate to the app in your web browser.
2. Input a video link and submit the form.
3. The video will be downloaded, converted, and transcribed.
4. A blog post will be generated and stored in the database.
5. View the generated blog post in the app or export it as needed.


