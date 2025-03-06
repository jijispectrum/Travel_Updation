from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

# def index(request):
#     return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def fyp(request):
    return render(request,'fyp.html')

def service(request):
    return render(request,'service.html')

def login(request):
    return render(request,'login.html')

def recomendations(request):
    return render(request,'recomendations.html')

def contact(request):
    return render(request,'contact.html')

def userdash(request):
    return render(request,'userdash.html')

def favlocation(request):
    return render(request,'favlocation.html')

def recentrecom(request):
    return render(request,'recentrecom.html')

def support(request):
    return render(request,'support.html')

def testimonial(request):
    return render(request,'testimonial.html')

def profile(request):
    return render(request,'profile.html')

def package(request):
    return render(request,'package.html')



#user registration
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirmpassword = request.POST.get('confirm_password', '')

        if not username or not email or not password  or not confirmpassword:
            messages.error(request, 'Please fill all the fields.')
        elif password != confirmpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_view')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login_view')

    return render(request, 'login.html', {'page': 'register'})


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')  # Adjust 'index' to the name of your home page view
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'page': 'login'})

    #Testimonial form
# from .forms import testform
# # from .models import Test
# def testimonial(request):
#         if request.method == 'POST':
#             form = testform(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('testimonial')
#         else:
#             form = testform()
#         return render(request,'review.html',{'form':form})   
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        location = request.POST.get('location', '').strip()
        review = request.POST.get('review', '').strip()

        # Validate fields
        if not all([name, email, location, review]):
            messages.error(request, 'Please fill all the fields.')
        else:
            try:
                validate_email(email)
                # Save to database
                Test.objects.create(name=name, email=email, location=location, review=review)
                messages.success(request, 'Review submitted successfully.')
                return redirect('contact')
            except ValidationError:
                messages.error(request, 'Invalid email address.')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')

    return render(request, 'index.html')

# from django.shortcuts import render, redirect
# from .forms import TourPreferenceForm

# def filter_tours(request):
#     if request.method == 'POST':
#         form = TourPreferenceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Filters applied successfully!')
#             return redirect('recomendations')  # Adjust this if needed
#     else:
#         form = TourPreferenceForm()
    
#     return render(request, 'recomendations.html', {'form': form})

from django.shortcuts import render
from .models import Destination
from django.db.models import Q
# from . models import Accommodation
from django.shortcuts import render
from django.db.models import Q
from .models import Destination

def search_destinations(request):
    query = request.GET.get('query', '').strip().lower()  # Normalize query
    destinations = Destination.objects.all()  # Default: Show all destinations

    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(state__icontains=query) |
            Q(country__icontains=query)
        )

    return render(request, 'search.html', {'destinations': destinations, 'query': query})

from django.shortcuts import render
from .models import Destination

# def filter_destinations(request):
#     destinations = Destination.objects.all()

#     # Get filter values from the request
#     tour_type = request.GET.get('tour_type')
#     accommodation_type = request.GET.get('accommodation_type')
#     state = request.GET.get('state')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     # Apply filters
#     if tour_type:
#         destinations = destinations.filter(tour_type=tour_type)

#     if accommodation_type:
#         destinations = destinations.filter(accommodation_type=accommodation_type)

#     if state:
#         destinations = destinations.filter(state__icontains=state)

#     if min_price and max_price:
#         destinations = destinations.filter(price__gte=min_price, price__lte=max_price)

#     return render(request, 'recomm.html', {'destinations': destinations})
from django.shortcuts import render
from .models import Destination
from django.shortcuts import render
from .models import Destination

def filter_destinations(request):
    destinations = None  # Initially no results

    # Get filter values from request
    tour_type = request.GET.get('tour_type')
    accommodation_type = request.GET.get('accommodation_type')
    state = request.GET.get('state')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    max_days = request.GET.get('max_days')  # Keep only max_days
    interest = request.GET.get('interest')
    min_distance = request.GET.get('min_distance')
    max_distance = request.GET.get('max_distance')

    # Check if any filter is applied
    if any([tour_type, accommodation_type, state, min_price, max_price, max_days, interest, min_distance, max_distance]):
        destinations = Destination.objects.all()

        # Apply filters
        if tour_type:
            destinations = destinations.filter(tour_type=tour_type)

        if accommodation_type:
            destinations = destinations.filter(accommodation_type=accommodation_type)

        if state:
            destinations = destinations.filter(state__icontains=state)

        if min_price and max_price:
            destinations = destinations.filter(price__gte=min_price, price__lte=max_price)

        if max_days:
            destinations = destinations.filter(duration__lte=max_days)

        if interest:
            destinations = destinations.filter(interest__icontains=interest)

        if min_distance and max_distance:
            destinations = destinations.filter(distance__gte=min_distance, distance__lte=max_distance)

    return render(request, 'recomm.html', {'destinations': destinations})
