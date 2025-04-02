from django.db import models
from modelcluster.models import ClusterableModel
from django.shortcuts import render
from wagtail.models import Page
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import StructBlock, CharBlock, TextBlock, URLBlock, RichTextBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey

from django import forms
from django.core.mail import send_mail
import re
from django.utils.html import escape

def clean_html(text):
    allowed_tags = ['b', 'i', 'u', 'span', 'a', 'h1', 'h2', 'h3', 'p', 'br', 'ul', 'ol', 'li']
    return bleach.clean(text, tags=allowed_tags)

# 📌 Modelo para el Carrusel
class CarouselImage(models.Model):
    id = models.AutoField(primary_key=True)  # Definir clave primaria explícitamente
    page = ParentalKey("home.HomePage", on_delete=models.CASCADE, related_name="carousel_images")
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="+"
    )
    caption = RichTextField(features=[
    'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
    'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
    'code', 'link', 'document-link', 'embed', 'image', 'table','color',"font_color",
    ], blank=True, null=True)
    font_color = models.CharField(max_length=7, default="#000000")  # Default black
    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
        NativeColorPanel("font_color"),
    ]

    def save(self, *args, **kwargs):
        # Modify the rich text content to inject the font_color
        if self.font_color:
            caption_html = self.caption
            # Inject the color as an inline style to all paragraphs, spans, or inline text
            caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                                  r'\1<span style="color: ' + escape(self.font_color) + ';">', caption_html)
            caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
            self.caption = caption_html

        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Imagen del Carrusel"
        verbose_name_plural = "Imágenes del Carrusel"


class Section(models.Model):
    id = models.AutoField(primary_key=True)  # Definir clave primaria explícitamente
    page = ParentalKey("home.HomePage", on_delete=models.CASCADE, related_name="secciones")
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="+"
    )
    title = RichTextField(features=["bold", "italic", "h2", "h3"], blank=False, verbose_name="Titulo")
    caption = RichTextField(features=[
    'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
    'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
    'code', 'link', 'document-link', 'embed', 'image', 'table','color',"font_color",
    ], blank=True, null=True, verbose_name='Descripcion')
    font_color = models.CharField(max_length=7, default="#000000", verbose_name="Color descripcion")  # Default black
    font_color2 = models.CharField(max_length=7, default="#000000", verbose_name="Color titulo")  # Default black
    target = models.CharField(max_length=50, blank=True, help_text="ID del target de la imagen")
    panels = [
        FieldPanel("image"),
        FieldPanel("title"),
        NativeColorPanel("font_color2"),
        FieldPanel("caption"),
        NativeColorPanel("font_color"),
    ]

    def save(self, *args, **kwargs):
        # Modify the rich text content to inject the font_color
        if self.font_color:
            caption_html = self.caption
            # Inject the color as an inline style to all paragraphs, spans, or inline text
            caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                                  r'\1<span style="color: ' + escape(self.font_color) + ';">', caption_html)
            caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
            self.caption = caption_html
        if self.font_color2:
            caption_html2 = self.title
            # Inject the color as an inline style to all paragraphs, spans, or inline text
            caption_html2 = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                                  r'\1<span style="color: ' + escape(self.font_color2) + ';">', caption_html2)
            caption_html2 = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html2)
            self.title = caption_html2

        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"

class Card(models.Model):
    """Tarjeta reutilizable dentro de una sección con colores forzados"""
    id = models.AutoField(primary_key=True)
    section = ParentalKey("home.SectionG", on_delete=models.CASCADE, related_name="cardsgeneral") 
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    title = RichTextField(features=["bold", "italic", "h3", "h4","font_color",], blank=False)
    description = RichTextField(features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
        'code', 'link', 'document-link', 'embed', 'image', 'table', 'color',"font_color",
    ], blank=True, null=True)
    font_color = models.CharField(max_length=7, default="#000000", verbose_name="Color del texto de la descripción")  
    font_color2 = models.CharField(max_length=7, default="#000000", verbose_name="Color del texto del titulo") 
    panels = [
        FieldPanel("image"),
        FieldPanel("title"),
        NativeColorPanel("font_color2"),
        FieldPanel("description"),
        NativeColorPanel("font_color"),
    ]

    def save(self, *args, **kwargs):
        """Inyecta colores en la descripción antes de guardar"""
        if self.font_color:
            self.description = self.apply_color(self.description, self.font_color)
        if self.font_color2:
            self.title = self.apply_color(self.title, self.font_color2)
        super().save(*args, **kwargs)

    def apply_color(self, text, color):
        """Método auxiliar para aplicar color inline al texto"""
        text = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                      rf'\1<span style="color: {escape(color)};">', text)
        text = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', text)
        return text

    class Meta:
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"


