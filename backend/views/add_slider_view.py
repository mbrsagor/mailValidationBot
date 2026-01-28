from django.views import generic


from backend.forms.slider_form import SliderModelForm
from backend.models import Slider



class AddSliderView(generic.CreateView):
    model = Slider
    form_class = SliderModelForm
    template_name = 'features/slider/add_slider.html'
    success_url = '/admin/backend/slider/'
