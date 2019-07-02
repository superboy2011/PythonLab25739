from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from accounts.models import Note, Folder
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.middleware.csrf import get_token

# Create your views here.
# TODO: find a way to manage the reminder, check how we sent emails for starters


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        response = HttpResponse(json.dumps({'csrf status': 'active', 'csrfchip': get_token(request)}), status=200)
        return response
    else:
        json_data = json.loads(request.body)
        password_in = json_data['InPassword']
        username_in = json_data['InUsername']
        user = authenticate(request, username=username_in, password=password_in)
        if user is not None:
            login(request, user)
            response = HttpResponse('Login Successful. Welcome ' + user.first_name, status=200)
        else:
            response = HttpResponse('Login Failed. Invalid username or password.', status=401)
        return response


@require_POST
def logout(request):
    if request.user.is_authenticated:
        logout(request, request.user)
        response = HttpResponse('Login Successful', status=200)
    else:
        response = HttpResponse('You haven''t been logged in!!!', status=401)
    return response


@require_POST
def signup(request):
    if 'NEWUsername' not in request.json or 'NEWPassword' not in request.json or 'NEWEmail' not in request.json or 'NEWFirst_name' not in request.json or 'NEWLast_name' not in request.json:
        response = HttpResponse('Insufficient data for signup', status=400)
    elif User.objects.filter(username=request.json['NEWUsername']).exists():
        response = HttpResponse('Duplicate Username', status=409)
    elif User.objects.filter(email=request.json['NEWEmail']).exists():
        response = HttpResponse('Duplicate Email', status=409)
    else:
        user = User.objects.create_user(username=request.json['NEWUsername'], password=request.json['NEWPassword'],
                                        email=request.json['NEWEmail'], first_name=request.json['NEWFirst_name'],
                                        last_name=request.json['NEWLast_name'])
        user.save()
        response = HttpResponse('User successfully signed up!!!', status=200)
    return response


@require_POST
def add_note(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=request.json['folder_name']).exists():
        response = HttpResponse('No folder with said name', status=400)
    elif Note.objects.filter(name=request.json['name'], folder_name=request.get['folder_name'],
                             user=request.user).exists():
        response = HttpResponse('Another note with the same name in the same folder exists already', status=409)
    else:
        note = Note.objects.create(name=request.json['name'], folder_name=request.json['folder_name'],
                                   data=request.json['data'])
        note.user = request.user
        note.y_m = int(request.json['y_m'])
        note.m_m = int(request.json['m_m'])
        note.d_m = int(request.json['d_m'])
        note.h_m = int(request.json['h_m'])
        note.min_m = int(request.json['min_m'])
        note.s_m = int(request.json['s_m'])
        if 'y_r' in request.json:
            note.y_r = int(request.json['y_r'])
            note.m_r = int(request.json['m_r'])
            note.d_r = int(request.json['d_r'])
            note.h_r = int(request.json['h_r'])
            note.min_r = int(request.json['min_r'])
            note.s_r = int(request.json['s_r'])
        else:
            note.y_r = 0
            note.m_r = 0
            note.d_r = 0
            note.h_r = 0
            note.min_r = 0
            note.s_r = 0
        note.save()
        folder = Folder.objects.filter(folder_name=note.folder_name)
        folder.list_notes = folder.list_notes + "," + note.name
        folder.save()
        response = HttpResponse('Note saved successfully', status=200)
    return response


@require_GET
def get_note(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Note.objects.filter(name=request.json['name'], folder_name=request.get['folder_name'],
                                 user=request.user).exists():
        response = HttpResponse('The requested note does not exist', status=404)
    else:
        note = Note.objects.filter(name=request.json['name'], folder_name=request.json['folder_name'],
                                   user=request.user)
        response = HttpResponse(json.dumps(model_to_dict(note)), status=200)
    return response


@require_POST
def update_note(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Note.objects.filter(name=request.json['name'], folder_name=request.get['folder_name'],
                                 user=request.user).exists():
        response = HttpResponse('The note to be updated does not exist', status=409)
    else:
        note = Note.objects.filter(name=request.json['name'], folder_name=request.json['folder_name'],
                                   user=request.user)
        if 'new_name' in request.json['data']:
            note.name = request.json['new_name']
            folder = Folder.objects.filter(folder_name=note.folder_name)
            listed_note_names = folder.list_notes.split(',')
            listed_note_names = [request.json['new_name'] if note_name == request.json['name'] else note_name for
                                 note_name in listed_note_names]
            folder.list_notes = ','.join(map(str, listed_note_names))
            folder.save()
        if 'data' in request.json:
            note.json = request.json['data']
        if 'y_m' in request.json:
            note.y_m = int(request.json['y_m'])
            note.m_m = int(request.json['m_m'])
            note.d_m = int(request.json['d_m'])
            note.h_m = int(request.json['h_m'])
            note.min_m = int(request.json['min_m'])
            note.s_m = int(request.json['s_m'])
        if 'y_r' in request.json:
            note.y_r = int(request.json['y_r'])
            note.m_r = int(request.json['m_r'])
            note.d_r = int(request.json['d_r'])
            note.h_r = int(request.json['h_r'])
            note.min_r = int(request.json['min_r'])
            note.s_r = int(request.json['s_r'])
        note.save()
        response = HttpResponse('Note updated successfully', status=200)
    return response


@require_POST
def delete_note(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Note.objects.filter(name=request.json['name'], folder_name=request.get['folder_name'],
                                 user=request.user).exists():
        response = HttpResponse('The note to be deleted does not exist', status=409)
    else:
        Note.objects.filter(name=request.json['name'], folder_name=request.json['folder_name'],
                            user=request.user).delete()
        folder = Folder.objects.filter(name=request.json['folder_name'])
        listed_note_names = folder.list_notes.split(',')
        listed_note_names.remove(request.json['name'])
        folder.list_notes = ','.join(map(str, listed_note_names))
        folder.save()
        response = HttpResponse('Note deleted successfully', status=200)
    return response


@require_POST
def add_folder(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif Folder.objects.filter(name=request.json['name']).exists():
        response = HttpResponse('Duplicate folder name', status=400)
    else:
        folder = Folder.objects.create(name=request.json['name'], list='')
        folder.save()
        response = HttpResponse('Folder created successfully', status=200)
    return response


@require_GET
def get_folder_list(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    else:
        folder_set = Folder.objects.all().values_list('name')
        response = HttpResponse(json.dumps(folder_set), status=200)
    return response


@require_GET
def get_folder_content(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=request.json['name'], user=request.user).exists():
        response = HttpResponse('Requested folder does not exist')
    else:
        folder_note_list = Folder.objects.filter(name=request.json['name'], user=request.user)
        response = HttpResponse(json.dumps(folder_note_list.list_notes), status=200)
    return response


@require_POST
def delete_folder(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=request.json['name'], user=request.user).exists():
        response = HttpResponse('Said folder does not exist')
    else:
        Folder.objects.filter(name=request.json['name'], user=request.user).delete()
        Note.objects.filter(folder_name=request.json['name'], user=request.user)
        response = HttpResponse('Successfully deleted the folder and its notes', status=200)
    return response
