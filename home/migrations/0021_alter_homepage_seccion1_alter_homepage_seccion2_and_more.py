# Generated by Django 4.2.20 on 2025-03-21 15:57

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0020_rename_paragraph_text_homepage_seccion1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="seccion1",
            field=wagtail.fields.RichTextField(
                default="ELECTROMECANICA",
                help_text="Edit this text from the Wagtail admin panel.",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="seccion2",
            field=wagtail.fields.RichTextField(
                default="MANTENIMIENTO INDUSTRIAL",
                help_text="Edit this text from the Wagtail admin panel.",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="seccion3",
            field=wagtail.fields.RichTextField(
                default="SISTEMAS DE SEGURIDAD",
                help_text="Edit this text from the Wagtail admin panel.",
            ),
        ),
    ]
