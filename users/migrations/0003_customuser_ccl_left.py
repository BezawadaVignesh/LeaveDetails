# Generated by Django 4.1.7 on 2023-03-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_sls_cls_ccls'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ccl_left',
            field=models.IntegerField(default=0, verbose_name='ccl_left'),
            preserve_default=False,
        ),
    ]
