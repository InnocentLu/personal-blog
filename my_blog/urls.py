"""my_blog 项目 URL 路由配置"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django 后台管理
    path('admin/', admin.site.urls),
    # blog 应用路由
    path('', include('blog.urls')),
]

# 媒体文件访问路由
# 开发环境：DEBUG=True 时由 Django 开发服务器提供
# 生产环境：DEBUG=False 时也提供服务（Railway 容器内 media 临时存储）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
