# Generated by Django 3.1.1 on 2020-10-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newfirst', '0003_auto_20201023_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.TextField(default='')),
                ('content', models.TextField(default='')),
                ('type', models.TextField(default='')),
                ('name', models.TextField(default='', unique=True)),
                ('describe', models.TextField(default='')),
            ],
        ),
    ]
