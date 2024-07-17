from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default = date.today)
    # chat 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    # ForeignKey -> auf ein anderes Objekt referenzieren
    # on_delete=models.CASCADE -> Nachricht wird mit dem Nutzer gelöscht
    # related_name='author_message_set' -> Damit die Datenbank weiß, das es sich um das Feld author innerhalb der Message handelt
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')
