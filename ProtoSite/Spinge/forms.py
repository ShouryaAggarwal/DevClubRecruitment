from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, User, Profile, Course


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={'rows': '1', 'cols': '50'}),
        help_text='Tell us about yourself!',
        required=False
        )
    student = forms.BooleanField(required=False)
    professor = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = {'bio', 'student', 'professor'}

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        student = cleaned_data.get('student')
        professor = cleaned_data.get('professor')
        if student and professor:
            raise forms.ValidationError('You cannot be both student and a professor!')
        if not student and not professor:
            raise forms.ValidationError('You have to be either a student or a professor to join Spinge!')


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('label', 'body')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'about')
