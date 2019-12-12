from django.forms import (
    ModelForm,
    CharField,
    IntegerField,
    DateField,
    HiddenInput
)
from giftexchanger.models.app import UserDetails, GiftExchange


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


class AdminEditExchangeInfo(ModelForm):
    title = CharField(required=True)
    description = CharField(required=True)
    spending_max = IntegerField(required=True)
    exchange = CharField(widget=HiddenInput(), required=False)
    schedule_day = DateField(required=True)

    class Meta:
        model = GiftExchange
        fields = [
            'title',
            'description',
            'spending_max',
            'schedule_day',
            'exchange'
        ]
