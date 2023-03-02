from django import forms
from .models import User,Student,Course,TimePeriod,Program,CourseAllocation


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_type','username','email','mobile_number','first_name','last_name','address','profiles']
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder':'  username ','style': 'font-size:13px;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'  email@email.com','style': 'font-size:13px;'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control','style': 'font-size:13px;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'  firstname ','style': 'font-size:13px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'  lastname ','style': 'font-size:13px;'}),
            'address': forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':13}),
            'profiles': forms.FileInput()
        }
        exclude = ['user_type']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['department','period']
        exclude = ['user']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('level','department','title','description')

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = "__all__"



class CourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'browser-default checkbox'}),
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ['lecturer', 'courses']