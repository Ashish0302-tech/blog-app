from django.contrib import admin
from django.urls import path,include
from accounts import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
     path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blogs/new/', views.blog_create, name='blog_create'),
    path('blogs/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('blogs/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
