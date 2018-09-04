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
    title = CHAT_ROOMS.get(room_name, None)
    if title:
        data = {'title': title, 'name': room_name}
        return render(request, template_name, data)
    return redirect('chats')
