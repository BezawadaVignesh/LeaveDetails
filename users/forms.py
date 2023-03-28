from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, CLS, CCLS, SLS, Profile


class SearchSIDFrom(forms.Form):
    sid = forms.CharField(max_length=100)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'sid', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'designation', 'department', 'ccl_left', 'image')


class HolidayForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'

    from_date = forms.DateField(widget=DateInput)
    no_of_leaves = forms.FloatField()
    desc = forms.CharField(max_length=200)


class LeaveRequestForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'

    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)
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
