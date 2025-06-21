# Cursor 规则使用指南

## 概述

本项目已经配置了完整的 Cursor 规则和 VS Code 设置，以提供最佳的 Django 开发体验。这些配置包括代码规范、开发工具、任务自动化等。

## 文件结构

```
.vscode/
├── settings.json          # VS Code 工作区设置
├── extensions.json        # 推荐的扩展列表
├── tasks.json            # 预定义任务
├── launch.json           # 调试配置
└── django.code-snippets  # Django 代码片段

.cursorrules              # Cursor AI 规则
```

## 主要功能

### 1. 代码规范 (.cursorrules)

`.cursorrules` 文件定义了项目的编码规范和最佳实践：

- **Python/Django 规范**: PEP 8 风格、命名约定、导入顺序
- **前端规范**: HTML 语义化、JavaScript 规范
- **文件组织**: 应用结构、API 结构、模板结构
- **开发最佳实践**: 数据库优化、缓存策略、安全考虑
- **API 设计**: RESTful 设计、版本控制、错误处理

### 2. VS Code 设置 (settings.json)

配置了以下功能：

- **Python 环境**: 自动激活虚拟环境、代码格式化、导入排序
- **Django 支持**: 模板语法高亮、路径配置、调试设置
- **编辑器配置**: 自动保存、代码格式化、文件关联
- **文件过滤**: 排除缓存文件、虚拟环境等

### 3. 扩展推荐 (extensions.json)

推荐安装的扩展包括：

- **Python 开发**: Python、Black、Flake8、Pylance
- **Django 开发**: Django、Django Template
- **前端开发**: Prettier、ESLint
- **工具**: GitLens、Docker、Material Icon Theme

### 4. 任务自动化 (tasks.json)

预定义了常用任务：

```bash
# 开发服务器
Ctrl+Shift+P → "Tasks: Run Task" → "启动 Django 开发服务器"

# 数据库迁移
Ctrl+Shift+P → "Tasks: Run Task" → "数据库迁移"

# 代码格式化
Ctrl+Shift+P → "Tasks: Run Task" → "代码格式化 (Black)"
```

### 5. 代码片段 (django.code-snippets)

提供了常用的代码模板：

- `django-model`: 创建 Django 模型
- `django-view`: 创建视图函数
- `django-class-view`: 创建类视图
- `django-ninja-api`: 创建 Django Ninja API
- `django-form`: 创建表单
- `django-template`: 创建模板
- `django-test`: 创建测试
- `django-admin`: 创建 Admin 配置

## 使用方法

### 1. 安装扩展

打开 VS Code，按 `Ctrl+Shift+X` 打开扩展面板，安装推荐的扩展。

### 2. 使用代码片段

在 Python 文件中输入片段前缀（如 `django-model`），按 `Tab` 键自动补全。

### 3. 运行任务

按 `Ctrl+Shift+P` 打开命令面板，输入 "Tasks: Run Task" 选择要运行的任务。

### 4. 代码格式化

保存文件时自动格式化，或手动按 `Shift+Alt+F`。

### 5. 调试

按 `F5` 启动调试，或使用预配置的调试配置。

## 开发工作流

### 1. 创建新应用

```bash
# 使用代码生成器
python src/manage.py autocode app_name

# 或手动创建
python src/manage.py startapp app_name
```

### 2. 开发流程

1. **创建模型**: 使用 `django-model` 片段
2. **创建迁移**: 运行 "数据库迁移" 任务
3. **创建视图**: 使用 `django-view` 或 `django-class-view` 片段
4. **创建模板**: 使用 `django-template` 片段
5. **创建测试**: 使用 `django-test` 片段
6. **代码格式化**: 保存时自动格式化

### 3. API 开发

1. **创建 Schema**: 使用 `django-ninja-api` 片段
2. **实现端点**: 遵循 RESTful 设计原则
3. **添加文档**: 使用 docstring 描述 API
4. **测试 API**: 使用 Postman 或 curl

### 4. 前端开发

1. **HTML/CSS**: 使用语义化 HTML 和标准 CSS
2. **JavaScript**: 使用原生 JavaScript 或 Alpine.js 进行交互

## 最佳实践

### 1. 代码质量

- 遵循 PEP 8 规范
- 使用 Black 格式化代码
- 使用 isort 排序导入
- 使用 Flake8 检查代码质量

### 2. 测试

- 为每个模型和视图编写测试
- 使用 Factory Boy 生成测试数据
- 保持测试覆盖率 > 80%

### 3. 安全

- 使用 Django 内置安全功能
- 验证所有用户输入
- 实现适当的权限控制
- 使用 HTTPS 在生产环境

### 4. 性能

- 优化数据库查询
- 使用缓存减少数据库访问
- 压缩静态文件
- 使用 CDN 分发静态资源

## 故障排除

### 1. Python 解释器问题

确保 VS Code 使用正确的 Python 解释器：
1. 按 `Ctrl+Shift+P`
2. 输入 "Python: Select Interpreter"
3. 选择项目虚拟环境

### 2. 扩展不工作

1. 检查扩展是否正确安装
2. 重启 VS Code
3. 检查扩展设置

### 3. 任务执行失败

1. 检查命令路径是否正确
2. 确保依赖已安装
3. 检查工作目录设置

### 4. 代码片段不工作

1. 确保文件类型正确
2. 检查片段语法
3. 重启 VS Code

## 自定义配置

### 1. 修改代码规范

编辑 `.cursorrules` 文件，添加或修改规则。

### 2. 添加新任务

在 `tasks.json` 中添加新的任务定义。

### 3. 创建自定义片段

在 `django.code-snippets` 中添加新的代码片段。

### 4. 调整设置

修改 `settings.json` 中的设置项。

## 总结

这些 Cursor 规则和 VS Code 配置为 Django 开发提供了完整的开发环境，包括：

- 统一的代码规范
- 自动化开发工具
- 代码片段和模板
- 任务自动化
- 调试和测试支持 