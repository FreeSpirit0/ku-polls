# Generated by Django 3.2.6 on 2021-09-07 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default='', verbose_name='end date'),
            preserve_default=False,
        ),
    ]
