import zk
from zk.exception import ZKError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods as alowed

from .forms import ScanTerminal, SaveTerminal, EditTerminal, UserForm
from .models import Terminal, User, Attendance

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@alowed(['GET'])
@login_required
def index(request):
    return render(request, 'zkcluster/index.html')

@alowed(['GET'])
@login_required
def dashboard(request):
    return render(request, 'zkcluster/dashboard.html')

@alowed(['GET'])
@login_required
def terminal(request):
    terminals = Terminal.objects.all()
    data = {
        'terminals': terminals
    }
    return render(request, 'zkcluster/terminal.html', data)

@alowed(['POST'])
@login_required
def terminal_add(request):
    connected = request.GET.get('connected')
    if connected:
        form = SaveTerminal(request.POST or None, {'validate_name': True})
        if form.is_valid():
            try:
                form.save()
                return redirect('zkcluster:terminal')
            except ZKError as e:
                messages.add_message(request, messages.ERROR, str(e))
    else:
        form = SaveTerminal(request.POST or None)

    data = {
        'form': form
    }
    return render(request, 'zkcluster/terminal_add.html', data)

@alowed(['GET', 'POST'])
@login_required
def terminal_scan(request):
    form = ScanTerminal(request.POST or None)
    if request.POST and form.is_valid():
        ip = form.cleaned_data['ip']
        port = form.cleaned_data['port']
        password = form.cleaned_data['password']
        force_udp = form.cleaned_data['force_udp']

        terminal = Terminal(
            ip=ip,
            port=port,
            password=password,
            force_udp=force_udp
        )
        try:
            terminal.zk_connect()
            sn = terminal.zk_getserialnumber()

            # manipulate the POST information
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['serialnumber'] = sn
            request.POST._mutable = mutable

            terminal.zk_disconnect()
            return terminal_add(request)
        except ZKError as e:
            messages.add_message(request, messages.ERROR, str(e))

    data = {
        'form': form
    }

    return render(request, 'zkcluster/terminal_scan.html', data)

@alowed(['GET', 'POST'])
@login_required
def terminal_edit(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    form = EditTerminal(request.POST or None, instance=terminal)
    if request.POST and form.is_valid():
        try:
            form.save()
        except ZKError as e:
            messages.add_message(request, messages.ERROR, str(e))
        return redirect('zkcluster:terminal')
    data = {
        'terminal': terminal,
        'form': form
    }
    return render(request, 'zkcluster/terminal_edit.html', data)

@alowed(['POST'])
def terminal_format(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    try:
        terminal.format()
    except ZKError as e:
        messages.add_message(request, messages.ERROR, str(e))

    return redirect('zkcluster:terminal')

@alowed(['POST'])
def terminal_delete(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    try:
        terminal.delete()
    except ZKError as e:
        messages.add_message(request, messages.ERROR, str(e))

    return redirect('zkcluster:terminal')

@alowed(['POST'])
def terminal_restart(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    try:
        terminal.zk_connect()
        terminal.zk_restart()
    except ZKError as e:
        messages.add_message(request, messages.ERROR, str(e))

    return redirect('zkcluster:terminal')

@alowed(['POST'])
def terminal_poweroff(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    try:
        terminal.zk_connect()
        terminal.zk_poweroff()
        terminal.zk_disconnect()
    except ZKError as e:
        messages.add_message(request, messages.ERROR, str(e))

    return redirect('zkcluster:terminal')

@alowed(['POST'])
def terminal_voice(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    try:
        terminal.zk_connect()
        terminal.zk_voice()
        terminal.zk_disconnect()
    except ZKError as e:
        messages.add_message(request, messages.ERROR, str(e))

    return redirect('zkcluster:terminal')

@alowed(['GET', 'POST'])
@login_required
def terminal_action(request, action, terminal_id):
    if action == 'edit':
        return terminal_edit(request, terminal_id)
    elif action == 'restart':
        return terminal_restart(request, terminal_id)
    elif action == 'poweroff':
        return terminal_poweroff(request, terminal_id)
    elif action == 'voice':
        return terminal_voice(request, terminal_id)
    elif action == 'format':
        return terminal_format(request, terminal_id)
    elif action == 'delete':
        return terminal_delete(request, terminal_id)
    else:
        raise Http404("Action doest not allowed")

@alowed(['GET', 'POST'])
@login_required
def user(request):
    users = User.objects.all()
    data = {
        'users': users
    }
    return render(request, 'zkcluster/user.html', data)

@alowed(['GET', 'POST'])
@login_required
def user_add(request):
    form = UserForm(request.POST or None)
    if request.POST and form.is_valid():
        try:
            form.save()
            return redirect('zkcluster:user')
        except ZKError as e:
            messages.add_message(request, messages.ERROR, str(e))

    data = {
        'form': form
    }
    return render(request, 'zkcluster/user_add.html', data)

@alowed(['GET', 'POST'])
@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = UserForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        try:
            form.save()
            return redirect('zkcluster:user')
        except ZKError as e:
            messages.add_message(request, messages.ERROR, str(e))

    data = {
        'form': form
    }
    return render(request, 'zkcluster/user_edit.html', data)

@alowed(['POST'])
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        user.delete()
    except ZKError as e:
        messages.add_message(request, messages.ERROR, str(e))
    return redirect('zkcluster:user')

@alowed(['GET', 'POST'])
@login_required
def user_action(request, action, user_id):
    if action == 'edit':
        return user_edit(request, user_id)
    elif action == 'delete':
        return delete_user(request, user_id)
    else:
        raise Http404("Action doest not allowed")

@alowed(['GET', 'POST'])
@login_required
def attendance(request):
    attendances = Attendance.objects.all()
    data = {
        'attendances': attendances
    }
    return render(request, 'zkcluster/attendance.html', data)

@alowed(['GET'])
@login_required
def attendance_sync(request):
    terminals = Terminal.objects.all()
    for terminal in terminals:
        try:
            terminal.zk_connect()
            attendances = []
            for attendance in terminal.zk_get_attendances():
                try:
                    user = User.objects.get(pk=attendance.user_id)
                except User.DoesNotExist as e:
                    logger.warn("User not found")
                    continue
                Attendance.objects.create(
                    user=user,
                    timestamp=attendance.timestamp,
                    status=attendance.status
                )
            terminal.zk_clear_attendances()
            terminal.zk_voice()
            terminal.zk_disconnect()
        except ZKError as e:
            logger.warn("ZKError on get_attendance")
    return redirect('zkcluster:attendance')
