# Generated by Django 2.0.2 on 2018-04-12 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180412_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='flag',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='usertype',
            field=models.CharField(default='', max_length=100),
        ),
    ]
