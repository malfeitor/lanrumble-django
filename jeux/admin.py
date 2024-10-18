from django.contrib import admin
from .models import Videogame, Player, Boardgame, VideogameRating, TokenResetPassword


class VideogameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "coop",
        "pvp",
        "f2p",
        "max_online_players",
        "max_hot_seat_players",
    )


class BoardgameAdmin(admin.ModelAdmin):
    list_display = ("title", "game_time", "min_players", "max_players")


admin.site.register(Videogame, VideogameAdmin)
admin.site.register(Player)
admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(VideogameRating)
admin.site.register(TokenResetPassword)
