from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.SignupPage, name="signup"),  # Root URL points to SignupPage
    path("home/", views.HomePage, name="home"),  # /home URL points to HomePage
    path("login/", views.LoginPage, name="login"),  # /login URL points to LoginPage
    path(
        "logout/", views.LogoutPage, name="logout"
    ),  # /logout URL points to LogoutPage
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
