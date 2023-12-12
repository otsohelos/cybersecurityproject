from django.urls import path, include
from .views import homePageView, addView, latestView
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', homePageView, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
	path('logout/', LogoutView.as_view(next_page='/')),
	path('login/', LoginView.as_view(template_name='registration/login.html')),
    path('add/', addView, name='add'),
    path('latest/<int:user_id>', latestView, name='latest'),
]
