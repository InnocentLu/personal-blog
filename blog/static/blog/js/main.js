/**
 * 陆焱烨个人技术博客 - 交互动效脚本
 * 包含：滚动入场动画、返回顶部按钮、数字递增动画
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============ 1. 返回顶部按钮 ============
    // 动态创建返回顶部按钮
    var backToTopBtn = document.createElement('button');
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.innerHTML = '↑';
    backToTopBtn.title = '返回顶部';
    document.body.appendChild(backToTopBtn);

    // 滚动监听：控制按钮显示/隐藏
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    // 点击返回顶部
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ============ 2. 滚动入场动画（IntersectionObserver） ============
    // 为指定元素添加 scroll-reveal 类，进入视口时触发动画
    var revealTargets = document.querySelectorAll(
        '.content-card, .sidebar-card, .honor-item, .acm-template-card, .acm-detail-page > *'
    );

    // 使用 IntersectionObserver 实现高性能滚动检测
    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // 触发数字递增动画
                    var nums = entry.target.querySelectorAll('.stat-num');
                    nums.forEach(animateCounter);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealTargets.forEach(function(el) {
            // 已有 CSS 动画的元素不再重复添加
            if (!el.style.animation) {
                el.classList.add('scroll-reveal');
                observer.observe(el);
            }
        });
    }

    // ============ 3. 数字递增动画 ============
    function animateCounter(el) {
        if (el.dataset.animated) return;
        el.dataset.animated = 'true';

        var target = parseInt(el.textContent, 10) || 0;
        if (target === 0) return;

        var duration = 1200;
        var startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            // easeOutQuart 缓动函数
            var eased = 1 - Math.pow(1 - progress, 4);
            el.textContent = Math.floor(eased * target);
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                el.textContent = target;
            }
        }
        requestAnimationFrame(step);
    }

    // ============ 4. 导航栏滚动渐变效果 ============
    var navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            } else {
                navbar.style.boxShadow = '0 2px 12px rgba(0, 0, 0, 0.06)';
                navbar.style.background = 'linear-gradient(135deg, #ffffff 0%, #fafbfc 100%)';
            }
        });
    }

    // ============ 5. 卡片点击波纹效果 ============
    var rippleTargets = document.querySelectorAll('.content-card, .acm-template-card');
    rippleTargets.forEach(function(card) {
        card.addEventListener('click', function(e) {
            var ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(23, 81, 153, 0.15)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';

            var rect = card.getBoundingClientRect();
            var size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';

            // 确保 card 有 position: relative
            if (getComputedStyle(card).position === 'static') {
                card.style.position = 'relative';
            }
            card.style.overflow = 'hidden';
            card.appendChild(ripple);

            setTimeout(function() {
                ripple.remove();
            }, 600);
        });
    });

    // 动态注入 ripple 关键帧
    var style = document.createElement('style');
    style.textContent = '@keyframes ripple { to { transform: scale(2.5); opacity: 0; } }';
    document.head.appendChild(style);

});
