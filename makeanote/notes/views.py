from django.shortcuts import render
from django.http import HttpResponse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Create your views here.
def index(request):
    get_auth("test123")
    return render(request, 'notes/temp2.html')

def get_auth(data):
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




def drive_auth(request):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)

    # View all folders and file in your Google Drive
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in fileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))
        # Get the folder ID that you want
        if (file['title'] == "To Share"):
            fileID = file['id']

    file1 = drive.CreateFile({"mimeType": "text/csv", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
    file1.SetContentFile("small_file.csv")
    file1.Upload()  # Upload the file.INSTALLED_APPS.

