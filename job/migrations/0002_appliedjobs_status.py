# Generated by Django 2.1.5 on 2019-03-31 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedjobs',
            name='status',
            field=models.BooleanField(blank='True', default='False'),
        ),
    ]