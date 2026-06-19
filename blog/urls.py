"""blog 应用路由配置"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 首页
    path('', views.home, name='home'),
    # 内容详情页
    path('content/<int:pk>/', views.content_detail, name='detail'),
    # 关于我页面
    path('about/', views.about, name='about'),
    # ACM 算法板子
    path('acm/', views.acm_template_list, name='acm_list'),
    path('acm/<int:pk>/', views.acm_template_detail, name='acm_detail'),
]
