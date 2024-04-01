from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CVForm

def upload_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            return redirect('cv_uploaded')
    else:
        form = CVForm()
    return render(request, 'joinus/upload_cv.html', {'form': form})

def cv_uploaded(request):
    return render(request, 'joinus/cv_uploaded.html')
