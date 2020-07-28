from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import *
from .decorators import *


# Create your views here.
@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('succesfully authenticated user' + request.POST.get('username'))
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is Incorrect')

    context = {

    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("form Valid", request.POST)
            user = form.save()
            # we will also assign group using signals
            # group = Group.objects.get(name='customers')
            # we will use django signals instead  of this
            # Customer.objects.create(user=user,name=user.username)
            username = form.cleaned_data.get('username')
            # user.groups.add(group)
            messages.success(request, 'Account has been created for ' + username)
            return redirect('login')

        print("form is invalid", request.POST)

    context = {
        'form': form
        
    }
    return render(request, 'accounts/registration.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def user_view(request):
    orders = request.user.customer.orders_set.all()
    print("user group: ", request.user.groups.all())
    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'orders_delivered': orders.filter(Status='delivered').count(),
        'orders_pending': orders.filter(Status='pending').count(),
        'role': request.user.groups.all()[0].name
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def account_settings(request):
    user = request.user
    form = CustomerForm(instance=user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            redirect('settings')
    context = {
        'form': form
    }
    return render(request, 'accounts/accounts_settings.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    context = {
        'customers': Customer.objects.all(),
        'orders': Orders.objects.all(),
        'total_orders': Orders.objects.count(),
        'orders_delivered': Orders.objects.filter(Status='delivered').count(),
        'orders_pending': Orders.objects.filter(Status='pending').count()
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def products(request):
    context = {
        'products': Products.objects.all()
    }

    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def customers(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = customer.orders_set.all()
    total_order = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_order': total_order
    }

    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def create_order(request, customer_id):
    OrderFormSet = inlineformset_factory(Customer, Orders, fields=('products', 'Status'), extra=5)
    customer = Customer.objects.get(id=customer_id)
    formset = OrderFormSet(queryset=Orders.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    context = {
        'formset': formset
    }
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        # check if the form data is valid
        if formset.is_valid():
            formset.save()
            return redirect('home')
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def update_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    # set from instance with previous values
    form = OrderForm(instance=order)
    # update form with the given new values
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        # check if the form data is valid
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def delete_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()

        return redirect('home')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def add_product(request):
    # OrderFormSet = inlineformset_factory(Products, extra=5)
    formset = AddProductForm()

    if request.method == 'POST':
        formset = AddProductForm(request.POST)
        # check if the form data is valid
        if formset.is_valid():
            formset.save()
            return redirect('products')

    context = {
        'formset': formset
    }
    return render(request, 'accounts/add_product.html', context)
