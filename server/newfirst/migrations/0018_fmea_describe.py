# Generated by Django 3.1.1 on 2020-10-31 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newfirst', '0017_rules_belong'),
    ]

    operations = [
        migrations.AddField(
            model_name='fmea',
            name='describe',
            field=models.TextField(blank=True, default=''),
        ),
    ]
