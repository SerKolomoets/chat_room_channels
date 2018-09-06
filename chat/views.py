import re
from django.shortcuts import render, redirect

CHAT_ROOMS = {
    'first': 'First Room',
    'second': 'Second Room',
    'third': 'Third Room'
}


def index(request, template_name='index.html'):
    data = {'chats': CHAT_ROOMS}
    return render(request, template_name, data)


def chat_room(request, room_name, template_name='room.html'):
    if not request.session.get('username', None):
        return redirect('set_username')
    title = CHAT_ROOMS.get(room_name, None)
    if title:
        data = {'title': title, 'name': room_name}
        return render(request, template_name, data)
    return redirect('chats')


def set_username(request, template_name='set_username.html'):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        pattern = re.compile('^[a-zA-Z0-9]{6,12}$')
        if pattern.match(username):
            request.session['username'] = username
            return redirect('chats')
        return redirect('set_username')
    return render(request, template_name)
