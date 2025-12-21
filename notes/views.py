from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Note  

def home(request):
    if request.method == "POST":
        # Get data from the form
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            Note.objects.create(title=title, content=content)
            messages.success(request, 'Your note has been saved successfully!')
            # REMOVE the redirect. Just let the code fall through to the render below.
        else:
            messages.error(request, 'Please fill out all fields.')

        
    return render(request, 'notes/home.html')

def index(request):
    # Fetch all notes from the database
    all_notes = Note.objects.all()
    
    # Send the notes to the HTML template using a dictionary (context)
    return render(request, 'notes/index.html', {'notes': all_notes})