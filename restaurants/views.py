import app as app
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.shortcuts import render
from restaurants.forms import BurgerForm, RestaurantForm


from django.http import HttpResponse
from django.template import loader

from .models import Restaurant, Burger


# Define a view function named index that takes an HTTP request object as its argument
def index(request):
    # Query the database for all Restaurant objects and order them in descending order by name
    longer_restaurant_list = Restaurant.objects.order_by('-restaurant_name')

    # Load the index.html template
    template = loader.get_template('restaurants/templates/index.html')

    # Create a dictionary named context containing the longer_restaurant_list
    context = {'longer_restaurant_list': longer_restaurant_list, }

    # Render the index.html template with the context dictionary as its context
    # and return the rendered template as an HTTP response
    return render(request, 'restaurants/templates/index.html', context)


# Define a view function named settings that takes an HTTP request object as its argument
def settings(request):
    # Render the settings.html template and return it as an HTTP response
    return render(request, 'restaurants/settings.html')


# Define a view function named global_restaurant that takes an HTTP request object as its argument
def global_restaurant(request):
    # Try to retrieve all Restaurant objects from the database
    try:
        restaurant = Restaurant.objects.all()
    except Restaurant.DoesNotExist:
        # If no Restaurants are found, raise an HTTP 404 error
        raise Http404("No restaurants available.")

    # Render the global_restaurant.html template with the 'restaurant' QuerySet passed as context
    return render(request, 'restaurants/global_restaurant.html', {'restaurants': restaurant})


# Define a view function named detail_restaurant that takes an HTTP request object and a restaurant_id as arguments
def detail_restaurant(request, restaurant_id):
    # Try to retrieve the Restaurant object with the specified restaurant_id from the database
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        # If no Restaurant is found, raise an HTTP 404 error
        raise Http404("This restaurant doesn't exist.")

    # Render the detail_restaurant.html template with the 'restaurant' and 'burgers' QuerySets passed as context
    # 'burgers' contains all Burger objects
    return render(request, 'restaurants/detail_restaurant.html',
                  {'restaurant': restaurant, 'burgers': Burger.objects.all})


# Define a view function named add_burger that takes an HTTP request object as its argument
def add_burger(request):
    # If the HTTP request method is POST, try to validate the submitted form data
    if request.method == 'POST':
        form = BurgerForm(request.POST)
        if form.is_valid():
            # If the form data is valid, save the new burger to the database
            burger = form.save()

            # Check for duplicate burgers (same name, description, and restaurant), and delete the new one if found
            for bur in Burger.objects.all():
                if burger.restaurant == bur.restaurant and burger.name == bur.name and \
                        burger.description == bur.description and burger.id != bur.id:
                    burger.delete()

                    # If a duplicate is found, render the add_burger.html template with an error message
                    return render(request, 'restaurants/add_burger.html',
                                  {'form': form, 'error': "There is already a burger with this name."})

            # If no duplicate burgers are found, redirect to the detail view of the new burger's restaurant
            return redirect('../../restaurants/' + str(burger.restaurant.id))
    else:
        # If the HTTP request method is not POST, create a new, empty BurgerForm
        form = BurgerForm()

    # Render the add_burger.html template with the BurgerForm passed as context
    return render(request, 'restaurants/add_burger.html', {'form': form})


# Define a view function named add_restaurant that takes an HTTP request object as its argument
def add_restaurant(request):
    # If the HTTP request method is POST, try to validate the submitted form data
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            # If the form data is valid, save the new restaurant to the database
            restaurant = form.save()

            # Check for duplicate restaurants (same name, location, and phone number), and delete the new one if found
            for rest in Restaurant.objects.all():
                if restaurant.restaurant_name == rest.restaurant_name and restaurant.location == rest.location and \
                        restaurant.phone_number == rest.phone_number and restaurant.id != rest.id:
                    restaurant.delete()

                    # If a duplicate is found, render the add_restaurant.html template with an error message
                    return render(request, 'restaurants/add_restaurant.html',
                                  {'form': form, 'error': "There is already a restaurant with this name."})

            # If no duplicate restaurants are found, redirect to the index view for all restaurants
            return redirect('../../restaurants/')
    else:
        # If the HTTP request method is not POST, create a new, empty RestaurantForm
        form = RestaurantForm()

    # Render the add_restaurant.html template with the RestaurantForm passed as context
    return render(request, 'restaurants/add_restaurant.html', {'form': form})


# Define a view function named remove_burger that takes an HTTP request object, a restaurant ID, and a burger ID as
# its arguments
def remove_burger(request, restaurant_id, burger_id):
    # Retrieve the Burger object with the given burger ID
    burger = Burger.objects.get(pk=burger_id)

    # If the HTTP request method is POST, delete the Burger object from the database and redirect to the index view
    # for all restaurants
    if request.method == 'POST':
        burger.delete()
        return redirect('../../')

    # If the HTTP request method is not POST, render the remove_burger.html template with the Burger object passed as
    # context
    return render(request, 'restaurants/remove_burger.html', {'burger': burger})


# Define a view function named remove_restaurant that takes an HTTP request object and a restaurant ID as its arguments
def remove_restaurant(request, restaurant_id):
    # Retrieve the Restaurant object with the given restaurant ID
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    # If the HTTP request method is POST, delete the Restaurant object from the database and redirect to the index
    # view for all restaurants
    if request.method == 'POST':
        restaurant.delete()
        return redirect('../../')

    # If the HTTP request method is not POST, render the remove_restaurant.html template with the Restaurant object
    # passed as context
    return render(request, 'restaurants/remove_restaurant.html', {'restaurant': restaurant})


# Define a view function named update_burger that takes an HTTP request object, a restaurant ID, and a burger ID as
# its arguments
def update_burger(request, restaurant_id, burger_id):
    # Retrieve the Burger object with the given burger ID
    burger = Burger.objects.get(pk=burger_id)

    # If the HTTP request method is POST, update the Burger object with the submitted form data and redirect to the
    # index view for all burgers
    if request.method == 'POST':
        form = BurgerForm(request.POST, instance=burger)
        if form.is_valid():
            # Update the existing Burger object in the database with the submitted form data
            form.save()
            # Redirect to the index view for all burgers with the ID of the updated burger as a URL parameter
            return redirect('../../', burger.id)
    else:
        # If the HTTP request method is not POST, render the update_burger.html template with the Burger object and
        # form passed as context
        form = BurgerForm(instance=burger)

    return render(request, 'restaurants/update_burger.html', {'burger': burger, 'form': form})


def update_restaurant(request, restaurant_id):
    # get the restaurant object from the database using the restaurant_id parameter
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    # check if the request method is POST
    if request.method == 'POST':
        # create a form object and populate it with data from the request
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            # save the updated restaurant object to the database
            form.save()
            # redirect to the updated restaurant's detail page
            return redirect('../../', restaurant.id)
    else:
        # create a form object and populate it with the current values from the restaurant object
        form = RestaurantForm(instance=restaurant)

    # render the update_restaurant template with the form object as context
    return render(request, 'restaurants/update_restaurant.html', {'form': form})
