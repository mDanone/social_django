from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post, PostComment, UserProfile
from django import forms



class RegistrationForm(UserCreationForm, ModelForm):
	email = forms.EmailField(max_length=200, help_text='Required')
	class Meta:
		model = User
		fields = ('username', 
				  'email',
				  'password1', 
				  'password2')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class LoginForm(AuthenticationForm, ModelForm):
	class Meta:
		model = User
		fields = ('username', 
				  'password')

class PostAddForm(ModelForm):
	class Meta:
		model = Post
		fields = ('title', 
				  'description',
				  'image')

class PostUpdateForm(ModelForm):
	class Meta:
		model = Post
		fields = ('title', 
				  'description', 
				  'image')

class CommentPostForm(ModelForm):
	class Meta:
		model = PostComment
		fields = ('text',)

class MyProfileForm(ModelForm, forms.Form):
	status = forms.CharField(required=False)
	display_status = forms.BooleanField(required=False)
	description = forms.CharField(widget=forms.Textarea, required=False)
	class Meta:
		model = User
		fields = ('username', 
			      'email', 
				  'first_name',
				  'last_name', 
				  'status',
				  'display_status', 
				  'description')


class MyProfileExtraDataForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('status', 
				  'display_status', 
				  'description',)
