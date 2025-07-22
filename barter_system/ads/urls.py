from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api_views


urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('ads/create/', views.ad_create, name='ad_create'),
    path('ads/<int:pk>/update/', views.ad_update, name='ad_update'),
    path('ads/<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('proposals/', views.exchange_proposal_list, name='exchange_proposal_list'),
    path('proposals/create/<int:ad_receiver_id>/', views.exchange_proposal_create, name='exchange_proposal_create'),
    path('proposals/<int:pk>/update/', views.exchange_proposal_update, name='exchange_proposal_update'),

    path('api/ads/', api_views.AdListCreateView.as_view(), name='api_ad_list_create'),
    path('api/ads/<int:pk>/', api_views.AdRetrieveUpdateDestroyView.as_view(), name='api_ad_detail'),
    path('api/proposals/', api_views.ExchangeProposalListCreateView.as_view(), name='api_proposal_list_create'),
    path('api/proposals/<int:pk>/', api_views.ExchangeProposalRetrieveUpdateView.as_view(), name='api_proposal_detail'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]