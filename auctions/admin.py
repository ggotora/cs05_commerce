from django.contrib import admin

from auctions.models import Comment, Listing, Bid, User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Comment)
