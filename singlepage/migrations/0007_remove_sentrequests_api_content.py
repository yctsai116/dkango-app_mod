# Generated by Django 3.2.5 on 2021-07-29 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0006_sentrequests_api_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentrequests',
            name='api_content',
        ),
    ]
