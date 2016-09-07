"""
Forms for collections.
"""
from django.utils.translation import ugettext as _
from django import forms

from libs.ocl import OclApi

from apps.core.views import _get_source_type_list, _get_locale_list


class CollectionCreateForm(forms.Form):
    """ collection create form """
    required_css_class = 'required'

    short_code = forms.CharField(
        label=_('Collection Short code'),
        max_length=128,
        required=True,
        help_text=_('Short Name (e.g. ICD-10), Your new collection will live at: '
                    'https://OpenConceptLab.com/[OwnerType]/[Owner]/collections/'
                    '<span id="collection-name">[CollectionName]</span>'))
    name = forms.CharField(
        label=_('Collection Name'),
        max_length=128,
        required=True,
        help_text=_('Name (e.g. ICD-10), Your new collection will live at: '))

    full_name = forms.CharField(
        label=_('Collection Full Name'),
        required=True,
        help_text=_('Full Name (e.g. International Classification for Diseases v10)'))
    website = forms.URLField(
        label=_('Website'),
        required=False,
        help_text=_('Website (e.g. http://apps.who.int/classifications/icd10)'))
    collection_type = forms.ChoiceField(
        choices=[(v, v) for v in _get_source_type_list()],
        label=_('Collection Type'),
        required=False)
    public_access = forms.ChoiceField(
        label=_('Public Access'),
        required=False,
        initial='View',
        choices=(('View', 'View (default)'), ('Edit', 'Edit'), ('None', 'None')))
    default_locale = forms.ChoiceField(
        choices=[(d['code'], d['name']) for d in _get_locale_list()],
        label=_('Locale'),
        required=True)
    supported_locales = forms.CharField(
        max_length=30,
        label=_('Supported Locales'),
        required=True)

    description = forms.CharField(max_length=80, label=_('Description'), required=False)
    external_id = forms.CharField(
        label=_('External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))

    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        collection = self.initial['collection']
        request = self.initial['request']
        api = OclApi(request, debug=True)
        result = api.get('orgs', collection['owner'], 'collections', collection['id'],
                         'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used.'))
        return concept_id


class CollectionDeleteForm(forms.Form):
    required_css_class = 'required'


class CollectionEditForm(CollectionCreateForm):
    """ Form to edit collections """

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(CollectionEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_code')


class CollectionVersionAddForm(forms.Form):

    required_css_class = 'required'
    id = forms.CharField(
        label=_('ID'),
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'width:480px;',
                   'placeholder': "Name this Collection version"}))

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={'style': 'width:480px;',
                                     'rows': 5,
                                     'placeholder': 'Describe this Collection version'}))

    previous_version = forms.CharField(
        required=True,
        widget=forms.HiddenInput()),

    # released = forms.BooleanField(required=False, label=_('Released'))
