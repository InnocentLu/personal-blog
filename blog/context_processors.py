"""自定义模板上下文处理器：将博主信息注入所有模板"""
from django.db.models import Sum
from .models import PersonalInfo, Honor, Content, ACMTemplate


def blog_info(request):
    """
    向所有模板注入博主信息、荣誉列表、内容统计
    确保侧边栏在所有页面都能正常显示
    """
    # 获取唯一的博主信息记录（若无则创建默认记录）
    personal_info, _ = PersonalInfo.objects.get_or_create(
        pk=1,
        defaults={'name': '陆焱烨'}
    )
    # 全部荣誉奖项
    honors = Honor.objects.all()
    # 内容统计
    blog_count = Content.objects.filter(content_type='blog').count()
    video_count = Content.objects.filter(content_type='video').count()
    code_count = Content.objects.filter(content_type='code').count()
    total_count = Content.objects.count()
    # 总浏览量
    total_views = Content.objects.aggregate(
        total=Sum('views')
    )['total'] or 0
    # 算法板子数量
    acm_count = ACMTemplate.objects.count()

    return {
        'blog_info': personal_info,
        'honors': honors,
        'blog_count': blog_count,
        'video_count': video_count,
        'code_count': code_count,
        'total_count': total_count,
        'total_views': total_views,
        'acm_count': acm_count,
    }
