from django import forms
from .models import User,Student,Course,TimePeriod


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','mobile_number','first_name','last_name','address','profiles']
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder':'  username ','style': 'font-size:13px;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'  email@email.com','style': 'font-size:13px;'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control','style': 'font-size:13px;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'  firstname ','style': 'font-size:13px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'  lastname ','style': 'font-size:13px;'}),
            'address': forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':13}),
            'profiles': forms.FileInput()
        }
        exclude = ['profiles']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['course','period','user']
        exclude = ['user']

