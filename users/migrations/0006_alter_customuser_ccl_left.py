# Generated by Django 4.1.7 on 2023-03-25 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_ccl_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ccl_left',
            field=models.IntegerField(blank=True, verbose_name='ccl_left'),
        ),
    ]