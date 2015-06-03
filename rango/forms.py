from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the\
            category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug  = forms.CharField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the page\
            name")
    url  = forms.URLField(max_length=200, help_text="Please enter the url of \
            the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta: 
        model = Page
        exclude = ('category', )
                

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture', )

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password', )

class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('password', )
