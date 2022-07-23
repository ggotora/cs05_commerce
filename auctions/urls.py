from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new_listing", views.new_listing, name="new_listing"),
    path('categories/', views.categories, name="categories"),
    path('categories/<str:category>/category_list', views.category_list, name="category_list"),
    path('add_remove_watchlist/<int:listing_id>', views.add_remove_watchlist, name="add_remove_watchlist"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('close_listing/<int:listing_id>', views.close_listing, name="close_listing"),
    path('close_listing/<int:listing_id>/closed_listing', views.closed_listing, name="closed_listing"),

]



