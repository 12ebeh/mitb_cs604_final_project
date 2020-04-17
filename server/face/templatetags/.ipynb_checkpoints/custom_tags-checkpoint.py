from django import template

register = template.Library()

@register.inclusion_tag('forms/image_upload.html')
def image_upload_widget(upload_widget_id, session_id):
    return {
        'upload_widget_id': upload_widget_id,
        'session_id': session_id
    }
