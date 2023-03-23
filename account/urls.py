from django.urls import path
import account.views


urlpatterns = [
    path('logout/', account.views.logout, name="logout"),
    path('login/', account.views.login, name="login"),
    path('register/', account.views.register, name="register"),
]
