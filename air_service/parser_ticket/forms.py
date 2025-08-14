from django import forms
from .models import Ticket

class TicketUploadForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['uploaded_file']