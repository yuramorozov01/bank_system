# Generated by Django 4.0.1 on 2022-02-08 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banksettings',
            name='settings_name',
            field=models.CharField(choices=[('bank.settings', 'bank.settings')], default='bank.settings', max_length=128, primary_key=True, serialize=False, verbose_name='Settings name'),
        ),
    ]
