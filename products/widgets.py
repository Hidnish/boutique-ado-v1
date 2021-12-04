from django.forms.widgets import ClearableFileInput
# re-labeling method to ' _ '
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    unput_text = _('')
    template_name = 'products/custom_widget_templates/custome_clearable_file_input.html'
