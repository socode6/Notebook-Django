from django.shortcuts import render,redirect, get_object_or_404
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
    search_query = ''
    
    # Handle search via POST
    if request.method == "POST":
        search_query = request.POST.get('search', '')
        if search_query:
            all_notes = all_notes.filter(title__icontains=search_query) | all_notes.filter(content__icontains=search_query)
    
    # Send the notes to the HTML template using a dictionary (context)
    return render(request, 'notes/index.html', {'notes': all_notes, 'search_query': search_query})

def edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            note.title = title
            note.content = content
            note.save()
            messages.success(request, 'Your note has been updated successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please fill out all fields.')
    
    return render(request, 'notes/edit.html', {'note': note})

def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    if request.method == "POST":
        note.delete()
        messages.success(request, 'Your note has been deleted successfully!')
        return redirect('index')
    
    return render(request, 'notes/delete.html', {'note': note})