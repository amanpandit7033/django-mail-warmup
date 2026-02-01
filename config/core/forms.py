from django import forms
from .models import SenderMail
from .models import RecipientMail
from .models import SubjectLine
from .models import MailBody

class SenderMailForm(forms.ModelForm):
    class Meta:
        model = SenderMail
        fields = ['email', 'app_password', 'status']


class RecipientMailForm(forms.ModelForm):
    class Meta:
        model = RecipientMail
        fields = ['email', 'status']


class SubjectLineForm(forms.ModelForm):
    class Meta:
        model = SubjectLine
        fields = ['subject', 'status']


class MailBodyForm(forms.ModelForm):
    class Meta:
        model = MailBody
        fields = ['body', 'status']

class CSVUploadForm(forms.Form):
    file = forms.FileField()