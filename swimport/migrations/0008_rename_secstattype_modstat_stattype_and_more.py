# Generated by Django 4.1.3 on 2022-11-26 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("swimport", "0007_rename_primarystattype_mod_pristattype_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="modstat",
            old_name="secStatType",
            new_name="StatType",
        ),
        migrations.RenameField(
            model_name="modstat",
            old_name="secStatValue",
            new_name="StatValue",
        ),
        migrations.RemoveField(
            model_name="modstat",
            name="secStatRoll",
        ),
        migrations.AddField(
            model_name="modstat",
            name="StatRoll",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="modstat",
            name="statPS",
            field=models.CharField(default="P", max_length=1),
        ),
    ]