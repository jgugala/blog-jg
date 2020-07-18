from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('', views.PostsList.as_view(), name='home'),
    path('search/', views.PostsList.as_view(), name='search_results'),
    path('create/', views.PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('<slug:slug>/', views.PostDetails.as_view(), name='post_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
