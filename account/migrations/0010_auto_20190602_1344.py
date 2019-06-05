# Generated by Django 2.1.7 on 2019-06-02 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_node_reg_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='reg_date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='node',
            old_name='activate_date',
            new_name='expired_date',
        ),
        migrations.RemoveField(
            model_name='node',
            name='user_parent',
        ),
        migrations.AddField(
            model_name='node',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='invited_children', to='account.Node'),
        ),
    ]
