from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView
from django.forms import ModelForm

from ecommerce.settings import LOGIN_REDIRECT_URL

from .forms import CustomUserCreationForm

from store.models import Customer


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomerView(generic.DetailView):
    template_name = 'accounts/profile.html'
    model = Customer
    context_object_name = 'customer'

    
class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'email', 'profile_image']
    template_name = 'accounts/profile_edit.html'
    # success_url = reverse_lazy('checkout')


class Frm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'profile_image']

def edit(request, pk):
    customer = Customer.objects.get(id=pk)
    form = Frm(instance=customer)

    if request.method == 'POST':
        form = Frm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            
            return redirect('profile')
    context = {'form': form}    
    return render(request, 'accounts/profile_edit.html', context)

        
        
    