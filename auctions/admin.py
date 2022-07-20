from django.contrib import admin

from auctions.models import Comment, Listing, Bid

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
