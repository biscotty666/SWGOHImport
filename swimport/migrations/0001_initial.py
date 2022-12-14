# Generated by Django 4.1.3 on 2022-11-24 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Guild",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("guildId", models.CharField(blank=True, max_length=20)),
                ("name", models.CharField(blank=True, max_length=15)),
                ("desc", models.CharField(blank=True, max_length=100)),
                ("members", models.IntegerField()),
                ("status", models.IntegerField(null=True)),
                ("required", models.IntegerField(null=True)),
                ("gp", models.IntegerField()),
                ("bannerColor", models.CharField(blank=True, max_length=25)),
                ("bannerLogo", models.CharField(blank=True, max_length=25)),
                ("message", models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("playerId", models.CharField(max_length=15)),
                ("allycode", models.IntegerField()),
                ("level", models.IntegerField()),
                ("gp", models.IntegerField()),
                ("gpChar", models.IntegerField()),
                ("gpShip", models.IntegerField()),
                ("active", models.BooleanField(default=True)),
                ("guildMemberLevel", models.IntegerField()),
                ("updated", models.CharField(blank=True, max_length=30)),
                (
                    "guild",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="swimport.guild",
                    ),
                ),
            ],
            options={
                "ordering": ["playerId"],
            },
        ),
        migrations.CreateModel(
            name="Toon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("toonID", models.CharField(max_length=45)),
                ("toonName", models.CharField(max_length=45)),
                ("nameKey", models.CharField(max_length=45)),
                ("rarity", models.IntegerField()),
                ("toonLevel", models.IntegerField()),
                ("gp", models.IntegerField()),
                ("gearLevel", models.IntegerField()),
                ("primaryUnitStat", models.IntegerField()),
                ("relic", models.IntegerField()),
                ("combatType", models.IntegerField(blank=True)),
                ("crew", models.CharField(blank=True, max_length=45)),
                ("isZeta", models.CharField(blank=True, max_length=45)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="swimport.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Strike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("strike_date", models.DateField()),
                ("ishard", models.BooleanField(default=True)),
                ("comments", models.TextField(blank=True, max_length=200)),
                (
                    "activity",
                    models.CharField(
                        choices=[
                            ("TW", "TW"),
                            ("TB", "TB"),
                            ("Tickets", "Tickets"),
                            ("Other", "Other"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="swimport.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-strike_date"],
            },
        ),
    ]
