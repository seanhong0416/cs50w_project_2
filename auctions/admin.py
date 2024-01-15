from django.contrib import admin

from .models import User, AuctionList, Bids, Comments, WatchList

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionList)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(WatchList)
