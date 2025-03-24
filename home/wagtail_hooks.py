import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail import hooks

@hooks.register('register_rich_text_features')
def register_font_color_feature(features):
    """
    Register a custom inline style feature for applying font color in the rich text editor.
    """
    feature_name = 'font_color'  # Feature name for the custom color
    type_ = 'INLINE_STYLE'  # Use INLINE_STYLE for inline styles (color)
    tag = 'span'  # We'll use <span> to apply the color inline

    control = {
        'type': type_,
        'label': 'Text Color',  # Label that will appear in the toolbar
        'description': 'Apply a custom color',
        'style': {'color': '#ff0000'},  # Default color, can be customized
    }

    # Register the editor plugin for Draftail
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # Register the conversion rule
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    features.default_features.append('font_color')

