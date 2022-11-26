from django.contrib import admin
from .models import Guild, Player, Toon, Skill, Mod, Equipped, ModStat

admin.site.register(Guild)
admin.site.register(Player)
admin.site.register(Toon)
admin.site.register(Skill)
admin.site.register(Mod)
admin.site.register(ModStat)
admin.site.register(Equipped)
# Register your models here.
