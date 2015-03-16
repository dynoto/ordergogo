from django.contrib import admin
from member.models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff','photo','updated_at')
# Register your models here.
