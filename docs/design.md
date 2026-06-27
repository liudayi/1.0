# 我的博客系统设计文档

## 1. 项目背景
个人学习 Django 的练习项目，实现用户认证、文章发布、评论功能。

## 2. 功能列表
- 用户注册、登录、注销
- 发布、编辑、删除文章
- 文章列表分页显示
- "碎碎念"功能
- "友链"动态显示
- 导航栏组件

## 3. 数据模型
### User（使用 Django 内置）
### Article
- title: CharField
- content: TextField
- author: ForeignKey(User)
- created_at: DateTimeField

## 4. 技术栈
- Python 3.11
- Django 5.x
- SQLite（开发）
- Bootstrap 5（前端样式）

## 5.功能模块

### 5.1用户系统与认证模块
- 功能概述:~~提供用户的登录和注销功能,因为用户登录后有权限修改内容,所以还需要鉴权功能~~
    实现用户的登录、注销，并基于登录状态控制文章、评论等内容的修改权限（鉴权）。
- URL 设计(用户访问的路径)
    ~~'login','logout'~~

- 模型设计 (models.py)
    Django自带的User类(Django.contrib.auth)
- 表单设计 (forms.py)
    ~~这是干什么的?(用于校验数据)~~
    校验清洗出干净的数据给views层使用,继承FormView
- 视图设计 (views.py)
    ~~LoginView;LogoutView;(负责执行操作)~~

- 模板设计 (templates/)
    homepage.html;authentication/user_login.html
- 数据流说明
    
