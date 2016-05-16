from django                                 import forms
from django.forms.widgets                   import CheckboxSelectMultiple
from .models                                import E
from users.models                           import Person
from django.contrib.auth.models             import User

class EForm(forms.ModelForm):
    class Meta:
        model = E
        fields = ('e_date', 'detail_public', 'detail_private', 'notes', 'attendees')
    def __init__(self, *args, **kwargs):
        super(EForm, self).__init__(*args, **kwargs)
        self.fields["attendees"].widget = CheckboxSelectMultiple()
        self.fields["attendees"].queryset = Person.objects.order_by('username')

class E2Form(forms.ModelForm):
    class Meta:
        model = E
        fields = ('e_date', 'detail_public', 'detail_private')

'''

class EForm(forms.Form):
    e_date         = forms.CharField(max_length=20)
    detail_public  = forms.CharField(max_length=20)
    detail_private = forms.CharField(max_length=20)
    notes          = forms.CharField(max_length=20)
    attendees      = forms.CharField(max_length=20)
    def __init__(self, *args, **kwargs):
        super(EForm, self).__init__(*args, **kwargs)
        self.fields["attendees"].widget = CheckboxSelectMultiple()
        self.fields["attendees"].queryset = User.objects.order_by('username')

class DisplaynameForm(forms.Form):
    display_name = forms.CharField(max_length=20)
'''
