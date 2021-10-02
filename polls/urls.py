from django.urls import path

from . import views
app_name = 'polls'
urlpatterns = [
    path('classfication', views.IndexView.as_view(), name='index'),
   path('download/', views.mlmodels),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:attribute_id>/vote/', views.vote, name='vote'),
    path('signup',views.signup, name = 'signup'),
    path('doclassification', views.home1, name = 'doclassification'),
    path('result', views.result),
    
]

