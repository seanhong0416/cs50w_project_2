from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to="items")
    description = models.CharField(max_length=128)
    type = models.CharField(max_length=16)
    starting_bid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_selling_items")
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Item No.{self.id}:{self.title} by {self.owner.username}"

class Bids(models.Model):
    item = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bidding_items")

    def __str__(self):
        return f"{self.item}, Bid:{self.price} dollars, Bidder:{self.bidder.username}"

class Comments(models.Model):
    item = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comments")
    content = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.item}, Comment:{self.content}, Commenter:{self.commenter.username}"