# Generated by Django 4.2.20 on 2025-03-21 20:06

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0023_homepage_background_color_ban_homepage_font_color_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="cards",
            field=wagtail.fields.StreamField(
                [("card", 4)],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {"required": False},
                    ),
                    1: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {"features": ["bold", "italic", "underline"], "required": True},
                    ),
                    2: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "underline",
                                "strikethrough",
                                "superscript",
                                "subscript",
                                "h2",
                                "h3",
                                "h4",
                                "h5",
                                "h6",
                                "ol",
                                "ul",
                                "hr",
                                "blockquote",
                                "code",
                                "link",
                                "document-link",
                                "embed",
                                "image",
                                "table",
                                "color",
                            ],
                            "required": True,
                        },
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"default": "#000000", "max_length": 7},
                    ),
                    4: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("imagex", 0),
                                ("title", 1),
                                ("description", 2),
                                ("font_color", 3),
                            ]
                        ],
                        {},
                    ),
                },
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="cards2",
            field=wagtail.fields.StreamField(
                [("card", 4)],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {"required": False},
                    ),
                    1: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {"features": ["bold", "italic", "underline"], "required": True},
                    ),
                    2: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "underline",
                                "strikethrough",
                                "superscript",
                                "subscript",
                                "h2",
                                "h3",
                                "h4",
                                "h5",
                                "h6",
                                "ol",
                                "ul",
                                "hr",
                                "blockquote",
                                "code",
                                "link",
                                "document-link",
                                "embed",
                                "image",
                                "table",
                                "color",
                                "colorpicker",
                            ],
                            "required": True,
                        },
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"default": "#000000", "max_length": 7},
                    ),
                    4: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("imagex", 0),
                                ("title", 1),
                                ("description", 2),
                                ("font_color", 3),
                            ]
                        ],
                        {},
                    ),
                },
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="cards3",
            field=wagtail.fields.StreamField(
                [("card", 4)],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {"required": False},
                    ),
                    1: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {"features": ["bold", "italic", "underline"], "required": True},
                    ),
                    2: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "underline",
                                "strikethrough",
                                "superscript",
                                "subscript",
                                "h2",
                                "h3",
                                "h4",
                                "h5",
                                "h6",
                                "ol",
                                "ul",
                                "hr",
                                "blockquote",
                                "code",
                                "link",
                                "document-link",
                                "embed",
                                "image",
                                "table",
                                "color",
                            ],
                            "required": True,
                        },
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"default": "#000000", "max_length": 7},
                    ),
                    4: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("imagex", 0),
                                ("title", 1),
                                ("description", 2),
                                ("font_color", 3),
                            ]
                        ],
                        {},
                    ),
                },
            ),
        ),
    ]
