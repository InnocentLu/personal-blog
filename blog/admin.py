"""blog 应用后台注册配置"""
from django.contrib import admin
from .models import PersonalInfo, Honor, Content, ACMTemplate


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    """个人信息后台管理：单例模式"""
    list_display = ('name', 'grade_major', 'updated_at')
    fieldsets = (
        ('基础信息', {
            'fields': ('name', 'grade_major', 'avatar', 'intro')
        }),
        ('技术栈', {
            'fields': ('tech_stack',),
            'description': '多个技术栈标签请用英文逗号分隔，例如：Python,Java,C++'
        }),
    )

    # 限制只能存在一条记录
    def has_add_permission(self, request):
        return not PersonalInfo.objects.exists()


@admin.register(Honor)
class HonorAdmin(admin.ModelAdmin):
    """荣誉奖项后台管理"""
    list_display = ('title', 'award_date', 'order', 'created_at')
    list_filter = ('award_date',)
    search_fields = ('title', 'description')
    list_editable = ('order',)
    ordering = ('order', '-created_at')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """内容后台管理：博客文章 / 视频内容 / 代码片段"""
    list_display = (
        'title', 'content_type', 'views', 'published_at'
    )
    list_filter = ('content_type', 'published_at')
    search_fields = ('title', 'summary')
    list_editable = ('content_type',)
    ordering = ('-published_at',)

    fieldsets = (
        ('通用信息', {
            'fields': ('title', 'content_type', 'summary', 'cover')
        }),
        ('博客文章内容', {
            'fields': ('body',),
            'description': '仅当内容类型为「博客文章」时填写',
            'classes': ('collapse',),
        }),
        ('视频内容', {
            'fields': ('video_file', 'video_desc'),
            'description': '仅当内容类型为「视频内容」时填写，支持上传 mp4 文件',
            'classes': ('collapse',),
        }),
        ('代码片段', {
            'fields': ('language', 'code_content', 'code_desc'),
            'description': '仅当内容类型为「代码片段」时填写',
            'classes': ('collapse',),
        }),
    )


@admin.register(ACMTemplate)
class ACMTemplateAdmin(admin.ModelAdmin):
    """ACM 算法板子后台管理"""
    list_display = ('title', 'category', 'problem_id', 'views', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'problem_id', 'description')
    list_editable = ('category',)
    ordering = ('category', '-created_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'problem_id')
        }),
        ('代码内容', {
            'fields': ('code', 'description')
        }),
    )
