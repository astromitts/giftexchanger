from django.test import TestCase
from giftexchanger.models.app import GiftExchange, UserProfile
from datetime import date, timedelta


class GiftExchangeTestCase(TestCase):

    def setUp(self):
        expired_date = date.today() - timedelta(3)
        expired_exchange = GiftExchange(
            title='Expired gift exchange',
            description='This is a gift exchange that already happened',
            schedule_day=expired_date,
            spending_max=25
        )
        expired_exchange.save()
        self.expired_exchange = expired_exchange

        upcoming_date = date.today() + timedelta(3)
        upcoming_exchange_main = GiftExchange(
            title='Upcoming gift exchange',
            description='This is a gift exchange that will happen soon',
            schedule_day=upcoming_date,
            spending_max=35
        )
        upcoming_exchange_main.save()
        self.upcoming_exchange_main = upcoming_exchange_main

        upcoming_exchange_secondary = GiftExchange(
            title='Other upcoming gift exchange',
            description='This is a different gift exchange that will happen soon',
            schedule_day=upcoming_date,
            spending_max=35
        )
        upcoming_exchange_secondary.save()
        self.upcoming_exchange_secondary = upcoming_exchange_secondary

        test_users = [
            {
                'first_name': 'Bob',
                'last_name': 'Belcher',
                'email': 'bob@wonderwharf.com',
                'likes': 'Cooking gadgets, westerns',
                'dislikes': 'Italian food',
                'allergies': 'Shellfish',
            },
            {
                'first_name': 'Linda',
                'last_name': 'Belcher',
                'email': 'lindaxoxox@yahoo.com',
                'likes': 'Porcelain babies, romance',
                'dislikes': None,
                'allergies': None,
            },
            {
                'first_name': 'Jimmy',
                'last_name': 'Pesto',
                'email': 'jimmy@wonderwharf.com',
                'likes': 'Karaoke, succulents',
                'dislikes': 'Bob',
                'allergies': None,
            },
            {
                'first_name': 'Teddy',
                'last_name': '???',
                'email': 'teddy@wonderwharf.com',
                'likes': None,
                'dislikes': 'Dancing',
                'allergies': None,
            },
            {
                'first_name': 'Calvin',
                'last_name': 'Fischoeder',
                'email': 'mrf@wonderwharf.com',
                'likes': 'Money, golf carts, luxury',
                'dislikes': 'Sunglasses, glasses',
                'allergies': 'Penecilin',
            },
            {
                'first_name': 'Tina',
                'last_name': 'Belcher',
                'email': 'tbelcher@wagstaffmiddleschool.edu',
                'likes': 'Boys, horses, zombies',
                'dislikes': None,
                'allergies': None,
            },
            {
                'first_name': 'Gene',
                'last_name': 'Belcher',
                'email': 'gbelcher@wagstaffmiddleschool.edu',
                'likes': 'Music, noisemakers, dark and light chocolate, game of thrones',
                'dislikes': 'Snakes',
                'allergies': 'Shellfish',
            },
            {
                'first_name': 'Louis',
                'last_name': 'Belcher',
                'email': 'lbelcher@wagstaffmiddleschool.edu',
                'likes': None,
                'dislikes': None,
                'allergies': None,
            },

        ]

        self.test_users = []
        for row in test_users:
            test_user_profile, created = UserProfile.get_or_create(row['email'])
            test_user_profile.set_user_info(
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            test_user_profile.set_details_for_exchange(
                exchange=self.expired_exchange,
                likes=row['likes'],
                dislikes=row['dislikes'],
                allergies=row['allergies']
            )
            test_user_profile.set_details_for_exchange(
                exchange=self.upcoming_exchange_main,
                likes=row['likes'],
                dislikes=row['dislikes'],
                allergies=row['allergies']
            )
            self.test_users.append(test_user_profile)
