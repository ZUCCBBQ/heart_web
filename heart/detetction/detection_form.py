from django import forms


class registerForm(forms.Form):
    name = forms.CharField(label="name",max_length=15,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password =forms.CharField(label="password",max_length=15,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password2", max_length=15,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    reason = forms.CharField(label="reason",widget=forms.Textarea(attrs={'class': 'form-control'}))
