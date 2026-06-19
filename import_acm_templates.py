"""
导入 ACM 动态规划板子代码到数据库
读取 d:\Code\ACM\动态规划 目录下所有 .cpp 文件
按子目录名分类，解析文件名提取题目编号与标题
"""
import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')
django.setup()

from blog.models import ACMTemplate

# 源代码目录
SOURCE_DIR = r'd:\Code\ACM\动态规划'

# 子目录名到分类的映射
DIR_CATEGORY_MAP = {
    '01背包DP': '01背包',
    '区间DP': '区间DP',
    '基础DP': '基础DP',
    '完全背包': '完全背包',
    '数位DP': '数位DP',
}

# 解析文件名：提取题目编号和标题
# 例如: P1048采药.cpp -> problem_id=P1048, title=采药
#       P_3842_TJOI_2007_线段.cpp -> problem_id=P3842, title=TJOI_2007_线段
#       SP6340ZUMA_ZUMA.cpp -> problem_id=SP6340, title=ZUMA_ZUMA
#       数字计数.cpp -> problem_id='', title=数字计数
ID_PATTERN = re.compile(r'^(P_?\d+|SP\d+)(.*)$')


def parse_filename(filename):
    """从文件名解析题目编号和标题"""
    name = filename.replace('.cpp', '')
    match = ID_PATTERN.match(name)
    if match:
        problem_id = match.group(1).replace('_', '')
        title = match.group(2) if match.group(2) else name
        return problem_id, title
    return '', name


def import_templates():
    """导入所有板子代码"""
    count = 0
    for subdir_name, category in DIR_CATEGORY_MAP.items():
        subdir_path = os.path.join(SOURCE_DIR, subdir_name)
        if not os.path.isdir(subdir_path):
            continue

        for filename in os.listdir(subdir_path):
            if not filename.endswith('.cpp'):
                continue
            # 跳过临时文件
            if 'tempCodeRunnerFile' in filename:
                continue

            filepath = os.path.join(subdir_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                code_content = f.read()

            problem_id, title = parse_filename(filename)

            # 使用 get_or_create 避免重复导入
            obj, created = ACMTemplate.objects.get_or_create(
                title=title,
                category=category,
                defaults={
                    'problem_id': problem_id,
                    'code': code_content,
                }
            )
            if created:
                count += 1
                print(f'  导入: [{category}] {title} ({problem_id})')
            else:
                print(f'  跳过(已存在): [{category}] {title}')

    print(f'\n导入完成！共导入 {count} 条板子，数据库总计 {ACMTemplate.objects.count()} 条')


if __name__ == '__main__':
    import_templates()
