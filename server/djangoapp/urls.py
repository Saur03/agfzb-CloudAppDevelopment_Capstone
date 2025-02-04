from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import static_template_view, about_us_view, contact_us_view, login_view, logout_view, signup_view
from .views import get_dealerships

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('static-template/', static_template_view, name='static_template'),
    # Add more URL patterns if needed


    # path for about view
    path('about/', about_us_view, name='about_us'),

    # path for contact us view
    path('contact/', contact_us_view, name='contact_us'),

    # path for registration
    path('signup/', signup_view, name='signup'),

    # path for login
    path('login/', login_view, name='login'),

    # path for logout
    path('logout/', logout_view, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),
    

    path('get_dealerships/', get_dealerships, name='get_dealerships'),

    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),


    # path for dealer reviews view


    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



