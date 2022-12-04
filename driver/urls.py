from django.contrib import admin
from django.urls import path

from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="/"),
    path('signup/', signup, name="signup"),
    # path('quiz/<str:ty>/', quiz, name="quiz"),
    path('signin/', signin, name="signin"),
    path('logout/', signout,name="logout"),
    path('question/', check_quiz,name="check_quiz"),
    path('question/<str:tyy>/', check_quiz,name="check_quiz"),
    path('result/', result,name="result"),
    path('email/', s_email,name="email"),
]
