from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
	title = models.CharField(max_length=30,
							verbose_name='Название')
	description = models.TextField(verbose_name='Описание')
	user = models.ForeignKey(User,on_delete=models.PROTECT,
								verbose_name='Пользователь')
	image = models.ImageField(upload_to='images/',
							 default='static/images/None.jpg',
							 height_field=None,
							 width_field=None,
							 null=False, blank=False)
	published = models.DateTimeField(default=timezone.now)
	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		ordering = ['-published']

	def __str__(self):
		return self.title


class PostComment(models.Model):
	text = models.CharField(max_length=150)
	comment_user = models.ForeignKey(User,
									on_delete=models.PROTECT,
									verbose_name='Пользователь',)
	comment_post = models.ForeignKey(Post, 
									on_delete=models.PROTECT,
									verbose_name='Новость',
									related_name='post_comment')
	sub_comments = models.ForeignKey('self',
									on_delete=models.CASCADE,
									related_name='subcomment',
									null=True, blank=True,
									verbose_name='Под-комментарий')
	published = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'

	def get_absolute_url(self):
		return reverse_lazy('post_detail',kwargs={'pk':self.comment_post.pk})


class UserProfile(models.Model):
	user = models.OneToOneField(User, 
								on_delete=models.CASCADE, 
								related_name='profile',)
	status = models.CharField(max_length=50, 
							  null=True, 
							  blank=True,
							  verbose_name='Статус')
	display_status = models.BooleanField(default=True)

	description = models.TextField(null=True, 
								   blank=True,
								   verbose_name='О себе')
	subscribes = models.ManyToManyField("self", through="Follow")

	def  __str__(self):
		return self.user.username

	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

class Follow(models.Model):
	subscriber = models.ForeignKey(User,on_delete=models.CASCADE, related_name="subscriber")
	signed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="signed")
	date_followed = models.DateField(auto_now=True)

	def __str__(self):
		return self.subscriber.username + " follows " + self.signed.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

  	