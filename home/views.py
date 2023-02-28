from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import random
# Create your views here.

def count_cart(request):
    username = request.user.username
    cart_count = Cart.objects.filter(checkout = False, username = username).count()
    return cart_count



def count_wishlist(request):
    username = request.user.username
    wishlist_count = Wishlist.objects.filter(username = username).count()
    return wishlist_count
class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
    views['sale_products'] = Product.objects.filter(labels='sale')


class HomeView(BaseView):
    def get(self,request):
        self.views
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        self.views['subcategories'] = SubCategory.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['reviews'] = Review.objects.all()
        self.views['new_products'] = Product.objects.filter(labels = 'new')
        self.views['hot_products'] = Product.objects.filter(labels = 'hot')

        return render(request, 'index.html',self.views)


class CategoryView(BaseView):
    def get(self,request,slug):
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        ids = Category.objects.get(slug = slug).id
        self.views['category_products'] = Product.objects.filter(category_id = ids)
        return render(request, 'category.html', self.views)

class BrandView(BaseView):
    def get(self,request,slug):
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        ids = Brand.objects.get(slug = slug).id
        self.views['brand_products'] = Product.objects.filter(brand_id = ids)
        return render(request, 'brand.html', self.views)

class SearchView(BaseView):
    def get(self,request):
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        query = request.GET.get('query')
        if query == "":
            return redirect('/')
        else:
            self.views['search_product'] = Product.objects.filter(description__icontains = query)
        return render(request, 'search.html', self.views)

class ProductDetailView(BaseView):
    def get(self, request, slug):
        self.views['count_review'] = ProductReview.objects.filter(slug = slug).count()
        username = request.user.username
        self.views['cart_view'] = Cart.objects.filter(username = username, checkout = False, slug=slug)
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        # for particular product detail
        self.views['product_detail'] = Product.objects.filter(slug = slug)
        # for related product
        subcat_id = Product.objects.get(slug=slug).subcategory_id
        self.views['related_products'] = Product.objects.filter(subcategory_id = subcat_id)
        # for multiple images view
        products_id = Product.objects.get(slug=slug).id
        self.views['product_images'] = ProductImage.objects.filter(product_id=products_id)
        self.views['product_reviews'] = ProductReview.objects.filter(slug = slug)
        return render(request, 'product-detail.html', self.views)


class CartView(BaseView):

    def get(self, request):
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        username = request.user.username
        self.views['cart_view'] = Cart.objects.filter(username = username, checkout = False)
        s = 0
        for i in self.views['cart_view']:
            s = s + i.total
        self.views['sub_total'] = s
        self.views['delivery_charge'] = 50
        self.views['Grand_total'] = s + 50
        return render(request, 'cart.html', self.views)

def product_review(request, slug):

    if request.method == 'POST':
        username = request.user.username
        email = request.user.email
        star = request.POST['star']
        comment = request.POST['comment']
        data = ProductReview.objects.create(
            name = username,
            email = email,
            star = star,
            comment = comment,
            slug = slug
        )
        data.save()
        messages.success(request, 'The review is submitted successfully!')
    return redirect(f'/product_detail/{slug}')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'This username is already taken!')
                return redirect('/signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'This email is already registered!')
                return redirect('/signup')
            else:
                data = User.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password
                )
                data.save()
        else:
            messages.error(request, 'Entered password doesnot match!')
            return redirect('/signup')
    return render(request,'signup.html')



def add_to_cart(request, slug):
    if request.user.is_authenticated:
        username = request.user.username
        if Product.objects.filter(slug = slug).exists():
            if Cart.objects.filter(slug =slug, checkout = False, username = username).exists():
                quantity = Cart.objects.get(slug =slug, checkout = False, username = username).quantity
                price = Product.objects.get(slug=slug).price
                discounted_price = Product.objects.get(slug=slug).discounted_price
                quantity = quantity + 1
                if discounted_price > 0:
                    total = discounted_price*quantity
                else:
                    total = price*quantity
                Cart.objects.filter(slug=slug, checkout=False, username=username).update(total = total, quantity = quantity)
            else:
                price = Product.objects.get(slug=slug).price
                discounted_price = Product.objects.get(slug=slug).discounted_price
                if discounted_price > 0:
                    total = discounted_price
                else:
                    total = price
                data = Cart.objects.create(
                    username = username,
                    slug = slug,
                    quantity = 1,
                    total = total,
                    items = Product.objects.get(slug=slug)
                )
                data.save()
                messages.success(request, "Product successfully added to cart!")
    else:
        messages.error(request, "Please login before to proceed...")
        return redirect('/')
    return redirect('/')


