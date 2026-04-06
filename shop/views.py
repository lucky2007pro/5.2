from .forms import CarForm
from .models import Car
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = '/'

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = '/'

class CarDeleteView(DeleteView):
    model = Car
    success_url = '/'