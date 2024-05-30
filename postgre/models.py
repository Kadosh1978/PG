from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        commets_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        print(posts_rating)
        print('------------')
        print(commets_rating)
        print('------------')
        print(posts_comments_rating)

        self.rating = posts_rating * 3 + commets_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    category_type = models.CharField(max_length = 255, unique = True)

    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.category_type
        
        
    

class Post(models.Model):
    news = 'NE'
    articles = 'AR'
    POSITIONS = [
        (news, "Новость"),
        (articles, "Статья"),
    ]
    time_in = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    head = models.CharField(max_length = 255, unique = True)
    text = models.TextField()
    category = models.ManyToManyField(Category, through="PostCategory")
    rating = models.IntegerField(default=0)
    post_type = models.CharField(max_length = 2, choices=POSITIONS, default=news)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'
    
    def __str__(self):
        return f'Заголовок: {self.head.title()}: Дата публикации: {self.time_in}: Текст статьи:{self.text}'
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()