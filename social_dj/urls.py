from django.urls import path

from . import views

urlpatterns = [
	path('registration/', views.UserRegCreateView.as_view(), name='reg_page'),
	path(r'activate/<id>/<token>',
		views.ActivationView.as_view(), name='activate'),
	path('login/', views.UserLoginView.as_view(), name='login_page'), 
	path('logout/', views.UserLogoutView.as_view(), name='logout'),
	path('news/', views.UserNewsView.as_view(), name='news_page'),
	path('add_post/', views.UserAddPostView.as_view(), name='add_post'),
	path('update/', views.UpdatePostListView.as_view(), name='update_list'),
	path('update/<int:pk>', views.UpdatePostView.as_view(), name='update_add'),
	path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail' ),
	path('myprofile/', views.MyProfileView.as_view(), name='my_profile'),
	path('edit/<int:pk>', views.EditProfileView.as_view(), name='edit'),
	path('user_profile/<int:pk>', views.UserProfileView.as_view(), name='user_profile'),
	path('search_result/', views.SearchResultView.as_view(), name='search_result'),
]