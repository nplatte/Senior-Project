# Generated by Django 2.2.2 on 2019-07-30 00:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0007_handout'),
    ]

    operations = [
        migrations.AddField(
            model_name='handout',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
