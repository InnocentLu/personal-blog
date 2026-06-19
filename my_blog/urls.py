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
# 仅在 DEBUG=True（开发环境）时由 Django 开发服务器提供 media 文件服务
# 生产环境（DEBUG=False）不挂载 media 路由，避免目录不存在时引发 500 错误
# Railway 容器是临时存储，media 文件每次部署后丢失，需用云存储（如 S3/Cloudinary）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
