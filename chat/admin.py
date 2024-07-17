from django.contrib import admin
from chat.models import Message, Chat

# Gib an was im Admin Panel angezeigt wird.
# z.B. nicht alle Felder für alle Admins anzeigen
# evtl. Zusatzfelder einbauen (Suche nach Nutzern)
# Filter einstellen
class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'text', 'created_at', 'author', 'receiver')       # Felder für die Detailansicht (zum bearbeiten)
    list_display = ('text', 'created_at', 'author', 'receiver') # Elemente die in der Listenansicht angezeigt werden
    search_fields = ('text',)                                   # Erstellt Suchleiste für die Messages

# Register your models here.
admin.site.register(Message, MessageAdmin) # Das Model wird registriert und dem Admin Panel hinzugefügt.
admin.site.register(Chat)