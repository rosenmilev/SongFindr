from django.urls import path
from . import views
from .views import TermsOfUseView

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('terms_of_use/', TermsOfUseView.as_view(), name='terms_of_use'),
]
