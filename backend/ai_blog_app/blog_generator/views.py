from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json 
import os
from pytube import YouTube
from yt_dlp import YoutubeDL
import assemblyai as aai
import openai
from .models import BlogPost

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_TOKEN')
API_KEY_OPENAI = os.getenv('API_KEY')

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'Invalid data sent'}, status=400)
        
        # Get the title
        title = yt_title(yt_link)
        print(title)
        
        # Get the transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error':'Transcription failed'}, status=500)
        
        # Get OpenAI to comment
        blog_content = generate_blog_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({'error':'Blog generation failed'}, status=500)
        
        # Save blog to database
        new_blog_article = BlogPost.objects.create(user=request.user, youtube_title=title, youtube_link=yt_link, generated_content=blog_content)
        new_blog_article.save()
        
        # return blog as response
        
        
        return JsonResponse({'content':blog_content})
    else:
        return JsonResponse({'error':'Invalid request method'}, status=405)
    
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            downloaded_file = ydl.prepare_filename(info_dict)
            
            base, ext = os.path.splitext(downloaded_file)
            mp4_file = f"{base}.mp4"
            os.rename(downloaded_file, mp4_file)
            
            print(f"Audio file downloaded and saved as: {mp4_file}")
            return mp4_file
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None


def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = API_KEY
    
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_file)
    return transcript.text
    
    
def generate_blog_from_transcript(transcript):
    openai.api_key = API_KEY_OPENAI
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article. Write it based on the transcript, but don't make it look like a YouTube video; make it look like a proper blog article:\n\n{transcript}\n\nArticle:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    blog_content = response['choices'][0]['message']['content']
    return blog_content
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request,user)
            return redirect('/')
        
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {"error_message": error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request,user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html',{'error_message':error_message})

        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html',{'error_message':error_message})
        
    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('/')

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'all-blog.html', {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_details = BlogPost.objects.get(id=pk)
    if request.user == blog_article_details.user:
        return render(request, 'blog-details.html', {'blog_article_details': blog_article_details})
    else:
        return redirect('/')
    