# Increase quantity from cart page
def increase_cart_quantity(request, slug):
    username = request.user.username
    if Product.objects.filter(slug = slug).exists():
        if Cart.objects.filter(slug =slug, checkout = False, username = username).exists():
            quantity = Cart.objects.get(slug =slug, checkout = False, username = username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            quantity = quantity + 1
            if discounted_price > 0:
                total = discounted_price*quantity
            else:
                total = price*quantity
            Cart.objects.filter(slug=slug, checkout=False, username=username).update(total = total, quantity = quantity)
        else:
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if discounted_price > 0:
                total = discounted_price
            else:
                total = price
            data = Cart.objects.create(
                username = username,
                slug = slug,
                quantity = 1,
                total = total,
                items = Product.objects.get(slug=slug)
            )
            data.save()
    else:
        return redirect('/')
    return redirect('/cart')

# Increase quantity from detail_product page
def increase_cart_quantity_product_detail(request, slug):
    username = request.user.username
    if Product.objects.filter(slug = slug).exists():
        if Cart.objects.filter(slug =slug, checkout = False, username = username).exists():
            quantity = Cart.objects.get(slug =slug, checkout = False, username = username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            quantity = quantity + 1
            if discounted_price > 0:
                total = discounted_price*quantity
            else:
                total = price*quantity
            Cart.objects.filter(slug=slug, checkout=False, username=username).update(total = total, quantity = quantity)
        else:
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if discounted_price > 0:
                total = discounted_price
            else:
                total = price
            data = Cart.objects.create(
                username = username,
                slug = slug,
                quantity = 1,
                total = total,
                items = Product.objects.get(slug=slug)
            )
            data.save()
    else:
        return redirect('/')
    return redirect(f'/product_detail/{slug}')


# Reduce quantity from Cart page
def reduce_quantity(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Cart.objects.filter(slug=slug, checkout=False, username=username).exists():
            quantity = Cart.objects.get(slug=slug, checkout=False, username=username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if quantity > 1:
                quantity = quantity - 1
                if discounted_price > 0:
                    total = discounted_price * quantity
                else:
                    total = price * quantity
                Cart.objects.filter(slug=slug, checkout=False, username=username).update(total=total, quantity=quantity)
                # messages.success(request, "Product quantity deducted successfully.")
            else:
                messages.error(request, "The quantity is already 1.")

    return redirect('/cart')


# Reduce quantity from Product detail page
def reduce_quantity_product_detail(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Cart.objects.filter(slug=slug, checkout=False, username=username).exists():
            quantity = Cart.objects.get(slug=slug, checkout=False, username=username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if quantity > 1:
                quantity = quantity - 1
                if discounted_price > 0:
                    total = discounted_price * quantity
                else:
                    total = price * quantity
                Cart.objects.filter(slug=slug, checkout=False, username=username).update(total=total, quantity=quantity)
                # messages.success(request, "Product quantity deducted successfully.")
            else:
                messages.error(request, "The quantity is already 1.")
                return redirect(f'/product_detail/{slug}')



def delete_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, checkout=False, username=username).exists():
        Cart.objects.filter(slug=slug, checkout=False, username=username).delete()

    return redirect('/cart')

class WishlistView(BaseView):

    def get(self, request):
        username = request.user.username
        self.views['wishlist_views'] = Wishlist.objects.filter(username = username)
        self.views['wishtlist_count'] = count_wishlist(request)
        self.views['cart_counts'] = count_cart(request)
        return render(request, 'wishlist.html', self.views)


def add_to_wishlist(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Wishlist.objects.filter(slug=slug, username=username).exists():
            messages.error(request, "This product is already added to your wishlist!")
        else:
            data = Wishlist.objects.create(
                username=username,
                slug=slug,
                items=Product.objects.get(slug=slug)
            )
            data.save()
            messages.success(request, "Product successfully added to Wishlist!")
    return redirect('/')


def add_wishlist_to_cart(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Cart.objects.filter(slug=slug, checkout=False, username=username).exists():
            quantity = Cart.objects.get(slug=slug, checkout=False, username=username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            quantity = quantity + 1
            if discounted_price > 0:
                total = discounted_price * quantity
            else:
                total = price * quantity
            Cart.objects.filter(slug=slug, checkout=False, username=username).update(total=total, quantity=quantity)
        else:
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if discounted_price > 0:
                total = discounted_price
            else:
                total = price
            data = Cart.objects.create(
                username=username,
                slug=slug,
                quantity=1,
                total=total,
                items=Product.objects.get(slug=slug)
            )
            data.save()
            Wishlist.objects.filter(slug=slug, username=username).delete()
            messages.success(request, "Product successfully added to cart!")


    return redirect('/wishlist')
def delete_wishlist(request, slug):
    username = request.user.username
    if Wishlist.objects.filter(slug=slug, username=username).exists():
        Wishlist.objects.filter(slug=slug, username=username).delete()

    return redirect('/wishlist')


def newsletters(request):
    if request.method == "POST":
        email = request.POST['email']
        if Newsletter.objects.filter(email=email).exists():
            messages.error(request, 'This Email is already submitted!')
        else:
            data = Newsletter.objects.create(
                email = email
            )
            data.save()
            messages.success(request, 'Thanks for submitted your Email!')
    return redirect('/')


class CheckoutView(BaseView):
    def get(self, request):
        self.views['cart_counts'] = count_cart(request)
        self.views['wishtlist_count'] = count_wishlist(request)
        username = request.user.username
        self.views['cart_view'] = Cart.objects.filter(username=username, checkout=False)
        total_price = 0
        for item in self.views['cart_view']:
            total_price = total_price + item.total
        self.views['delivery_charge'] = 50
        self.views['Grand_total'] = total_price + 50
        # self.views = {'cartitems': self.views['cart_view'], 'total_price': total_price}

        return render(request, 'checkout.html', self.views)

#
#
# # def checkout(request):
# #     cartitems = Cart.objects.filter(user = request.user)
# #     total_price = 0
# #     for item in cartitems:
# #         if item.discounted_price > 0:
# #             total_price = total_price + item.discounted_price * item.quantity
# #         else:
# #             total_price = total_price + item.price * item.quantity
# #         context = {'cartitems': cartitems, 'total_price':total_price}
# #
# #         return render(request, 'checkout.html', context)
#
# # @login_required(login_url='loginpage')
# def placeorder(request):
#     if request.method == 'POST':
#         user = request.user.username
#         first_name = request.POST['fname']
#         last_name = request.POST['lname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         address = request.POST['address']
#         country = request.POST['country']
#         city = request.POST['city']
#         state = request.POST['state']
#         zip_code = request.POST['zip_code']
#         payment_mode = request.POST['payment_mode']
#         cart = Cart.objects.filter(user=request.user)
#         cart_total_price = 0
#         for item in cart:
#             if item.product.discounted_price > 0:
#                 cart_total_price = cart_total_price + item.product.discounted_price * item.quantity
#             else:
#                 cart_total_price = cart_total_price + item.product.price * item.quantity
#         trackno = 'shrestha'+str(random.randint(1111111,9999999))
#         while Order.objects.filter(traking_no=trackno) is None:
#             trackno = 'shrestha' + str(random.randint(1111111, 9999999))
#
#         data = Order.objects.create(
#             user=user,
#             first_name = first_name,
#             last_name = last_name,
#             email=email,
#             phone=phone,
#             address=address,
#             country=country,
#             city=city,
#             state=state,
#             zip_code=zip_code,
#             payment_mode=payment_mode,
#             total_price = cart_total_price,
#             tracking_no=trackno
#         )
#         data.save()
#
#         neworderitems = Cart.objects.filter(user=request.user)
#         for item in neworderitems:
#             OrderItem.objects.create(
#                 order=data,
#                 product=item.product,
#                 price=cart_total_price,
#                 quantity=item.quantity
#             )
#
#             # # To decrease the product quantity from available stock
#             # orderproduct = Product.objects.filter(id=item.product_id).first()
#             # orderproduct.quantity =
#
#             Cart.objects.filter(user=request.user).delete()
#         messages.success(request, 'Your order has been placed successfully!')
#
#     return  redirect('/')
