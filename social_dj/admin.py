from django.contrib import admin

# Register your models here.wd
from .models import Post, PostComment, UserProfile, Follow
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class FollowAdmin(admin.ModelAdmin):
	list_display = ('subscriber', 'signed')
	list_display_link = ('subscriber_id',)
	


class PostAdmin(admin.ModelAdmin):
	list_display = ('title',)
	list_display_link = ('title',)


class CommentPostAdmin(admin.ModelAdmin):
	list_display = ('comment_user', 'comment_post' )
	list_display_link = ('comment_user',)


class UserInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name = 'Доп информация'

class UserAdmin(UserAdmin):
	inlines = (UserInline, )



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, CommentPostAdmin)
admin.site.register(Follow, FollowAdmin)