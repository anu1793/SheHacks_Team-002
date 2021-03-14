from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import nltk
from textblob import TextBlob 
from nltk.corpus import wordnet 
from googletrans import Translator
import json
from google_trans_new import google_translator
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import nltk
import re
import csv
import matplotlib.pyplot as plt
from tqdm import tqdm
from social_django.models import UserSocialAuth
# %matplotlib inline
# pd.set_option('display.max_colwidth', 300)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score, accuracy_score
import joblib
import datetime
from notes.models import WordStreak,SentHighlight
from allauth.account.models import EmailAddress
from django.utils import timezone
from datetime import date
data = []
nltk.download('wordnet')
nltk.download('stopwords')
# with open("booksummaries.txt", 'r') as f:
#     reader = csv.reader(f, dialect='excel-tab')
#     for row in tqdm(reader):
#         data.append(row)
# book_id = []
# book_name = []
# summary = []
# genre = []

# for i in tqdm(data):
#     book_id.append(i[0])
#     book_name.append(i[2])
#     genre.append(i[5])
#     summary.append(i[6])

# books = pd.DataFrame({'book_id': book_id, 'book_name': book_name,
#                        'genre': genre, 'summary': summary})
# books.head(2)

# books.drop(books[books['genre']==''].index, inplace=True)
# books[books['genre']=='']

# import nltk
# nltk.download('stopwords')

# json.loads(books['genre'][0]).values()

# genres = []
# for i in books['genre']:
#   genres.append(list(json.loads(i).values()))
# books['genre_new'] = genres

# all_genres = sum(genres,[])
# len(set(all_genres))

# def clean_summary(text):
#     text = re.sub("\'", "", text)
#     text = re.sub("[^a-zA-Z]"," ",text)
#     text = ' '.join(text.split())
#     text = text.lower()
#     return text

# books['clean_summary'] = books['summary'].apply(lambda x: clean_summary(x))
# books.head(2)

# from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))
# def remove_stopwords(text):
#     no_stopword_text = [w for w in text.split() if not w in stop_words]
#     return ' '.join(no_stopword_text)

# books['clean_summary'] = books['clean_summary'].apply(lambda x: remove_stopwords(x))

# multilabel_binarizer = MultiLabelBinarizer()
# multilabel_binarizer.fit(books['genre_new'])

# y = multilabel_binarizer.transform(books['genre_new'])

# x_train, x_val, ytrain, yval = train_test_split(books['clean_summary'],
#                                               y, test_size=0.2)
mb=joblib.load('mb.pkl') 



word_list = []
def clean_summary(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^a-zA-Z]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

tfidf = joblib.load('tfidf.pkl') 
clf = joblib.load('recc.pkl')
def predict(m):
    print(m)
    m = clean_summary(m)
    m = remove_stopwords(m)
    m_vec = tfidf.transform([m])
    m_pred = clf.predict(m_vec)
    return mb.inverse_transform(m_pred)


# gauth = GoogleAuth()
# gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
# drive = GoogleDrive(gauth)
# fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# for file in fileList:
#   print('Title: %s, ID: %s' % (file['title'], file['id']))
#   # Get the folder ID that you want
#   if(file['title'] == "To Share"):
#       fileID = file['id']

# file1 = drive.CreateFile({"mimeType": "text/csv", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
# file1.SetContentFile("small_file.csv")
# file1.Upload() # Upload the file.
# print('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))   
def get_auth(data):
    print("print auth")
    print(data)
    print(type(data))
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)

    # View all folders and file in your Google Drive
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    flag = 0
    for file in fileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))
        # Get the folder ID that you want
        if (file['title'] == "Hello.txt"):
            file.GetContentFile("Hello.txt")
            update = file.GetContentString() + "\n"+ data
            file.SetContentString(update)
            file.Upload()
            flag = 1
            break
    if flag == 0:
    # return HttpResponse('Updated file %s with mimeType %s' % (file['title'], file['mimeType']))
        file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        file1.SetContentString(data)  # Set content of the file from given string.
        file1.Upload()
    





def translate_word_text(text):
    print(text)
    blob = TextBlob(text)
    result = {}
    print(blob)
    if (blob.detect_language() != 'en'):
        result["src"] = blob.detect_language()
        result["word"] = blob.translate(to='en')
        print(result)
    else:
        result["src"] = 'en'
        result["word"] = text
        

    #detect the language
   # lang = TextBlob(text)
    #detected_language = lang.detect_language()
#   translate it to english

    # print(result.src)
    # print(result.dest)
    # print(result.origin)
    # print(result.text)
    # print(result.pronunciation)
    return result


def summary_report():
    count = WordStreak.objects.filter(username='temp123')
    print(count)
    sentences = SentHighlight.objects.values_list('sentence',flat=True).distinct()
    print(type(sentences))
    print(sentences)
    pred_sent=' '
    for sen in sentences:
        pred_sent = pred_sent + sen 
    pred = predict(pred_sent)
    print(type(pred))
    print(pred)
    result = {}
    result['count'] = len(count)
    result['rec'] = pred
    return result




    


# @ensure_csrf_cookie
@csrf_exempt
def index(request):
    try:
        
        data = json.loads(request.body) 
        print(data['word'])
        

        if (len(data['word'].split(' '))>1) :
            print('its a sentence')
            sentence = SentHighlight.objects.create(username='temp123', sentence=data['word'], date=date.today())
            sentence.save()
            # get_auth(data['word'])
            response_data={}
            response_data['def'] = 'sentence'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else :
            if request.user:
                print("Finally")
                print(request.user)
            
            
            print(request.session.keys())
            result = translate_word_text(data['word'])
            syns = wordnet.synsets(result["word"])
            definition = syns[0].definition()
            usage = syns[0].examples()
            print(definition)
            send_text = "Definition: " + definition
            response_data = {}
            response_data['success'] = 'Create word successful!'
            response_data['def'] = send_text
            if data['word'] not in word_list:
                word_list.append(data['word'])

                # print(request.resource_owner)
                # if request.user.authenticated:
                #     print(request.user.username)
                if WordStreak.objects.filter(username='temp123').count()==0:

                    word = WordStreak.objects.create(username='temp123',count=1, language=result['src'], date=date.today())
                    word.save()
                else :
                    count = WordStreak.objects.filter(username='temp123').count()
                    word = WordStreak.objects.create(username='temp123',count=count+1, language=result['src'], date=date.today())
                    word.save()

            response_data["summary"] = summary_report()
            # response_data['dest']=result.dest
            response_data['src'] = result["src"]
            return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
       
    except Exception as ex:
        print(ex)
        return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )


