from django.shortcuts import render


def render_index(request):
    return render(request, 'Chat/index.html')


def render_chat_room(request, **kwargs):
    return render(request, 'Chat/chat.html', {"name": kwargs["name"]})
