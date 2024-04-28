from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'index.html')

def signIn(request):
    return render(request, 'signIn.html')

def signUp(request):
    return render(request, 'signUp.html')
