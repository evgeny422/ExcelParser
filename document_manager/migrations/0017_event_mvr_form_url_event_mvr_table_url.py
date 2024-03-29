# Generated by Django 4.0.4 on 2023-03-14 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0016_event_current_alter_event_outdated_alter_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='mvr_form_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на форму (МВР)'),
        ),
        migrations.AddField(
            model_name='event',
            name='mvr_table_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на таблицу (МВР)'),
        ),
    ]
