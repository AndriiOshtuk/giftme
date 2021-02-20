from django import forms


class GiftBookedForm(forms.Form):
    is_booked = forms.BooleanField(required=False)
