from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from models import Message

import json

def concate_jsonify(json_string, new_string):
    if json_string is None:
        empty_list = []
        empty_list.append(new_string);
        json_string = empty_list;
        return json.dumps(json_string);
    array_unpacked = json.loads(json_string);
    jsonified_string = json.loads(json.dumps(new_string));
    array_unpacked.append(jsonified_string);
    new_array = array_unpacked;
    new_json_array = json.dumps(new_array);
    return new_json_array;

def create_entry(phone_number, text_content):
    text_content = concate_jsonify(None, text_content);
    new_entry= Message(phone_number=phone_number,acquired_date=timezone.now(), text_contents=text_content);
    new_entry.save();
    return

def check_number_exist(phone_number):
    try:
        entry = Message.objects.get(phone_number=phone_number)
    except entry.DoesNotExist:
        return False
    return True

def add_message(phone_number, text_content):
    entry = Message.objects.get(phone_number=phone_number)
    entry.text_contents = concate_jsonify(entry.text_contents, text_content);
    entry.save();
    return 

def get_all_text():    
    for entry in Message.objects:
        print entry.text_contents;
    return

def get_all_numbers():
    for entry in Message.objects:
        print entry.phone_number;
    return

#Twilio helper functions defined below
def send_SMS(phone_number):
    return
    
def receive_SMS(request):
    return


