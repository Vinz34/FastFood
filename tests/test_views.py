from django.test import TestCase
from restaurants.models import Burger, Restaurant
from django.urls import reverse
from django.test import RequestFactory, TestCase
from django.views import View
from django.http import HttpResponse


class TestRestaurant(TestCase):

    def test_no_restaurants(self):
        """
            If no restaurants exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('home_page:global_restaurant'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No restaurants are available.")
        self.assertQuerysetEqual(response.context['restaurants'], map(repr, []))

    def test_restaurants(self):
        """
            Restaurants are displayed on the global restaurant page.
        """
        new_resto = Restaurant(restaurant_name="Test Resto", location="a", phone_number="45", open="True")
        new_resto.save(new_resto)
        response = self.client.get(reverse('home_page:global_restaurant'))
        self.assertQuerysetEqual(
            response.context['restaurants'],
            [new_resto],
        )


class DummyView(View):
    def add_burger(self):
        new_resto = Restaurant(restaurant_name="Test Resto", location="a", phone_number="45", open="True")
        new_resto.save(new_resto)
        # Create a new burger instance
        burger = Burger.objects.create(restaurant=new_resto,name="Cheeseburger", price=9.99,
                                       description="Juicy beef patty topped with melted cheese.")

        # Return a success message
        return HttpResponse("Burger added successfully.")


class DummyViewTestCase(TestCase):
    def test_add_burger(self):
        view = DummyView()

        response = view.add_burger()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Burger added successfully.")

