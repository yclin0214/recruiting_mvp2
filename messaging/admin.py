from django.contrib import admin
from .models import Message

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    fields = ['phone_number', 'text_contents', 'acquired_date']

admin.site.register(Message, MessageAdmin)
