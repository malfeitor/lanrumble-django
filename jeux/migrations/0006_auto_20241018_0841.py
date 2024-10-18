# Generated by Django 4.2.15 on 2024-10-18 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jeux", "0005_rename_jeu_societe_boardgame_rename_joueur_player_and_more"),
    ]

    operations = [
        migrations.RenameField("Videogame", "nom", "title"),
        migrations.RenameField(
            "Videogame", "joueurs_max_hot_seat", "max_hot_seat_players"
        ),
        migrations.RenameField("Videogame", "joueurs_max_online", "max_online_players"),
        migrations.RenameField("Player", "amis", "friends"),
        migrations.RenameField("Player", "liste_jeux", "videogames_list"),
        migrations.RenameField("Boardgame", "nom", "title"),
        migrations.RenameField("Boardgame", "temps_prevu", "game_time"),
        migrations.RenameField("Boardgame", "joueurs_max", "max_players"),
        migrations.RenameField("Boardgame", "joueurs_min", "min_players"),
        migrations.RenameField("Boardgame", "complexite", "difficulty"),
        migrations.RenameField("Boardgame", "possede_par", "owned_by"),
        migrations.RenameField("VideogameRating", "valeur", "rating"),
        migrations.RenameField("VideogameRating", "jeu_concerne", "videogame"),
        migrations.RenameField("VideogameRating", "joueur_concerne", "player"),
    ]
