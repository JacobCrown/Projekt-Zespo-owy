from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import UpdateView
from django.forms import ModelForm

from .forms import CustomUserCreationForm, EditCustomerForm
from store.utils import cartData

from store.models import Customer


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(SignUpView, self).get_context_data(*args,**kwargs)
        context['cartItems'] = 0
        return context

class CustomerView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    redirect_field_name = 'home'
    template_name = 'accounts/profil.html'
    model = Customer
    context_object_name = 'customer'

    def get(self, request, **kwargs):
        self.object = Customer.objects.get(id=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        context['cartItems'] = cartData(request)['cartItems']
        
        return render(request, self.template_name, context)

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user.customer
    
class CustomerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    redirect_field_name = 'home'
    model = Customer
    form_class = EditCustomerForm
    template_name = 'accounts/profiledit.html'

    def get(self, request, **kwargs):
        self.object = Customer.objects.get(id=kwargs['pk'])
        context = self.get_context_data(**kwargs)
        context['cartItems'] = cartData(request)['cartItems']
        
        return render(request, self.template_name, context)

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user.customer