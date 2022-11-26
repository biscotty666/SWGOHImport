# Generated by Django 4.1.3 on 2022-11-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("swimport", "0011_rename_statroll_modstat_statroll_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="modstat",
            old_name="statRoll",
            new_name="roll",
        ),
        migrations.RenameField(
            model_name="modstat",
            old_name="statValue",
            new_name="value",
        ),
        migrations.RemoveField(
            model_name="modstat",
            name="statPS",
        ),
        migrations.AddField(
            model_name="modstat",
            name="unitStat",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="modstat",
            name="statType",
            field=models.CharField(default="P", max_length=1),
        ),
    ]
