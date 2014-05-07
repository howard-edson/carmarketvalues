from django import forms
from cmv_app.models import Search
#from .models import UserProfile
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, MultiField, Div, HTML, \
    Field, Reset, Fieldset, ButtonHolder
from crispy_forms.bootstrap import FormActions, AppendedText, InlineCheckboxes,\
    InlineField, InlineRadios, PrependedText
from django.core.urlresolvers import reverse
import datetime
from cmv_app.shortcuts import MAKES, DynamicChoiceField, regions


form_layout=Layout(
            HTML('''
                {% if messages %}
                {% for message in messages %}
                <p {% if message.tags %} style="text-align:center"
                class="alert alert-{{ message.tags }}"
                {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                '''),
            'regions',
            'vehicle_make',
            'vehicle_model',
            'extra_keywords',
            AppendedText('max_price', '$', active=True),
            AppendedText('min_price', '$', active=True),
            'max_year',
            'min_year',
            PrependedText('pic_only',''),
            PrependedText('search_title_only','',css_class="shift"),
            InlineRadios('seller_type'),
            Field('submit_button_type', type='hidden'),
        )

class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        exclude = ("user", "created",)
        
class SearchInputForm(forms.ModelForm):
    # This is a hidden field that holds the submit type value. Used to
    # determine whether the user clicked 'Save' or 'Save & Add Another' in
    # the Search Create Form.
    submit_button_type = forms.CharField(required=False)
    
    NA=(('NA','     --------------- SELECT MAKE -------------      '),)
    vehicle_model=DynamicChoiceField(
                    label="Car model",
                    choices=NA, 
                    widget=forms.Select(attrs={'id':'makes','disabled':'disabled'})
                   )
    
    def __init__(self, *args, **kwargs):
        super(SearchInputForm, self).__init__(*args, **kwargs)
        self.fields['max_year'] = forms.ChoiceField(
            choices=self.get_my_choices(),
            initial=datetime.datetime.now().year)
        
        self.fields['min_year'] = forms.ChoiceField(
            choices=self.get_my_choices(),
            initial=datetime.datetime.now().year-20)
        
        self.fields['vehicle_make']=forms.ChoiceField(
                    #initial="NA",
                    label="Car make",
                    choices=MAKES, 
                    widget=forms.Select(attrs={'id':'makes'})
                    )

        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-3 col-md-2 col-lg-2'
        self.helper.field_class = 'col-xs-9 col-md-10 col-lg-10'
        self.helper.layout = Layout(
            form_layout,
        )
        
    class Meta:
        model = Search
        exclude = ('user','vehicle_make','vehicle_model',)
        
    def get_my_choices(self):
        return [(r,r) for r in range(1980,(datetime.datetime.now().year+1))]
        

class SearchCreateForm(SearchInputForm):
    
    def __init__(self, *args, **kwargs):
        super(SearchCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit_and_add', 'Save & Add Another',
                                     css_class='pull-right'))
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('searchhome')))
        
            
class SearchUpdateForm(SearchInputForm):
    
    
        
    def __init__(self, *args, **kwargs):
        super(SearchUpdateForm, self).__init__(*args, **kwargs)
        self.vehicle_make=self.instance.vehicle_make
        #regions=self.instance.regions.all()
        
        self.helper.add_input(Submit('Update', 'update'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('home')))
        delete_url = reverse('search_delete', args=(self.instance.id,))
        self.helper.add_input(Button('delete', 'Delete',
                                     onclick='location.href="%s";' % delete_url,
                                     css_class='btn-danger pull-right'))

        #override the initial value of vehicle_make
        self.fields['vehicle_make'].initial = self.vehicle_make
                    
        #the model field is used in jquery to set the intial field for car model
        self.fields['model']=model=forms.CharField(max_length=100,initial=self.instance.vehicle_model)
        #this field is used only to preset the car model for updateview
        self.helper.layout = Layout(
                            form_layout,   
                            Field('model', type='hidden'),)
        

class SortFieldsForm(forms.Form):
#     latest_year=forms.BooleanField(label="latest year")
#     newest_entry=forms.BooleanField(label="newest post")
#     
#     #lowest_price=forms.BooleanField(label="lowest price")
#     #highest_price=forms.BooleanField(label="highest price")
#     
#     price_order=forms.ChoiceField(
#                     widget=forms.RadioSelect,
#                     label="price order",
#                     choices=(('lowest_price','lowest '),('highest_price','highest'),),
#                     initial="lowest_price",
#                     )
#     
#     def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-exampleForm'
#         self.helper.form_class = 'form-inline'
#         #self.helper.field_template='bootstrap3/layout/inline_field.html'
#         #self.helper.label_class='col-lg-2'
#         #self.helper.field_class='col-lg-12 form-control'
#         self.helper.form_method = 'post'
#         self.helper.form_action = 'sort_posting'
# 
#         super(SortFieldsForm, self).__init__(*args, **kwargs)
#         
#         self.helper.layout = Layout(
#            Div(
#             InlineRadios('price_order'),
#             ),
#             'newest_entry',
#             'latest_year',
#             #PrependedText('LowestPrice', ''),
#             #PrependedText('HighestPrice', ''),
#             #InlineCheckboxes('LowestPrice'),
#             #PrependedText('Newest_Entry', ''),
#             #    PrependedText('Latestyear', ''),
#             #ButtonHolder(
#                 Submit('submit', 'Submit', css_id="submit_sortform", css_class='button white')
#             #)
#         )
#     
    text_input = forms.CharField()
    textarea = forms.CharField(
    widget = forms.Textarea(),
    )
     
    radio_buttons = forms.ChoiceField(
    choices = (
    ('option_one', "Option one is this and that be sure to include why it's great"),
    ('option_two', "Option two can is something else and selecting it will deselect option one")
    ),
    widget = forms.RadioSelect,
    initial = 'option_two',
    )
     
    checkboxes = forms.MultipleChoiceField(
    choices = (
    ('option_one', "Option one is this and that be sure to include why it's great"),
    ('option_two', 'Option two can also be checked and included in form results'),
    ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
    ),
    initial = 'option_one',
    widget = forms.CheckboxSelectMultiple,
    help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )
     
    appended_text = forms.CharField(
    help_text = "Here's more help text"
    )
     
    prepended_text = forms.CharField()
     
    prepended_text_two = forms.CharField()
     
    multicolon_select = forms.MultipleChoiceField(
    choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )
     
    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
    Field('text_input', css_class='input-xlarge'),
    Field('textarea', rows="3", css_class='input-xlarge'),
    'radio_buttons',
    Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
    AppendedText('appended_text', '.00'),
    PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
    PrependedText('prepended_text_two', '@'),
    'multicolon_select',
    FormActions(
    Submit('save_changes', 'Save changes', css_class="btn-primary"),
    Submit('cancel', 'Cancel'),
    )
    )


        
