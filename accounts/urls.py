from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]

# 장고 내 클래스를 이용하는 경우, 메소드 형식으로 함수를 써준다. import도 잊지 않기