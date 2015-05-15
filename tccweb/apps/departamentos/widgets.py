# from django import forms
# from django.conf import settings
# from django.utils.safestring import mark_safe

# class ColorPickerWidget(forms.TextInput):
#     class Media:
#         css = {
#             'all': (
#                 '/media/css/colorPicker.css',
#             )
#         }
#         js = (
#             '/media/js/jquery-1.6.2.min.js',
#             '/media/js/jquery.colorPicker.js',
#         )

#     def __init__(self, language=None, attrs=None):
#         self.language = language or settings.LANGUAGE_CODE[:2]
#         super(ColorPickerWidget, self).__init__(attrs=attrs)

#     def render(self, name, value, attrs=None):
#         rendered = super(ColorPickerWidget, self).render(name, value, attrs)
#         return rendered + mark_safe(u'''<script type="text/javascript">
#             $('#id_%s').colorPicker();
#             </script>''' % name)


from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string

class ColorWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        colors = settings.COLORPICKER_COLORS
        return render_to_string("color_widget.html", locals())