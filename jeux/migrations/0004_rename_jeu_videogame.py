# Generated by Django 4.2.15 on 2024-10-18 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jeux', '0003_alter_tokenresetpassword_token'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Jeu',
            new_name='Videogame',
        ),
    ]