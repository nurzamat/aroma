# Generated by Django 2.1.7 on 2019-05-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20190318_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='reg_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]