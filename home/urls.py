from .views import *
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('brand/<slug>', BrandView.as_view(), name='brand'),
    path('search', SearchView.as_view(), name='search'),
    path('product_detail/<slug>', ProductDetailView.as_view(), name='product_detail'),
    path('signup', signup, name='signup'),
    path('product_review/<slug>', product_review, name='product_review'),
    path('cart', CartView.as_view(), name='cart'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('increase_cart_quantity/<slug>', increase_cart_quantity, name='increase_cart_quantity'),
    path('increase_cart_quantity_product_detail/<slug>', increase_cart_quantity_product_detail, name='increase_cart_quantity_product_detail'),
    path('reduce_quantity/<slug>', reduce_quantity, name='reduce_quantity'),
    path('reduce_quantity_product_detail/<slug>', reduce_quantity_product_detail, name='reduce_quantity_product_detail'),
    path('delete_cart/<slug>', delete_cart, name='delete_cart'),
    path('wishlist', WishlistView.as_view(), name='wishlist'),
    path('add_to_wishlist/<slug>', add_to_wishlist, name='add_to_wishlist'),
    path('add_wishlist_to_cart/<slug>', add_wishlist_to_cart, name='add_wishlist_to_cart'),
    path('delete_wishlist/<slug>', delete_wishlist, name='delete_wishlist'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('newsletters', newsletters, name='newsletters'),
    # path('place_order', placeorder, name='placeorder'),

]


