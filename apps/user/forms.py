from django import forms
from .models import User,Student,Course,Academics,Department,DepartmentAllocation,Semester,Classes


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_type','username','email','mobile_number','first_name','last_name','address','profile_image']
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder':'  username ','style': 'font-size:13px;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'  email@email.com','style': 'font-size:13px;'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control','style': 'font-size:13px;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'  firstname ','style': 'font-size:13px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'  lastname ','style': 'font-size:13px;'}),
            'address': forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':13}),
            'profile_image': forms.FileInput()
        }
        exclude = ['user_type']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['department','academic_year']
        exclude = ['user']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('department_id','title','course')



class DepartmentAllocationForm(forms.ModelForm):
    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'browser-default checkbox'}),
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="lecturer",
    )

    class Meta:
        model = DepartmentAllocation
        fields = ['lecturer', 'department']


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('semester_code','semester_name','semester_duration','is_current_semester','description')


class AcademicsForm(forms.ModelForm):
    class Meta:
        model = Academics
        fields = "__all__"

class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = "__all__"