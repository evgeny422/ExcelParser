# Generated by Django 4.0.4 on 2022-05-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0003_document_action_plan_ratio_document_deadline_ratio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='action_plan_ratio',
            field=models.PositiveIntegerField(verbose_name='План действий'),
        ),
        migrations.AlterField(
            model_name='document',
            name='deadline_ratio',
            field=models.PositiveIntegerField(verbose_name='Дедлайн'),
        ),
        migrations.AlterField(
            model_name='document',
            name='status_ratio',
            field=models.PositiveIntegerField(verbose_name='Статус'),
        ),
    ]
