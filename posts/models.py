from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Post(models.Model):
	title = models.CharField(_("title"), max_length=100)
	short_description = models.CharField(_("short description"), max_length=200)
	image = models.URLField(max_length = 200)
	full_description = models.TextField(_("full description"), blank = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	posted = models.BooleanField(_('posted'), default=False)


class Comment(models.Model):
	username = models.CharField(_("username"), max_length=100)
	text = models.CharField(_("text"), max_length=300)
	post = models.ForeignKey("Post", on_delete=models.SET_NULL, null=True)
