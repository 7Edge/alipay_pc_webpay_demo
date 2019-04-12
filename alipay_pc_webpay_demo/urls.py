"""alipay_pc_webpay_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path

from alipay_web import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path('pay/$', views.pay_order, name='pay'),
    re_path('pay_notify/', views.async_notify, name='pay_notify'),
    re_path('pay_result/$', views.pay_result, name='pay_result')
]


