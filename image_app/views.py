from django.shortcuts import render
from .models import Image
from .forms import ImageForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'index.html')

def list(request):
    tweets = Image.objects.all().order_by('-created_at')
    return render(request,'list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('list')
    else:
        form = ImageForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Image,pk=tweet_id,user = request.user)
    if request.method =='POST':
        form = ImageForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('list')
    else:
        form = ImageForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Image,pk=tweet_id,user=request.user)
    if request.method =='POST':
        tweet.delete()
        return redirect("list")
    return render(request,'tweet_delete.html',{'tweet':tweet})

def register(request):
   
    if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
           user = form.save(commit=False)
           user.set_password(form.cleaned_data['password1'])
           user.save()
           login(request,user)
           return redirect("list")
    else:
       form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form}) 