from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import CustomUser

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email is already registered'})
        
        otp = random.randint(100000, 999999)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = otp
        
        return redirect('otp_verification')
    return render(request, 'signup.html')

def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if int(entered_otp) == request.session['otp']:
            email = request.session['email']
            password = request.session['password']
            user = CustomUser.objects.create_user(email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP'})
    return render(request, 'otp_verification.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm

@login_required
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != request.user:
        return redirect('blog_list')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != request.user:
        return redirect('blog_list')
    
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})
