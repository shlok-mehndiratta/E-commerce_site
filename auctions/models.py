from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=30)

    def __str__(self):
        return self.categoryName


class Bids(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="biduser")
    listing = models.ForeignKey('Listings', on_delete=models.CASCADE, related_name="bids", null=True, blank=True)


    def __str__(self):
        return f'{self.bid}'


class Listings(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    price = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="userbid")
    imageUrl = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userwatchlist")

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='usercomment')
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name='listingcomment')
    message = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.author} comment on {self.listing}'
    