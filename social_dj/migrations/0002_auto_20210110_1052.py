# Generated by Django 3.1.4 on 2021-01-10 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_dj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateField(auto_now=True)),
                ('signed_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signed', to=settings.AUTH_USER_MODEL)),
                ('subscriber_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscribes',
            field=models.ManyToManyField(related_name='_userprofile_subscribes_+', through='social_dj.Follow', to='social_dj.UserProfile'),
        ),
    ]