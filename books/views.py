from django.shortcuts import render,redirect

from books.forms import SignUpForm,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from books.models import Product,Basket,BasketItem,Order

# Create your views here.

class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            # data=form_instance.cleaned_data

            # User.objects.create_user(**data)

            print("account created")

            return redirect("signin")

        return render(request,"register.html",{"form":form_instance})

class LogInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            print(user_object)

            if user_object:

                login(request,user_object)

                print("logined successfully")

                return redirect("index")
            
        print("login failed")

        return render(request,"login.html",{"form":form_instance})

class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"index.html",{"data":qs})


class ProductDetailView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)

        return render(request,"product_detail.html",{"data":qs})


# localhost:products/{id}/carts/add/

class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        qty=request.POST.get("qty")

        #basket_obj=Basket.objects.get(owner=request.user)

        Basket_obj=request.user.cart

        Basket_item_objects=BasketItem.objects.filter(Basket_object=Basket_obj,product_object=product_obj,is_order_placed=False)
       
        if Basket_item_objects:

            Basket_item_objects[0].quantity+=int(qty)

            Basket_item_objects[0].save()

        else:
                BasketItem.objects.create(

                         Basket_object=Basket_obj,
                         product_object=product_obj,
                         quantity=qty
                          )

        
        print("product added to cart")
        

        return redirect("index")

class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False)

        return render(request,"cart_list.html",{"data":qs})

class CartDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")


class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):

        action=request.POST.get("action")

        id=kwargs.get("pk")

        basket_item_objects=BasketItem.objects.get(id=id)

        if action=="increment":

            basket_item_objects.quantity+=1

        else:
            basket_item_objects.quantity-=1

        basket_item_objects.save()

        print(action)

        return redirect("cart-summary")

class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
        
    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment_mode")

        user_obj=request.user

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)

        if payment_mode=="cod":
            order_obj=Order.objects.create(
                user_object=user_obj,
                delivery_address=address,
                phone=phone,
                pin=pin,
                email=email,
                payment_mode=payment_mode

            )

            for bi in cart_item_objects:

                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()

            order_obj.save()


        return redirect("index")


class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"order_summary.html",{"data":qs})

class CartDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")


class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):

        action=request.POST.get("action")

        id=kwargs.get("pk")

        basket_item_objects=BasketItem.objects.get(id=id)

        if action=="increment":

            basket_item_objects.quantity+=1

        else:
            basket_item_objects.quantity-=1

        basket_item_objects.save()

        print(action)

        return redirect("cart-summary")

class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
        
    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment_mode")

        user_obj=request.user

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)

        if payment_mode=="cod":
            order_obj=Order.objects.create(
                user_object=user_obj,
                delivery_address=address,
                phone=phone,
                pin=pin,
                email=email,
                payment_mode=payment_mode

            )

            for bi in cart_item_objects:

                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()

            order_obj.save()


        return redirect("index")


class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"order_summary.html",{"data":qs})