from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register.as_view(), name='register'),
    path('login', views.user_login.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.profile.as_view(), name='profile'),
    path('update', views.update_profile, name='update'),
    path('brands/<slug:brand_slug>/', views.home, name='brands'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('buy/<int:id>/', views.buy, name='buy'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),

]
