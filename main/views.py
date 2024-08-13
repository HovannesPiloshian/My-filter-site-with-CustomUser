from django.shortcuts import render, redirect
from .models import Color, Tent, Cart
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    # Get the list of all colors and distinct materials
    color_list = Color.objects.all()
    materials = Tent.objects.values_list('material', flat=True).distinct()

    # Initialize the tent query set
    tent_list = Tent.objects.all()

    # Check if the form has been submitted via POST
    if request.method == 'POST':
        color_id = request.POST.get('color_id')
        tent_name = request.POST.get('tent_name')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        price = request.POST.get('price')
        capacity = request.POST.get('capacity')

        # Filter by color_id if provided
        if color_id:
            tent_list = tent_list.filter(color=color_id)

        # Filter by tent_name if provided
        if tent_name:
            tent_list = tent_list.filter(name__iexact=tent_name)

        # Filter by weight if provided
        if weight:
            tent_list = tent_list.filter(weight__lte=weight)

        # Filter by height if provided
        if height:
            tent_list = tent_list.filter(height__lte=height)

        # Filter by price if provided
        if price:
            tent_list = tent_list.filter(price__lte=price)

        # Filter by capacity if provided
        if capacity:
            tent_list = tent_list.filter(capacity__gte=capacity)

    return render(request, 'index.html', context={
        'tent_list': tent_list,
        'color_list': color_list,
        'materials': materials
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def view_cart(request):
    cart_list = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_list': cart_list})

def add_to_cart(request, tent_id):
    try:
        tent = Tent.objects.get(id=tent_id)
        Cart.objects.create(user=request.user, tent=tent)
    except Tent.DoesNotExist:
        # Handle the case where the tent does not exist
        pass
    return redirect('index')
