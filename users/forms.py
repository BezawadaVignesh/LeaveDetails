from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError
from .models import CustomUser, CLS, CCLS, SLS, Profile
from .verifier import generate_leaves


class SearchSIDFrom(forms.Form):
    sid = forms.CharField(max_length=100)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'sid', 'email', 'first_name', 'last_name', 'password1', 'password2']


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'designation', 'department', 'ccl_left', 'ssl_left', 'epl_left', 'image']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'sid', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'designation', 'department', 'ccl_left', 'ssl_left', 'epl_left', 'image')


class HolidayForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'

    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)
    desc = forms.CharField(max_length=200)


class BaseHolidayFormSet(BaseFormSet):
    def clean(self):
        """ Check if no dates are overlying """
        if any(self.errors):
            return

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            s_date = form.cleand_data.get('from_date')
            e_date = form.cleand_data.get('to_date')
            no = (e_date - s_date).days + 1
            if no < 1:
                raise ValidationError("Enter valid dates")


class LeaveRequestForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'

    from_date = forms.DateField(widget=DateInput)
    from_date.widget.attrs.update({'class': 'form-control'})
    to_date = forms.DateField(widget=DateInput)
    to_date.widget.attrs.update({'class': 'form-control'})
    half = forms.ChoiceField(choices=[("False", "Full day"), ("True", "Half Day")])
    half.widget.attrs.update({'class': 'form-control'})
    Type = forms.ChoiceField(choices=[("False", "default"), ("True", "EPLs")])
    Type.widget.attrs.update({'class': 'form-control'})
    # no_of_leaves = forms.FloatField()


class CLSAddForm(forms.ModelForm):
    class Meta:
        model = CLS
        fields = ('on_date',)


class CCLSAddForm(forms.ModelForm):
    class Meta:
        model = CCLS
        fields = ('on_date',)


class SLSAddForm(forms.ModelForm):
    class Meta:
        model = SLS
        fields = ('on_date',)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'sid',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'sid',)
