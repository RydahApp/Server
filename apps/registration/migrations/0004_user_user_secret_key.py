# Generated by Django 5.0.4 on 2024-04-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_user_activation_key_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_secret_key',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
