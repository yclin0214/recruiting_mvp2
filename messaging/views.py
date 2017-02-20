import json
import unicodedata

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from models import Message

from twilio.rest import TwilioRestClient

MESSAGE = ["Thanks for using SmartHire. Please provide some information so we can help you find the ideal job. First, please provide your name and location.",
           "Great. Are you looking for full-time or part-time job? And in what industries?",
           "Thanks for the response. Can you also tell us your availability for work? (For example, Wednesday evening 7pm - 10pm, Sunday morning, etc.)",
           "One more question, what’s your current education level and your expected salary?",
           "Last one, how many years of work experience do you have and in what positions?",
           "Thanks for all your response. Once we find a good match for you, SmartHire will get back to you ASAP. Meanwhile, please feel free to provide us more information by texting to this number."]

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
    entry.message_count = entry.message_count + 1
    entry.save()
    print ("Successfully saved")
    return entry.message_count

def get_all_information():  
    all_entries = Message.objects.all()
    candidate_number = len(all_entries)
    candidate_dict = {}
    candidate_dict["Number of total candidates"] = candidate_number
    for entry in all_entries:
        candidate_dict[entry.phone_number] = entry.text_contents
    return json.dumps(candidate_dict)

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
        text_to_send = MESSAGE[0]
        create_entry(phone_number, text_content)
        send_SMS(phone_number, text_to_send)
    else:
        count = add_message(phone_number, text_content)
        if count < 7:
            text_to_send = MESSAGE[count]
            send_SMS(phone_number, text_to_send)
    return HttpResponse('Success')

def view_statistics(request):
    return HttpResponse(get_all_information())

