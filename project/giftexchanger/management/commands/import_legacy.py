import csv
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from giftexchanger.models import UserProfile, GiftAssignment, GiftExchange


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('exchange_id', type=int)

    def _get_user_profile_by_name(self, name):
        first_name = name.split(' ')[0]
        last_name = name.split(' ')[1]
        user = User.objects.get(first_name=first_name, last_name=last_name)
        profile = UserProfile.objects.get(user=user)
        return profile

    def handle(self, *args, **options):
        new_count = 0
        updated_count = 0
        file = options['file']
        exchange_id = options['exchange_id']

        exchange = GiftExchange.objects.get(pk=exchange_id)

        if 'responses' in file:
            with open(file, 'r') as filehandle:
                reader = csv.DictReader(filehandle)
                for row in reader:
                    user_profile, created = UserProfile.get_or_create(row['email'])

                    if created:
                        new_count += 1
                    else:
                        updated_count += 1

                    user_profile.set_user_info(
                        first_name=row['name'].split(' ')[0],
                        last_name=row['name'].split(' ')[1],
                    )
                    user_profile.set_details_for_exchange(
                        exchange=exchange,
                        likes=row['likes'],
                        dislikes=row['allergies/dislikes'],
                        allergies=row['allergies/dislikes']
                    )
            self.stdout.write(
                self.style.SUCCESS('Created {} new users'.format(new_count))
            )
            self.stdout.write(
                self.style.SUCCESS('Updated {} existing users'.format(updated_count))
            )

        elif 'assignments' in file:
            with open(file, 'r') as filehandle:
                reader = csv.DictReader(filehandle)
                for row in reader:
                    user_profile_giver = self._get_user_profile_by_name(row['giver'])
                    user_profile_receiver = self._get_user_profile_by_name(row['recipient'])
                    assg = GiftAssignment(
                        exchange=exchange,
                        giver=user_profile_giver,
                        receiver=user_profile_receiver
                    )
                    assg.save()

        else:
            self.stdout.write(self.style.ERROR('Unrecognized input file type'))
