from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Users

# Register your models here.


class UserInfoAdmin(UserAdmin):
    # 管理列表页面中想要显示的字段
    list_display = ('username', 'mobile', 'is_active', 'is_employee', 'date_joined', 'last_login')

    # 分页，每页数量
    list_per_page = 20

    # 只读的字段
    readonly_fields = ('nickname', 'avatar', 'gender', 'total_points', 'date_joined', 'last_login')

    # 详情页显示字段
    fieldsets = [
        ('基本信息', {'fields': ('username', 'mobile', 'email', 'is_active', 'is_employee', 'groups')}),
        ('补充信息', {'fields': ('nickname', 'avatar', 'gender', 'total_points', 'date_joined', 'last_login')})
    ]

    # 编辑页字段
    add_fieldsets = [
        ('创建用户', {
            'fields': ('username', 'password1', 'password2', 'mobile', 'email', 'is_active', 'is_employee', 'groups')}),
    ]


# TODO admin后台创建、编辑用户未对账户去重，存在隐患。
admin.site.register(Users, UserInfoAdmin)
