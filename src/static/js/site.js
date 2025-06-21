// 检查用户偏好的主题并应用
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

// 主题切换函数
function toggleDarkMode() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // 更新按钮图标
    updateThemeButton(newTheme);
}

// 更新主题切换按钮
function updateThemeButton(theme) {
    const button = document.getElementById('theme-toggle');
    if (!button) return;
    
    const sunIcon = button.querySelector('.fa-sun');
    const moonIcon = button.querySelector('.fa-moon');
    
    if (theme === 'dark') {
        sunIcon?.parentElement.classList.remove('hidden');
        moonIcon?.parentElement.classList.add('hidden');
    } else {
        sunIcon?.parentElement.classList.add('hidden');
        moonIcon?.parentElement.classList.remove('hidden');
    }
}

// 初始化主题
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    let theme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeButton(theme);
}

// 用户下拉菜单功能
function initUserDropdown() {
    const dropdownButton = document.getElementById('dropdownNavbarLink');
    const dropdownMenu = document.getElementById('dropdownNavbar');
    
    if (!dropdownButton || !dropdownMenu) return;
    
    dropdownButton.addEventListener('click', function(e) {
        e.preventDefault();
        dropdownMenu.classList.toggle('show');
    });
    
    // 点击外部关闭下拉菜单
    document.addEventListener('click', function(e) {
        if (!dropdownButton.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
}

// 移动端菜单功能
function initMobileMenu() {
    const menuButton = document.querySelector('[data-collapse-toggle]');
    const mobileMenu = document.getElementById('navbar-multi-level');
    
    if (!menuButton || !mobileMenu) return;
    
    menuButton.addEventListener('click', function(e) {
        e.preventDefault();
        mobileMenu.classList.toggle('show');
        
        // 更新按钮状态
        const isExpanded = mobileMenu.classList.contains('show');
        menuButton.setAttribute('aria-expanded', isExpanded);
    });
    
    // 点击菜单项关闭菜单
    const menuItems = mobileMenu.querySelectorAll('a');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            mobileMenu.classList.remove('show');
            menuButton.setAttribute('aria-expanded', 'false');
        });
    });
}

// 警告框关闭功能
function initAlerts() {
    const alerts = document.querySelectorAll('[data-dismiss-target]');
    
    alerts.forEach(alert => {
        const closeButton = alert.querySelector('[data-dismiss-target]');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                const targetId = this.getAttribute('data-dismiss-target');
                const target = document.querySelector(targetId);
                if (target) {
                    target.style.opacity = '0';
                    setTimeout(() => {
                        target.remove();
                    }, 300);
                }
            });
        }
    });
}

// 平滑滚动功能
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 卡片悬停效果
function initCardHover() {
    const cards = document.querySelectorAll('.card, .feature-card, .example-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// 按钮点击效果
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // 创建涟漪效果
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// 表单验证
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // 显示错误消息
                    let errorMsg = field.parentNode.querySelector('.error-message');
                    if (!errorMsg) {
                        errorMsg = document.createElement('div');
                        errorMsg.className = 'error-message';
                        field.parentNode.appendChild(errorMsg);
                    }
                    errorMsg.textContent = '此字段为必填项';
                } else {
                    field.classList.remove('error');
                    const errorMsg = field.parentNode.querySelector('.error-message');
                    if (errorMsg) {
                        errorMsg.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// 懒加载图片
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // 降级处理
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// 工具提示功能
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip-popup';
            tooltip.textContent = tooltipText;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip-popup');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// 页面加载完成后初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initUserDropdown();
    initMobileMenu();
    initAlerts();
    initSmoothScroll();
    initCardHover();
    initButtonEffects();
    initFormValidation();
    initLazyLoading();
    initTooltips();
    
    console.log('DjangoStarter 站点功能已初始化');
});

// 窗口大小改变时重新计算布局
window.addEventListener('resize', function() {
    // 可以在这里添加响应式相关的功能
});

// 页面可见性变化时的处理
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // 页面隐藏时的处理
    } else {
        // 页面显示时的处理
    }
});

// 导出全局函数
window.toggleDarkMode = toggleDarkMode;