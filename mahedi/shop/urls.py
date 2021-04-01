from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path('logout/',views.user_logout,name='user_logout'),
    path('login/',views.user_login,name='user_login'),
    path('register/',views.user_register,name='user_register'),
    path('profile/',views.user_profile,name='user_profile'),
    path('user_update/',views.user_update,name='user_update'),
    path('user_password/',views.user_password,name='user_password'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path("paytm/", views.paytm, name="HandleRequest"),
]