class SectionG(ClusterableModel, models.Model):
    """Sección que puede contener varias tarjetas con colores forzados"""
    id = models.AutoField(primary_key=True)  # Definir clave primaria explícitamente
    page = ParentalKey("home.HomePage", on_delete=models.CASCADE, related_name="sectionsG")
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    title = RichTextField(features=["bold", "italic", "h2", "h3","font_color",], blank=False)
    caption = RichTextField(features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
        'code', 'link', 'document-link', 'embed', 'image', 'table', 'color',"font_color",
    ], blank=True, null=True)
    font_color = models.CharField(max_length=7, default="#000000", verbose_name="Color del texto de la descripción")
    font_color2 = models.CharField(max_length=7, default="#000000", verbose_name="Color del título")
    # Añadiendo información de los Banners por seccion
    backimg = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", blank=True, null=True, verbose_name="Imagen division seccion"
    )
    backcolor = models.CharField(max_length=7, default="#ffffff", verbose_name="Transparencia de la seccion")
    backcontent =  models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="+", blank=True, null=True, verbose_name="Imagen seccion"
    )
    backcontent_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Transparencia de la seccion")

    panels = [
        FieldPanel("image"),
        FieldPanel("title"),
        NativeColorPanel("font_color2"),
        FieldPanel("caption"),
        NativeColorPanel("font_color"),
        FieldPanel("backimg"),
        NativeColorPanel("backcolor"),
        FieldPanel("backcontent"),
        NativeColorPanel("backcontent_color"),

        InlinePanel("cardsgeneral", label="Tarjetas dentro de la sección"),  # ✅ Permite múltiples tarjetas en la sección
    ]

    def save(self, *args, **kwargs):
        """Inyecta colores en título y caption antes de guardar"""
        if self.font_color:
            self.caption = self.apply_color(self.caption, self.font_color)
        if self.font_color2:
            self.title = self.apply_color(self.title, self.font_color2)
        super().save(*args, **kwargs)

    def apply_color(self, text, color):
        """Método auxiliar para aplicar color inline al texto"""
        text = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                      rf'\1<span style="color: {escape(color)};">', text)
        text = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', text)
        return text

    class Meta:
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"


# section clientes

class ClientslImage(models.Model):
    id = models.AutoField(primary_key=True)  # Definir clave primaria explícitamente
    page = ParentalKey("home.HomePage", on_delete=models.CASCADE, related_name="carousel_clients")
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="+"
    )
    panels = [
        FieldPanel("image"),
    ]


    class Meta:
        verbose_name = "Imagen del Carrusel"
        verbose_name_plural = "Imágenes del Carrusel"

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def send_email(self):
        send_mail(
            subject="Nuevo mensaje de contacto",
            message=f"Nombre: {self.cleaned_data['name']}\n"
                    f"Email: {self.cleaned_data['email']}\n"
                    f"Mensaje:\n{self.cleaned_data['message']}",
            from_email="info@teravolt.com.bo",
            recipient_list=[self.cleaned_data['email'], 'jfibanezquiroz@gmail.com', 'info@teravolt.com.bo'],
            fail_silently=False,
        )



class CardBlock(StructBlock):
    """A reusable card block with image, title, description, and link."""
    imagex = ImageChooserBlock(required=False)
    title = RichTextBlock(features=['bold', 'italic', 'underline'], required=True)
    description = RichTextBlock(features=[
    'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
    'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
    'code', 'link', 'document-link', 'embed', 'image', 'table','color',
    ], required=True)
    font_color = CharBlock(max_length=7, default="#000000")  # Default black
    def save(self, *args, **kwargs):
        # Modify the rich text content to inject the font_color
        if self.font_color:
            caption_html = self.title
            # Inject the color as an inline style to all paragraphs, spans, or inline text
            caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                                  r'\1<span style="color: ' + escape(self.font_color) + ';">', caption_html)
            caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
            self.title = caption_html
        super().save(*args, **kwargs)
    class Meta:
        template = "home/card_block.html"  # Create this template later
        icon = "placeholder"
        label = "Card"
    

class CardBlock2(StructBlock):
    """A reusable card block with image, title, description, and link."""
    imagex = ImageChooserBlock(required=False)
    title = RichTextBlock(features=['bold', 'italic', 'underline'], required=True)
    description = RichTextBlock(features=[
    'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
    'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
    'code', 'link', 'document-link', 'embed', 'image', 'table','color','colorpicker'
    ], required=True)
    font_color = CharBlock(max_length=7, default="#000000")  # Default black
    class Meta:
        template = "home/card_block2.html"  # Create this template later
        icon = "placeholder"
        label = "Card"
    def save(self, *args, **kwargs):
        # Modify the rich text content to inject the font_color
        if self.font_color:
            caption_html = self.title
            # Inject the color as an inline style to all paragraphs, spans, or inline text
            caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                                  r'\1<span style="color: ' + escape(self.font_color) + ';">', caption_html)
            caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
            self.title = caption_html

