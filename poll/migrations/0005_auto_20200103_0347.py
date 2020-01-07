# Generated by Django 3.0.1 on 2020-01-03 03:47

from django.db import migrations, models
import poll.models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20200102_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='deadline',
            field=models.DateTimeField(default=poll.models.get_deadline),
        ),
        migrations.AddField(
            model_name='poll',
            name='is_deleted',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='poll',
            name='is_draft',
            field=models.NullBooleanField(default=True),
        ),
    ]
