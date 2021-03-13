from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json

# Create your views here.
@csrf_exempt
def index(request):
    print(request)
    # if request.method == 'POST':
    # data = request.POST.get('note', "Hello")
    data = json.loads(request.body)
    print("--------------------------")
    print(data['note'])
    # else:
    #     data = {'note': "qwerty"}
    get_auth(data['note'])
    return HttpResponse("Success")


def get_auth(data):
    print("print auth")
    print(data)
    print(type(data))
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)

    # View all folders and file in your Google Drive
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in fileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))
        # Get the folder ID that you want
        if (file['title'] == "Hello.txt"):
            file.GetContentFile("Hello.txt")
            update = file.GetContentString() + "\n"+ data
            file.SetContentString(update)
            file.Upload()
            break
            # return HttpResponse('Updated file %s with mimeType %s' % (file['title'], file['mimeType']))
    file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    file1.SetContentString(data)  # Set content of the file from given string.
    file1.Upload()
    # return HttpResponse('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))


@csrf_exempt
def test(request):
    print("=============================")
    return render(request, 'notes/temp2.html')

