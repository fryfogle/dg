from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


class UserPaymentForm(forms.Form):
    from_date = forms.DateField(initial=datetime.date.today)
    to_date = forms.DateField(initial=datetime.date.today)

    '''
    def clean_from_date(self):
        date = self.cleaned_data
        from_date = date.get('from_date')
        to_date = date.get('to_date')
        if from_date > to_date:
            raise forms.ValidationError("From date should be less than or equal to To date")
        return from_date
    '''
