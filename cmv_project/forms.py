from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Fieldset, Field, Submit, Button
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from passwords.fields import PasswordField


class UserSettingsForm(forms.Form):
    """
    Form to allow users to change profile settings and preferences.
    """
    username = forms.CharField(required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email', required=False)
        
        
    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-6'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'
        self.helper.help_text_inline = False
        #self.helper.add_input(Submit('submit', 'Save'))
        #self.helper.add_input(Button(
        #    'cancel', 'Cancel', onclick='location.href="%s";' % \
        #                                reverse('home')))

        self. helper.layout = Layout(
            HTML('''
            {% if messages %}
            {% for message in messages %}
            <p {% if message.tags %} class="alert alert-{{ message.tags }}"\
            {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
            </p>
            '''),
            Fieldset(
                'Profile',
                Field('username', readonly=True),
                Field('email'),
                Field('first_name'),
                Field('last_name'),
                Field('time_zone'),
            ),
            FormActions(
                Submit('submit','Save'),
                Button('cancel','Cancel', \
                       onclick='location.href="%s";' % reverse('searchhome')),
                css_class='col-xs-12 col-md-offset-4',   
            ),
            #col-xs-12 col-md-offset-4
        )

    def clean_email(self):
        """
        Validates the email field.

        Check if the email field changed. If true, check whether the new email
        address already exists in the database and raise an error if it does.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(username=self.cleaned_data['username'])

        if email != user.email:
            if User.objects.filter(email=email):
                raise forms.ValidationError('Another account is already using '
                                            'this email address.')

        return email
    


 
class ValidatingSetPasswordForm(SetPasswordForm):
    new_password2 = PasswordField(label=_("New password confirmation"))
 
class ValidatingPasswordChangeForm(PasswordChangeForm):
    new_password2 = PasswordField(label=_("New password confirmation"))
