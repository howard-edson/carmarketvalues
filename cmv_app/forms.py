from django import forms
from cmv_app.models import Search
#from .models import UserProfile
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, MultiField, Div, HTML, \
    Field, Reset
from crispy_forms.bootstrap import FormActions, AppendedText, InlineCheckboxes,\
    InlineField
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
            #Field('vehicle_make', placeholder='Ford', required=True, autofocus=True),
            'region',
            'vehicle_make',
            'vehicle_model',
            'extra_keywords',
            AppendedText('max_price', '$', active=True),
            AppendedText('min_price', '$', active=True),
            'max_year',
            'min_year',
            'pic_only',
            'search_title_only',
            InlineCheckboxes('seller_type'),
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
        
        self.fields['region']=forms.ChoiceField(
        label = "region",
        choices = tuple([(reg,reg) for reg in regions]),
        initial = 'seattle',
        required = True,
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
        exclude = ('user','regions','vehicle_make','vehicle_model')
        
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
        regions=self.instance.regions.all()
        
        self.helper.add_input(Submit('Update', 'update'))
        self.helper.add_input(Button(
            'cancel', 'Cancel', onclick='location.href="%s";' % \
                                        reverse('home')))
        delete_url = reverse('search_delete', args=(self.instance.id,))
        self.helper.add_input(Button('delete', 'Delete',
                                     onclick='location.href="%s";' % delete_url,
                                     css_class='btn-danger pull-right'))
        self.fields['vehicle_make'] = forms.ChoiceField(
                    initial=self.vehicle_make,
                    label="Car make",
                    choices=MAKES,
                    widget=forms.Select(attrs={'id':'makes'})
                    )
        
        self.fields['model']=model=forms.CharField(max_length=100,initial=self.instance.vehicle_model)
        self.fields['region']=forms.ChoiceField(
        label = "region",
        choices = tuple([(reg,reg) for reg in regions]),
        initial = regions[0],
        required = True,
        )
        self.helper.layout = Layout(
                            form_layout,   
                            Field('model', type='hidden'),)


# #not implemented yet
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         exclude = ("user",)
    
        
