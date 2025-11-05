from .forms import CommentForm
from .models import Car
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .import forms
from .import models
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.

def contact(req):
    return render(req, 'contact.html')


def about(req):
    return render(req, 'about.html')


def home(req, brand_slug=None):
    data = models.Car.objects.all()
    if brand_slug is not None:
        brand = models.Brand.objects.get(slug=brand_slug)
        data = models.Car.objects.filter(brand=brand)
    brands = models.Brand.objects.all()
    return render(req, 'home.html', {'data': data, 'brands': brands})


def detail(req, id):
    car = get_object_or_404(Car, id=id)

    if req.method == "POST":
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.save()
    else:
        form = CommentForm()

    return render(req, 'detail.html', {'car': car, 'form': form})


class register(CreateView):
    model = User
    form_class = forms.Register_form
    template_name = 'register.html'
    success_url = reverse_lazy('home')

# def register(req):
#     if req.method == "POST":
#         form = forms.Register_form(req.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = forms.Register_form()
#     return render(req, 'register.html', {'form': form, 'type': 'Register'})


class user_login(LoginView):
    template_name = 'register.html'

    def get_success_url(self):

        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

# def user_login(req):
#     if req.method == "POST":
#         form = AuthenticationForm(req, req.POST)
#         if form.is_valid():
#             name = form.cleaned_data['username']
#             pas = form.cleaned_data['password']
#             auth = authenticate(req, username=name, password=pas)
#             if auth:
#                 login(req, auth)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(req, 'register.html', {'form': form, 'type': 'Login'})


@method_decorator(login_required, name='dispatch')
class profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = models.Cart.objects.filter(user=self.request.user)
        return context


# @login_required
# def profile(req):
#     orders = models.Cart.objects.filter(user=req.user)
#     return render(req, 'profile.html', {'orders': orders})



# @login_required
def update_profile(req):
    if req.method == "POST":
        form = forms.Update(req.POST, instance=req.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = forms.Update(instance=req.user)
    return render(req, 'register.html', {'form': form})



@login_required
def user_logout(req):
    logout(req)
    return redirect('home')


def buy(req, id):
    car = get_object_or_404(models.Car, id=id)
    if car.quantity > 0:
        models.Cart.objects.create(user=req.user, car=car)
        car.quantity -= 1
        car.save()
        return redirect('profile')
    else:
        return redirect('home')
