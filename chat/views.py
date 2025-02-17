from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from chat.models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    """
    render chat / handle POST requests for messages
    """
    if request.method == 'POST':
        myChat,created = Chat.objects.get_or_create(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message,])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1) # Wir schauen von der Message auf das Chat Objekt mit der ID 1
    return render(request, 'chat/index.html', { 'messages' : chatMessages })


def login_view(request):
    """
    render login / handle POST requests for login
    """
    redirect = request.GET.get('next') or '/chat/'
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            destination = request.POST.get('redirect') or '/chat/'
            return HttpResponseRedirect(destination)
        else:
            return render(request, 'auth/login.html', { 'wrongPassword' : True, 'redirect' : redirect })
    return render(request, 'auth/login.html', { 'redirect' : redirect })


def signup_view(request):
    """
    render signup / handle POST request for signup
    """
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/signup.html', { 'emailExists' : True })
        elif (password != conf_password):
            return render(request, 'auth/signup.html', { 'passwordsDontMatch' : True })
        else:
            user = User.objects.create_user(name,email,password)
            user.first_name = name
            user.save()
            return HttpResponseRedirect('/login/')
    return render(request, 'auth/signup.html') 


def logout_view(request):
    """
    logout user / redirect to login
    """
    logout(request)
    return redirect('/login')