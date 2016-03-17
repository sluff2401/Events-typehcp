from django                                 import forms
from django.forms.widgets                   import CheckboxSelectMultiple
from .models                                import E
from django.contrib.auth.models             import User
class EForm(forms.ModelForm):
    class Meta:
        model = E
        fields = ('e_date', 'detail_public', 'detail_private', 'notes', 'attendees')
    def __init__(self, *args, **kwargs):
        super(EForm, self).__init__(*args, **kwargs)
        self.fields["attendees"].widget = CheckboxSelectMultiple()
        self.fields["attendees"].queryset = User.objects.order_by('username')
