# Generated by Django 5.2 on 2025-05-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
