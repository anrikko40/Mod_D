from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat*3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('category name'))
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    #category = models.ForeignKey(
        #to='Category',
        #on_delete=models.CASCADE,
        #related_name='posts')
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.description[0:124] + '...'

    def __str__(self):
        return f'{self.name}: {self.description[:20]}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    verbose_name = pgettext_lazy('help text for MyModel model', 'This is the help text'),



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete = models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete = models.CASCADE)
    pass

class Comment(models.Model):
    postComment = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    commentTime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
