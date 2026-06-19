"""blog 应用视图函数"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from .models import Content, PersonalInfo, Honor, ACMTemplate


@require_GET
def home(request):
    """
    首页：内容信息流
    支持按内容类型筛选，默认展示全部内容
    按发布时间倒序排列
    """
    content_type = request.GET.get('type', '')
    if content_type in ('blog', 'video', 'code'):
        contents = Content.objects.filter(content_type=content_type)
    else:
        contents = Content.objects.all()

    # 热门内容：按浏览量倒序取前 5 条
    hot_contents = Content.objects.order_by('-views')[:5]

    return render(request, 'blog/home.html', {
        'contents': contents,
        'hot_contents': hot_contents,
        'current_type': content_type,
    })


@require_GET
def content_detail(request, pk):
    """
    内容详情页
    根据内容类型动态渲染对应展示效果
    自动累加浏览量
    """
    content = get_object_or_404(Content, pk=pk)
    # 浏览量 +1
    Content.objects.filter(pk=pk).update(views=content.views + 1)
    content.refresh_from_db()

    # 热门内容
    hot_contents = Content.objects.exclude(pk=pk).order_by('-views')[:5]

    return render(request, 'blog/detail.html', {
        'content': content,
        'hot_contents': hot_contents,
    })


@require_GET
def about(request):
    """关于我页面：展示个人介绍、学业背景、技术栈、荣誉奖项"""
    personal_info, _ = PersonalInfo.objects.get_or_create(
        pk=1,
        defaults={'name': '陆焱烨'}
    )
    honors = Honor.objects.all()
    return render(request, 'blog/about.html', {
        'personal_info': personal_info,
        'honors': honors,
    })


@require_GET
def acm_template_list(request):
    """
    ACM 算法板子列表页
    支持按分类筛选，按分类分组展示
    """
    category = request.GET.get('category', '')
    if category:
        templates = ACMTemplate.objects.filter(category=category)
    else:
        templates = ACMTemplate.objects.all()

    # 按分类分组统计
    from collections import OrderedDict
    category_stats = OrderedDict()
    for cat_code, cat_name in ACMTemplate.CATEGORY_CHOICES:
        count = ACMTemplate.objects.filter(category=cat_code).count()
        if count > 0:
            category_stats[cat_code] = {'name': cat_name, 'count': count}

    # 热门内容（复用侧边栏）
    hot_contents = Content.objects.order_by('-views')[:5]

    return render(request, 'blog/acm_list.html', {
        'templates': templates,
        'category_stats': category_stats,
        'current_category': category,
        'hot_contents': hot_contents,
    })


@require_GET
def acm_template_detail(request, pk):
    """
    ACM 算法板子详情页
    展示代码内容，使用 highlight.js 进行语法高亮
    """
    template = get_object_or_404(ACMTemplate, pk=pk)
    # 浏览量 +1
    ACMTemplate.objects.filter(pk=pk).update(views=template.views + 1)
    template.refresh_from_db()

    # 同分类的其他板子
    related = ACMTemplate.objects.filter(
        category=template.category
    ).exclude(pk=pk)[:5]

    # 热门内容（复用侧边栏）
    hot_contents = Content.objects.order_by('-views')[:5]

    return render(request, 'blog/acm_detail.html', {
        'template': template,
        'related': related,
        'hot_contents': hot_contents,
    })
