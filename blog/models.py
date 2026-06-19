"""blog 应用数据模型定义"""
from django.db import models


class PersonalInfo(models.Model):
    """
    博主个人信息模型（单例模式：全站仅一条数据）
    用于展示博主基础信息、技术栈等
    """
    name = models.CharField('姓名', max_length=50, default='陆焱烨')
    grade_major = models.CharField(
        '年级专业',
        max_length=100,
        default='计算机242班 大二在读'
    )
    avatar = models.ImageField(
        '头像',
        upload_to='avatars/',
        blank=True,
        null=True
    )
    intro = models.TextField('个人简介', blank=True, default='')
    # 技术栈以逗号分隔存储，例如 "Python,Java,C++"
    tech_stack = models.CharField(
        '技术栈标签（逗号分隔）',
        max_length=255,
        blank=True,
        default='Python,Java,C++,HTML/CSS,JavaScript'
    )
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'

    def __str__(self):
        return self.name


class Honor(models.Model):
    """荣誉奖项模型，可多条记录"""
    title = models.CharField('奖项名称', max_length=200)
    description = models.TextField('奖项描述', blank=True, default='')
    award_date = models.DateField('获奖日期', blank=True, null=True)
    order = models.IntegerField(
        '排序（数字越小越靠前）',
        default=0
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '荣誉奖项'
        verbose_name_plural = '荣誉奖项'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Content(models.Model):
    """
    统一内容模型：博客文章 / 视频内容 / 代码片段
    通过 content_type 字段区分内容类型
    """

    # 内容类型枚举
    TYPE_BLOG = 'blog'
    TYPE_VIDEO = 'video'
    TYPE_CODE = 'code'
    CONTENT_TYPE_CHOICES = [
        (TYPE_BLOG, '博客文章'),
        (TYPE_VIDEO, '视频内容'),
        (TYPE_CODE, '代码片段'),
    ]

    # 通用字段
    title = models.CharField('标题', max_length=200)
    content_type = models.CharField(
        '内容类型',
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default=TYPE_BLOG
    )
    summary = models.CharField('内容简介', max_length=500, blank=True, default='')
    cover = models.ImageField(
        '封面图',
        upload_to='covers/',
        blank=True,
        null=True
    )
    published_at = models.DateTimeField('发布时间', auto_now_add=True)
    views = models.PositiveIntegerField('浏览量', default=0)

    # 博客文章专属字段
    body = models.TextField('正文内容（博客文章）', blank=True, default='')

    # 视频内容专属字段
    video_file = models.FileField(
        '视频文件（mp4）',
        upload_to='videos/',
        blank=True,
        null=True
    )
    video_desc = models.TextField('视频简介', blank=True, default='')

    # 代码片段专属字段
    language = models.CharField(
        '编程语言',
        max_length=50,
        blank=True,
        default='python'
    )
    code_content = models.TextField('代码内容', blank=True, default='')
    code_desc = models.TextField('代码说明', blank=True, default='')

    class Meta:
        verbose_name = '内容'
        verbose_name_plural = '内容'
        ordering = ['-published_at']

    def __str__(self):
        return f'[{self.get_content_type_display()}] {self.title}'


class ACMTemplate(models.Model):
    """
    ACM 算法模板/题解模型
    用于存储动态规划等各类算法板子代码
    按分类组织，支持按题目编号检索
    """

    # 算法分类
    CATEGORY_01_KNAPSACK = '01背包'
    CATEGORY_INTERVAL = '区间DP'
    CATEGORY_BASIC = '基础DP'
    CATEGORY_COMPLETE_KNAPSACK = '完全背包'
    CATEGORY_DIGIT = '数位DP'
    CATEGORY_OTHER = '其他'

    CATEGORY_CHOICES = [
        (CATEGORY_01_KNAPSACK, '01背包DP'),
        (CATEGORY_INTERVAL, '区间DP'),
        (CATEGORY_BASIC, '基础DP'),
        (CATEGORY_COMPLETE_KNAPSACK, '完全背包'),
        (CATEGORY_DIGIT, '数位DP'),
        (CATEGORY_OTHER, '其他'),
    ]

    title = models.CharField('题目标题', max_length=200)
    category = models.CharField(
        '分类',
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER
    )
    problem_id = models.CharField('题目编号', max_length=50, blank=True, default='')
    code = models.TextField('代码内容')
    description = models.TextField('题目说明', blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    views = models.PositiveIntegerField('浏览量', default=0)

    class Meta:
        verbose_name = '算法板子'
        verbose_name_plural = '算法板子'
        ordering = ['category', '-created_at']

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title}'
