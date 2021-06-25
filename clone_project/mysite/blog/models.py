from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    # we can see timezone in settings.property
    # we add whatever timezone we need
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # Post can have some comments.
    def approve_comments(self):
        return self.comments.filter(approved_comment = True)

    def get_absolute_url(self):
        # after creating a post where should website takes them here
        return reverse('post_detail',kwargs={'pk': self.pk})

    #for model string representation
    def __str__(self):
        return self.title

class Comment(models.Model):
    # each comment will connect blog App
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=200)
    # for the approved comment date and time
    create_date = models.DateTimeField(default=timezone.now)
    # its for comment process and it is a BooleanField
    approved_comment = models.BooleanField(default=False)

    #approve method
    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        # it gives list view
        return reverse('post_list')

    def __str__(self):
        return self.text
