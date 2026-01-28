from django.urls import path
from backend.views import add_slider_view


urlpatterns = [
    path('add-new-slider/', add_slider_view.AddSliderView.as_view(), name='add_slider'),
]
