from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, CLS, CCLS, SLS



class LeaveRequestForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'
    from_date = forms.DateField(widget=DateInput)
    no_of_leaves = forms.IntegerField()


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
