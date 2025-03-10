from django.db import models
from wagtail.models import Page
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail.fields import StreamField
from wagtail.blocks import StructBlock, CharBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks

class CardBlock(StructBlock):
    """A reusable card block with image, title, description, and link."""
    imagex = ImageChooserBlock(required=False)
    title = CharBlock(required=True, max_length=100)
    description = TextBlock(required=True)

    class Meta:
        template = "home/card_block.html"  # Create this template later
        icon = "placeholder"
        label = "Card"

class HomePage(Page):
    heading = models.CharField(max_length=255, default="Soluciones integrales en tecnología")
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    image1 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    image2 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    image3 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    background_color = models.CharField(max_length=7, default="#ffffff")
    paragraph_text = models.TextField(
        default="Calidad y experiencia en servicios",
        help_text="Edit this text from the Wagtail admin panel."
    )

    cards = StreamField([("card", CardBlock())], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("image"),
        NativeColorPanel("background_color"),
        FieldPanel("paragraph_text"),
        FieldPanel("image1"),
        FieldPanel("image2"),
        FieldPanel("image3"),
        FieldPanel("cards"),
    ]
