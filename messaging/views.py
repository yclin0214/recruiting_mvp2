import json
import unicodedata

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from models import Message

from twilio.rest import TwilioRestClient

def concate_jsonify(json_string, new_string):
    if json_string is None:
        empty_list = []
        empty_list.append(new_string)
        json_string = empty_list
        return json.dumps(json_string)
    array_unpacked = json.loads(json_string)
    jsonified_string = json.loads(json.dumps(new_string))
    array_unpacked.append(jsonified_string)
    new_array = array_unpacked
    new_json_array = json.dumps(new_array)
    return new_json_array

def create_entry(phone_number, text_content):
    text_content = concate_jsonify(None, text_content);
    new_entry = Message(phone_number=phone_number,acquired_date=timezone.now(),
        text_contents=text_content, last_update=timezone.now())
    new_entry.save()
    return

def check_number_exist(phone_number):
    try:
        entry = Message.objects.get(phone_number=phone_number)
    except ObjectDoesNotExist:
        return False
    return True

def add_message(phone_number, text_content):
    entry = Message.objects.get(phone_number=phone_number)
    entry.text_contents = concate_jsonify(entry.text_contents, text_content)
    entry.save()
    print ("Successfully saved")
    return 

def get_all_text():    
    for entry in Message.objects:
        print entry.text_contents
    return

def get_all_numbers():
    for entry in Message.objects:
        print entry.phone_number
    return

#Twilio helper functions defined below
def send_SMS(phone_number, text_content):
    from django.conf import settings
    account_sid = settings.GLOBAL_VAR['ACCOUNT_SID']
    auth_token = settings.GLOBAL_VAR['AUTH_TOKEN']
    twilio_number = settings.GLOBAL_VAR['TWILIO_NUMBER']
    client = TwilioRestClient(account_sid, auth_token)
    #choose body text
    try:
        message = client.messages.create(to=phone_number, from_=twilio_number, body=text_content)
    except TwilioRestException as e:
        print (e)
    return

def receive_SMS(request):
    data = request.GET
    phone_number = unicodedata.normalize('NFKD', data['From']).encode('ascii', 'ignore')
    if len(phone_number) > 10:
        phone_number = phone_number[len(phone_number)-10 : len(phone_number)]
    text_content = unicodedata.normalize('NFKD', data['Body']).encode('ascii', 'ignore')
    #Debugging message
    print ("phone number is " + phone_number)
    print ("Text message is " + text_content)
    #Database query
    exist = check_number_exist(phone_number)
    print ("exist: " + str(exist))
    if exist is not True:
        create_entry(phone_number, text_content)
    else:
        add_message(phone_number, text_content)
    send_SMS(phone_number, "I have received your info")

    return HttpResponse('Success')


