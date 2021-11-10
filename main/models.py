
from django.db import models

# from user.models import User


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    # children для того, чтобы можно было вытащить все подкатегории какой-нибудь категории

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name


class News(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    created = models.DateTimeField()

    def __str__(self):
        return self.title

    # @property
    # def get_image(self):
    #     return self.images.first()
    #
    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('detail', kwargs={'pk': self.pk})


class Image(models.Model):
    image = models.ImageField(upload_to='recipes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        if self.image:
            return self.image.url
        return ''
