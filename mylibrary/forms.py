from django import forms


class LoginForm(forms.Form):
    user_id = forms.CharField(label="学号", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    user_name = forms.CharField(label="姓名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_id = forms.CharField(label="学号", min_length=8, max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", min_length=6, max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", min_length=6, max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(label="关键词", max_length=60,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入关键词'}))