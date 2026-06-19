# 陆焱烨的个人技术博客

> 基于 Django 开发的个人技术博客网站，支持博客文章、视频内容、代码片段三种内容类型，并集成 ACM 算法板子库。

## 博主简介

**陆焱烨**，计算机242班大二在读学生，热爱算法竞赛与技术开发。

主要荣誉：
- 蓝桥杯全国一等奖
- 浙江省大学生程序设计竞赛铜牌

## 博客功能

### 内容发布体系

| 内容类型 | 说明 |
|---------|------|
| 博客文章 | 支持正文内容、基础文本分段排版 |
| 视频内容 | 支持上传本地 mp4 视频，详情页内嵌 HTML5 播放器 |
| 代码片段 | 支持选择编程语言、代码说明，详情页 highlight.js 语法高亮 |

- 首页信息流混合展示三种内容，按发布时间倒序排列
- 每条内容卡片显示类型标签、标题、简介、发布时间

### ACM 算法板子库

- 收录动态规划等各类算法竞赛模板代码
- 按分类组织（01背包DP、区间DP、基础DP、完全背包、数位DP）
- 代码高亮显示，支持按分类筛选

### 个人介绍与荣誉

- 个人信息单例模型，全站仅一条数据
- 包含姓名、年级专业、头像、个人简介、技术栈标签
- 荣誉奖项支持多条记录，后台可自由增删

### 页面结构

- **首页**：内容信息流主页面
- **内容详情页**：根据内容类型动态渲染
- **算法板子**：ACM 模板代码列表与详情
- **关于我**：完整展示个人介绍、学业背景、技术栈、荣誉奖项

## 本地环境搭建

### 1. 环境要求

- Python 3.10+
- MySQL 8.0+
- Git
- Git LFS（用于管理大文件）

### 2. 克隆仓库

```bash
git clone https://github.com/InnocentLu/personal-blog.git
cd personal-blog
```

### 3. 安装 Git LFS（管理视频等大文件）

```bash
git lfs install
git lfs pull
```

### 4. 创建虚拟环境并安装依赖

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 5. 配置环境变量

复制环境变量示例文件并填入实际配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
DJANGO_SECRET_KEY=你的随机密钥
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

DB_NAME=my_weblog
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_HOST=localhost
DB_PORT=3306
```

### 6. 创建 MySQL 数据库

```sql
CREATE DATABASE my_weblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. 导入 ACM 算法板子（可选）

```bash
python import_acm_templates.py
```

### 9. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 10. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 查看博客前台
访问 http://127.0.0.1:8000/admin/ 进入后台管理

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DJANGO_SECRET_KEY` | Django 安全密钥 | 无（必须配置） |
| `DJANGO_DEBUG` | 调试模式（True/False） | False |
| `DJANGO_ALLOWED_HOSTS` | 允许访问的主机名 | * |
| `DB_NAME` | MySQL 数据库名 | my_weblog |
| `DB_USER` | MySQL 用户名 | root |
| `DB_PASSWORD` | MySQL 密码 | 无（必须配置） |
| `DB_HOST` | MySQL 主机地址 | localhost |
| `DB_PORT` | MySQL 端口 | 3306 |

## 项目结构

```
my_blog/
├── manage.py                  # 项目管理脚本
├── requirements.txt           # 依赖清单
├── .env.example               # 环境变量示例
├── .env                       # 环境变量（不提交）
├── .gitignore                 # Git 忽略配置
├── .gitattributes             # Git LFS 配置
├── import_acm_templates.py    # ACM 板子导入脚本
├── media/                     # 媒体文件目录
├── my_blog/                   # Django 项目包
│   ├── settings.py            # 核心配置
│   ├── urls.py                # 根路由
│   └── ...
└── blog/                      # 博客应用
    ├── models.py              # 数据模型
    ├── views.py               # 视图函数
    ├── admin.py               # 后台注册
    ├── templates/blog/        # HTML 模板
    └── static/blog/           # 静态文件（CSS/JS）
```

## 技术栈

- **后端**：Django 4.2
- **数据库**：MySQL 8.0（utf8mb4 字符集）
- **前端**：原生 HTML/CSS/JavaScript
- **代码高亮**：highlight.js
- **环境管理**：python-dotenv

## License

MIT License
