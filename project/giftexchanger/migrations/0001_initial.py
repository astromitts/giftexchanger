# Generated by Django 3.0 on 2019-12-05 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftExchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=600)),
                ('spending_max', models.IntegerField(default=25)),
                ('schedule_day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.CharField(blank=True, max_length=600, null=True)),
                ('dislikes', models.CharField(blank=True, max_length=600, null=True)),
                ('allergies', models.CharField(blank=True, max_length=600, null=True)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftexchanger.GiftExchange')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftexchanger.UserProfile')),
            ],
            options={
                'unique_together': {('user', 'exchange')},
            },
        ),
        migrations.CreateModel(
            name='GiftAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftexchanger.GiftExchange')),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='giver', to='giftexchanger.UserProfile')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='giftexchanger.UserProfile')),
            ],
            options={
                'unique_together': {('exchange', 'giver'), ('exchange', 'giver', 'receiver')},
            },
        ),
    ]
