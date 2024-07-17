from django.shortcuts import render
from chat.models import Chat, Message

# Create your views here.
def index(request):
    if request.method == 'POST':
        print("Received Data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST["textmessage"], chat=myChat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1) # Wir schauen von der Message auf das Chat Objekt mit der ID 1
    return render(request, 'chat/index.html', { 'messages' : chatMessages })