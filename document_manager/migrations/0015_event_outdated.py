# Generated by Django 4.0.4 on 2022-09-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0014_event_document_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='outdated',
            field=models.BooleanField(default=1, verbose_name='Активно'),
            preserve_default=False,
        ),
    ]