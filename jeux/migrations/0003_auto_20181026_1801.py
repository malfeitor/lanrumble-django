# Generated by Django 2.1.2 on 2018-10-26 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jeux', '0002_auto_20181026_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joueur',
            old_name='list_jeux',
            new_name='liste_jeux',
        ),
    ]
