from django.contrib.admin import register, ModelAdmin
from task.models import Task


@register(Task)
class TaskAdmin(ModelAdmin):
    
    list_display = ['user', 'title', 'complete',
                    'description', 'created_time']
    list_display_links = ['title']
    search_fields = ['title', 'user__username', 'description']
    list_filter = ['complete']
