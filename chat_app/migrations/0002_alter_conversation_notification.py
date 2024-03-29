# Generated by Django 5.0.1 on 2024-01-29 21:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0001_initial'),
        migrations.swappable_dependency(settings.NOTIFICATIONS_NOTIFICATION_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.NOTIFICATIONS_NOTIFICATION_MODEL),
        ),
    ]
