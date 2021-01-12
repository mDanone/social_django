from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, PostAddForm, PostUpdateForm, CommentPostForm
from .forms import MyProfileForm, MyProfileExtraDataForm
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, UserProfile, Follow
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect
# Create your views here.


class IndexView(TemplateView):
	template_name = 'base/index.html'

class SearchResultView(TemplateView):
	template_name = 'search_/search_result.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['result'] = User.objects.filter(first_name=self.request.GET.get('q'))
		if self.request.user.is_authenticated:
			context['current_user'] = User.objects.get(id = self.request.user.id)
			return context


class UserRegCreateView(CreateView):
	model = User
	form_class = RegistrationForm
	template_name = 'auth/reg.html'
	success_url = reverse_lazy('index')


	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.is_active= False
		self.object.save()
		current_site = get_current_site(self.request)
		mail_subject = 'Activate your blog account.'
		message = render_to_string('email_confirmation_message.html',
									{
									'user':self.object,
									'domain': current_site.domain,
									'uid':urlsafe_base64_encode(force_bytes(self.object.pk)),
									'token': account_activation_token.make_token(self.object)
									})
		to_email = self.object.email
		email = EmailMessage(mail_subject, message, to=[to_email])
		email.send()
		return super().form_valid(form)

class ActivationView(TemplateView):
	template_name = 'activate.html'
	def get(self, request, *args, **kwargs):
		try:
			uid = force_text(urlsafe_base64_decode(self.kwargs['id']))
			self.user = User.objects.get(id=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			self.user= None
		if self.user is not None and account_activation_token.check_token(self.user, self.kwargs['token']):
			self.user.is_active = True
			self.user.save()
			login(request, self.user)
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)

class UserLoginView(LoginView):
	form_class = LoginForm
	template_name = 'auth/login.html'
	success_url = reverse_lazy('index')
	def get_success_url(self):
		return self.success_url

class UserLogoutView(LogoutView):
	next_page = reverse_lazy('index')

class UserNewsView(LoginRequiredMixin, TemplateView):
	template_name = 'posts/news.html'
	login_url = reverse_lazy('index')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		list_subscribes = [i.signed for i in Follow.objects.filter(subscriber=self.request.user)]
		context['posts'] = Post.objects.filter(user__in=list_subscribes)
		return context

class UserAddPostView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'posts/add.html'
	form_class = PostAddForm
	success_url = reverse_lazy('news_page')
	login_url = reverse_lazy('add_post')
	redirect_field_name = 'hello'
	def get_success_url(self):
		return self.success_url

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class UpdatePostListView(LoginRequiredMixin, TemplateView):
	login_url  = reverse_lazy('index')
	success_url = reverse_lazy('news_page')
	template_name = 'posts/update_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(user=self.request.user)
		return context

class UpdatePostView(LoginRequiredMixin, UpdateView):
	form_class = PostUpdateForm
	model = Post
	login_url = reverse_lazy('update_post')
	template_name = 'posts/update_post.html'
	success_url = reverse_lazy('news_page')
	
	def get_success_url(self):
		return self.success_url

class PostDetailView(LoginRequiredMixin,DetailView, CreateView):
	model = Post
	template_name = 'posts/post_detail.html'
	login_url = reverse_lazy('post_detail')
	form_class = CommentPostForm

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.comment_user_id = self.request.user.id
		self.object.comment_post_id= self.kwargs['pk']
		self.object.save()
		return super().form_valid(form)

class MyProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'profile/my_profile.html'
	login_url = reverse_lazy('index')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['profile'] = User.objects.get(id=self.request.user.pk)
		return context

class EditProfileView(LoginRequiredMixin, UpdateView):
	model = User
	template_name = 'profile/edit_profile.html'
	login_url = reverse_lazy('index')
	form_class = MyProfileForm
	success_url = reverse_lazy('my_profile')

	def get_success_url(self):
		return self.success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = self.request.user
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.profile.status = form.cleaned_data.get('status')
		self.object.profile.description = form.cleaned_data.get('description')
		self.object.profile.display_status = form.cleaned_data.get('display_status')
		self.object.save()
		return super().form_valid(form)

class UserProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'profile/user_profile.html'
	login_url = 'index'

	def get_context_data(self, **kwargs):
		
		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		if (self.request.user == User.objects.get(id=kwargs['pk'])):
			return redirect('my_profile')
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
		context['follower'] = Follow.objects.filter(subscriber=self.request.user, signed=User.objects.get(id=kwargs['pk']))
		if Follow.objects.filter(subscriber=self.request.user, signed=User.objects.get(id=kwargs['pk'])):
			followed = True
		else:
			followed = False
		if request.is_ajax():
			return JsonResponse({'followed': followed}, status=200)
		return render(request, 'profile/user_profile.html', context)


	def post(self, request, *args, **kwargs):
		if (request.POST.get('sub') == 'f'):
			Follow.objects.get(subscriber=self.request.user, signed=User.objects.get(id=kwargs['pk'])).delete()
			print(request.POST.get('sub'))
		else:
			Follow.objects.create(subscriber=self.request.user, signed=User.objects.get(id=kwargs['pk']))
			print(request.POST.get('sub'))

		return JsonResponse({}, status=200)