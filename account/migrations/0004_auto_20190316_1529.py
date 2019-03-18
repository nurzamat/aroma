# Generated by Django 2.1.7 on 2019-03-16 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_bonus'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('level', models.IntegerField(default=0)),
                ('left', models.IntegerField(default=0)),
                ('right', models.IntegerField(default=0)),
                ('diff', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('bonus_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.BonusType')),
            ],
        ),
        migrations.RenameField(
            model_name='bonus',
            old_name='price_som',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='status',
        ),
        migrations.AddField(
            model_name='bonus',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bonus_partner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='node',
            name='activate_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='cycle',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='step',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='created_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='type',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bonus_user', to=settings.AUTH_USER_MODEL),
        ),
    ]