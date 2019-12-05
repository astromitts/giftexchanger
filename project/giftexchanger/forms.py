from django.forms import (
    ModelForm,
    CharField,
    HiddenInput
)
from giftexchanger.models import UserDetails


class EditUserDetailsForExchange(ModelForm):
    likes = CharField(required=False)
    dislikes = CharField(required=False)
    allergies = CharField(required=False)
    exchange = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = UserDetails
        fields = [
            'likes',
            'dislikes',
            'allergies',
            'exchange',
        ]
