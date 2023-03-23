from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Profile
from .forms import MessageForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages as django_messages


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def messages(request):
    chat_user = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
    else:
        form = MessageForm()

    if request.GET.get('chat_user'):
        chat_user = User.objects.get(id=request.GET.get('chat_user'))
        messages = Message.objects.filter(sender=request.user, receiver=chat_user) | Message.objects.filter(sender=chat_user, receiver=request.user)
        messages = messages.order_by('timestamp')
    else:
        messages = []

    if chat_user:
        form.fields['receiver'].initial = chat_user

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'accounts/messages.html', {'form': form, 'messages': messages, 'users': users, 'chat_user': chat_user})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'accounts/send_message.html', {'form': form})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            updated_email = form.cleaned_data.get('email')
            request.user.email = updated_email
            request.user.save()
            form.save()
            django_messages.success(request, 'Perfil actualizado correctamente')
            return redirect('profile')
        else:
            django_messages.error(request, 'Hubo un error al actualizar el perfil')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/profile_update.html', {'form': form})


