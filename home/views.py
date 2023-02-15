from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
    views['sale_products'] = Product.objects.filter(labels='sale')


class HomeView(BaseView):
    def get(self,request):
        self.views
        self.views['subcategories'] = SubCategory.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['reviews'] = Review.objects.all()
        self.views['new_products'] = Product.objects.filter(labels = 'new')
        self.views['hot_products'] = Product.objects.filter(labels = 'hot')

        return render(request, 'index.html',self.views)


class CategoryView(BaseView):
    def get(self,request,slug):
        ids = Category.objects.get(slug = slug).id
        self.views['category_products'] = Product.objects.filter(category_id = ids)
        return render(request, 'category.html', self.views)

class BrandView(BaseView):
    def get(self,request,slug):
        ids = Brand.objects.get(slug = slug).id
        self.views['brand_products'] = Product.objects.filter(brand_id = ids)
        return render(request, 'brand.html', self.views)

class SearchView(BaseView):
    def get(self,request):
        query = request.GET.get('query')
        if query == "":
            return redirect('/')
        else:
            self.views['search_product'] = Product.objects.filter(description__icontains = query)
        return render(request, 'search.html', self.views)

class ProductDetailView(BaseView):
    def get(self, request, slug):
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

class CartView(BaseView):

    def get(self, request):
        username = request.user.username
        self.views['cart_view'] = Cart.objects.filter(username = username)
        return render(request, 'cart.html', self.views)

def add_to_cart(request, slug):
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
            else:
                messages.error(request, "The quantity is already 1.")

    return redirect('/cart')

def delete_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, checkout=False, username=username).exists():
        Cart.objects.filter(slug=slug, checkout=False, username=username).delete()

    return redirect('/cart')

