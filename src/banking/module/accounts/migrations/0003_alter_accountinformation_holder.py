# Generated by Django 4.1.3 on 2022-11-27 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customer_user'),
        ('accounts', '0002_alter_accountinformation_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountinformation',
            name='holder',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customer'),
        ),
    ]
