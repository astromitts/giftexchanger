from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

from giftexchanger.utils.assignments import ExchangeAssigner


class GiftExchange(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=600)
    spending_max = models.IntegerField(default=25)
    schedule_day = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'pending'),  # assignments have not been set, so new users can be added
            ('assigned', 'assigned'),  # assignments have been set, so no new users
            ('closed', 'closed'),  # exchange is over, so nothing new allowed
        ),
        default='pending'
    )

    @property
    def status_desc(self):
        status_map = {
            'pending': """
                This gift exchange is upcoming but assignments have not been set for this exchange. 
                You can still add new users and users can make suggestions for each other.
            """,
            'assigned': """
                This gift exchange is upcoming and assignments have been set. 
                You cannot add any more users but users can make suggestions for each other.
            """,
            'closed': """
                This gift exchange is closed, nothing can be changed.
            """,
        }
        return self._status_desc
    

    def generate_assignments(self, max_tries=6, debug=False):
        assigner = ExchangeAssigner(self)
        assigner.make_assignments(max_tries, debug)
        assignment_objects = []
        for giver_id, receiver_id in assigner.assignment_map.items():
            gift_assignment = GiftAssignment(
                exchange=self,
                giver_id=giver_id,
                receiver_id=receiver_id
            )
            gift_assignment.save()
            assignment_objects.append(gift_assignment)
        return assignment_objects

    @property
    def participants(self):
        return [uds.user for uds in self.userdetails_set.all().order_by('?')]

    def get_available_users(self):
        import pdb
        pdb.set_trace()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    admin_of = models.ManyToManyField(GiftExchange)

    @property
    def name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def user_prt_id(self):
        return self.user.pk

    def get_assignment(self, exchange):
        assignment_qs = GiftAssignment.objects.filter(giver=self, exchange=exchange)
        if assignment_qs.exists():
            return assignment_qs.first().receiver
        else:
            return None

    @classmethod
    def get_or_create(cls, email):
        user_q = User.objects.filter(email=email)
        if user_q.exists():
            created = False
            user = user_q.first()
        else:
            created = True
            user = User(
                email=email,
                username=email
            )
            user.save()
            user.set_password('ChangeMe!123')
            user.save()
        if cls.objects.filter(user=user).exists():
            return cls.objects.get(user=user), created
        else:
            new_cls = cls(
                user=user
            )
            new_cls.save()
            return new_cls, created

    def set_user_info(self, first_name, last_name):
        self.user.first_name = first_name
        self.user.last_name = last_name
        self.user.save()

    def set_details_for_exchange(self, exchange, likes, dislikes, allergies):
        exchange_detail_qs = self.userdetails_set.filter(exchange=exchange)
        if exchange_detail_qs.exists():
            exchange_detail_instance = exchange_detail_qs.first()
        else:
            exchange_detail_instance = UserDetails(user=self, exchange=exchange)
        exchange_detail_instance.likes = likes
        exchange_detail_instance.dislikes = dislikes
        exchange_detail_instance.allergies = allergies
        exchange_detail_instance.save()
        return exchange_detail_instance

    def get_exchanges(self):
        return [d.exchange for d in self.userdetails_set.all()]

    def __str__(self):
        if self.user.username:
            return '%s // %s' % (self.user.username, self.user.email)
        return '%s' % (self.user.email)


class UserDetails(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exchange = models.ForeignKey(GiftExchange, on_delete=models.CASCADE)
    likes = models.CharField(max_length=600, blank=True, null=True)
    dislikes = models.CharField(max_length=600, blank=True, null=True)
    allergies = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'exchange')

    def __str__(self):
        return '{}, {}'.format(self.user.name, self.exchange)


class GiftAssignment(models.Model):
    exchange = models.ForeignKey(GiftExchange, on_delete=models.CASCADE)
    giver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='giver')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')

    def get_receiver_details(self):
        return UserDetails.objects.get(exchange=self.exchange, user=self.receiver)

    class Meta:
        unique_together = (['exchange', 'giver'], ['exchange', 'giver', 'receiver'])


def user_post_signal(sender, instance, created, **kwargs):
    """ Handler for custom user creation logic - adds new user to the
        app_users group  and creates a new associated UserProfile instance
    """
    if created:
        public_users_group, created = Group.objects.get_or_create(name='app_users')
        instance.groups.add(public_users_group)
        user_profile = UserProfile(user=instance)
        user_profile.save()
    else:
        pass


post_save.connect(user_post_signal, sender=User)
