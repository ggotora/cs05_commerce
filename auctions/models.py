from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    def watchlist_count(self):
        return self.watchlist.count()

class Listing(models.Model):
    CATEGORIES = (
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(choices=CATEGORIES, max_length=30)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, default=None, related_name='watchlist')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
        
    def current_price(self):
        return self.bid_set.all().aggregate(Max('price'))['price__max']

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid {self.price}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content 


