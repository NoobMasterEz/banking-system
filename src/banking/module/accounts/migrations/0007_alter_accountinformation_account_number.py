# Generated by Django 4.1.3 on 2022-11-27 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_accountinformation_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinformation',
            name='account_number',
            field=models.CharField(default='H638BEE1F7205', max_length=15, unique=True),
        ),
    ]