class CardBlock3(StructBlock):
    """A reusable card block with image, title, description, and link."""
    imagex = ImageChooserBlock(required=False)
    title = RichTextBlock(features=['bold', 'italic', 'underline'], required=True)
    description = RichTextBlock(features=[
    'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',  
    'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',  
    'code', 'link', 'document-link', 'embed', 'image', 'table','color',
    ], required=True)
    font_color = CharBlock(max_length=7, default="#000000")  # Default black
    class Meta:
        template = "home/card_block3.html"  # Create this template later
        icon = "placeholder"
        label = "Card"
    def save(self, *args, **kwargs):
        # Modify the rich text content to inject the font_color
        if self.font_color:
            caption_html = self.title
            # Inject the color as an inline style to all paragraphs, spans, or inline text
            caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
                                  r'\1<span style="color: ' + escape(self.font_color) + ';">', caption_html)
            caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
            self.title = caption_html

class HomePage(Page):
    heading = RichTextField(
    default="Calidad y experiencia en servicios",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )
    banner = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    font_color = models.CharField(max_length=7, default="#000000")  # Default black
    # font_color2 = models.CharField(max_length=7, default="#000000")  # Default black
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Logo Teravolt",
        related_name='+'
    )
    image1 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Seccion 1",
        related_name='+'
    )
    image2 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Seccion 2",
        related_name='+'
    )
    image3 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Seccion 3",
        related_name='+'
    )
    # background_color = models.CharField(max_length=7, default="#ffffff")
    background_color_ban = models.CharField(max_length=7, default="#ffffff")

    cards = StreamField([("card", CardBlock())], blank=True, use_json_field=True)
    cards2 = StreamField([("card", CardBlock2())], blank=True, use_json_field=True)
    cards3 = StreamField([("card", CardBlock3())], blank=True, use_json_field=True)

    # Color tipografia secciones
    font_color_secciones = models.CharField(max_length=7, default="#000000", verbose_name="Color titulo Secciones")  # Default black

    #Seccion 1
    seccion1 = RichTextField(
    default="ELECTROMECANICA",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',"font_color"
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    p1 = RichTextField(
    default="ELECTROMECANICA",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )
    bannerS1 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division Seccion 1",
        related_name='+'
    )
    background_color_s1 = models.CharField(max_length=7, default="#ffffff")
    backS1 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="background Seccion 1",
        related_name='+'
    )
    background_color_b1 = models.CharField(max_length=7, default="#ffffff")
    #Seccion 2
    seccion2 = RichTextField(
    default="MANTENIMIENTO INDUSTRIAL",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',"font_color"
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    p2 = RichTextField(
    default="MANTENIMIENTO INDUSTRIAL",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    bannerS2 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division Seccion 2",
        related_name='+'
    )
    background_color_s2 = models.CharField(max_length=7, default="#ffffff")
    backS2 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="background Seccion 2",
        related_name='+'
    )
    background_color_b2 = models.CharField(max_length=7, default="#ffffff")
    #Seccion 3
    seccion3 = RichTextField(
    default="SISTEMAS DE SEGURIDAD",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',"font_color"
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    p3 = RichTextField(
    default="SISTEMAS DE SEGURIDAD",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    bannerS3 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division Seccion 3",
        related_name='+'
    )
    background_color_s3 = models.CharField(max_length=7, default="#ffffff")
    backS3 = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="background Seccion 3",
        related_name='+'
    )
    background_color_b3 = models.CharField(max_length=7, default="#ffffff")

    bannerMsec = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division seccion Vision Mision",
        related_name='+'
    )
    bannerMV = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division Vision Mision",
        related_name='+'
    )


    #Seccion clientes
    seccionCliente = RichTextField(
    default="Clientes",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',"font_color"
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    pCliente = RichTextField(
    default="SISTEMAS DE SEGURIDAD",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )

    bannerSC = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division Seccion Cliente",
        related_name='+'
    )
    background_color_sC = models.CharField(max_length=7, default="#ffffff")
    backSC = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="background Seccion Cliente",
        related_name='+'
    )
    background_color_bC = models.CharField(max_length=7, default="#ffffff")

    bannerMV = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Imagen Division Mision Vision",
        related_name='+'
    )
    bannerMV_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Color fondo de Mision Vision")
    MV_colorback = models.CharField(max_length=7, default="#ffffff", verbose_name="Color de fondo titulo seccion")
    pMVT = RichTextField(
        default = "Mision Vision",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','font_color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )
    # font_MVT =  models.CharField(max_length=7, default="#ffffff")

    pMV1 = RichTextField(
        default = "mision",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','font_color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )
    pMV2 = RichTextField(
        default = "vision",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','font_color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )
    fontMV = models.CharField(max_length=7, default="#ffffff")

    pQS = RichTextField(
        default = "Quienes somos",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','font_color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )
    pOB = RichTextField(
        default = "objetivos",
    features=[
        'bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript',
        'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'blockquote',
        'code', 'link', 'document-link', 'embed', 'image', 'table','font_color',
        ],
        help_text="Edit this text from the Wagtail admin panel."
    )


    facebook_url = models.URLField(blank=True, help_text="Enlace a tu página de Facebook")
    whatsapp_number = models.URLField(blank=True, help_text="Número de WhatsApp con código de país")
    linkedin_url = models.URLField(blank=True, help_text="Enlace a tu perfil o empresa en LinkedIn")

    country = models.CharField(max_length=100, default="Bolivia")
    address = models.CharField(max_length=255, default="Calle Ejemplo #123")
    city = models.CharField(max_length=100, default="La Paz")
    
    email = models.EmailField(default="contacto@tuempresa.com")
    phone = models.CharField(max_length=20, default="+591 700-00000")
    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("image"),
        FieldPanel("banner"),
        NativeColorPanel("background_color_ban"),
        InlinePanel("carousel_images", label="Imágenes del Carrusel"),  # 📌 Agregamos el InlinePanel para el carrusel
        InlinePanel("sectionsG", label="Secciones de la página dinamica"),
        FieldPanel("seccionCliente"),
        FieldPanel("bannerSC"),
        FieldPanel("background_color_sC"),
        FieldPanel("backSC"),
        FieldPanel("background_color_bC"),
        InlinePanel("carousel_clients", label="Imágenes del cliente"),  # 📌 Agregamos el InlinePanel para el carrusel
        FieldPanel("bannerMsec"),
        FieldPanel("bannerMV"),
        FieldPanel("pMVT"),
        # NativeColorPanel("font_MVT"),
        NativeColorPanel("bannerMV_color"),
        NativeColorPanel("MV_colorback"),
        FieldPanel("pMV1"),
        FieldPanel("pMV2"),
        FieldPanel("pQS"),
        FieldPanel("pOB"),
        FieldPanel("facebook_url"),
        FieldPanel("whatsapp_number"),
        FieldPanel("linkedin_url"),
        FieldPanel("country"),
        FieldPanel("address"),
        FieldPanel("city"),
        FieldPanel("email"),
        FieldPanel("phone"),
    ]

    # def save(self, *args, **kwargs):
    #     if self.font_MVT:
    #         caption_html = self.pMVT
    #         # Inject the color as an inline style to all paragraphs, spans, or inline text
    #         caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
    #                               r'\1<span style="color: ' + escape(self.font_MVT) + ';">', caption_html)
    #         caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
    #         self.pMVT = caption_html
    #     # if self.fontMV:
    #     #     caption_html = self.pMV1
    #     #     # Inject the color as an inline style to all paragraphs, spans, or inline text
    #     #     caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
    #     #                           r'\1<span style="color: ' + escape(self.fontMV) + ';">', caption_html)
    #     #     caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
    #     #     self.pMV1 = caption_html
        
    #     # if self.fontMV:
    #     #     caption_html = self.pMV2
    #     #     # Inject the color as an inline style to all paragraphs, spans, or inline text
    #     #     caption_html = re.sub(r'(<p[^>]*>|<span[^>]*>|<div[^>]*>)', 
    #     #                           r'\1<span style="color: ' + escape(self.fontMV) + ';">', caption_html)
    #     #     caption_html = re.sub(r'(</p>|</span>|</div>)', r'</span>\1', caption_html)
    #     #     self.pMV2 = caption_html


    #     super().save(*args, **kwargs)

    def serve(self, request):
        form = ContactForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                form.send_email()
                # After sending the email, we redirect to the same page to avoid re-submitting
                return render(request, "home/home_page.html", {
                    "form": ContactForm(),  # Empty form after submission
                    "success": True,        # Show success message
                    "page": self,
                })
            else:
                # If form is invalid, return the form with errors
                return render(request, "home/home_page.html", {
                    "form": form,
                    "page": self,
                })
        else:
            # On GET request, simply return the empty form
            return render(request, "home/home_page.html", {
                "form": form,
                "page": self,
            })