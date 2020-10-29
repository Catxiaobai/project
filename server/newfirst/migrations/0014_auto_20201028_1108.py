# Generated by Django 3.1.1 on 2020-10-28 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newfirst', '0013_auto_20201025_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='item_content',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='item_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='item_introduction',
            new_name='path',
        ),
        migrations.AddField(
            model_name='item',
            name='software',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='item',
            name='team',
            field=models.TextField(default=''),
        ),
    ]
