from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import nltk
from textblob import TextBlob 
from nltk.corpus import wordnet 
from googletrans import Translator
import json
from google_trans_new import google_translator

def translate_word_text(text):
    print(text)
    blob = TextBlob(text)
    result = {}
    print(blob)
    if (blob.detect_language() != 'en'):
        result["src"] = blob.detect_language()
        result["word"] = blob.translate(to='en')
        print(result)
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



    


# @ensure_csrf_cookie
@csrf_exempt
def index(request):
    try:
        data = json.loads(request.body) 
        print(data['word'])
        nltk.download('wordnet')
        result = translate_word_text(data['word'])
        syns = wordnet.synsets(result["word"])
        definition = syns[0].definition()
        usage = syns[0].examples()
        print(definition)
        send_text = "Definition: " + definition
        response_data = {}
        response_data['success'] = 'Create word successful!'
        response_data['def'] = send_text
        
        # response_data['dest']=result.dest
        response_data['src'] = result["src"]
        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        # if request.method == 'POST' and request.headers.get({"contentType": "application/json"}):
        #     body_unicode = request.body.decode('utf-8')
        #     received_json = json.loads(body_unicode)
        #     print(received_json)
        #     response_data = {}
        #     nltk.download('wordnet')
        #     print("post_text" + post_text)
        #     syns = wordnet.synsets(post_text)
        #     definition = syns[0].definition()
        #     usage = syns[0].examples()
        #     print(syns[0].definition())
        #     print(syns[0].examples())
        #     send_text = "Definition: " + definition


        #     # post = Post(text=post_text, author=request.user)
        #     # post.save()

        #     response_data['success'] = 'Create word successful!'
        #     response_data['def'] = send_text
            
        #     return HttpResponse(
        #         json.dumps(response_data),
        #         content_type="application/json"
        #     )
        # else:
        #     return HttpResponse(
        #         json.dumps({"nothing to see": "this isn't happening"}),
        #         content_type="application/json"
        #     )
        
        
        
        
        
        
        
        # data_from_post = json.load(request)['post_data'] #Get data from POST request
        # #Do something with the data from the POST request
        # #If sending data back to the view, create the data dictionary
        # data = {
        #     'my_data':data_to_display,
        # }
        # return HttpResponse("Hello, world. You're at the polls index.")
    except Exception as ex:
        print(ex)
        return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )