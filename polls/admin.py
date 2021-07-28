from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    actions = ['make_published']

    @admin.action(description='Mark select questions')
    def make_published(self, request, queryset):
        updated = queryset.update(status='q')
        self.message_user(request, ngettext(
            messages.success(request, '%d questions were successfully selected.'),
            messages.warning(request, 'Not all questions selected'),
            messages.error(request, 'None of the questions were selected'),
            updated,
        ) % updated, messages.SUCCESS)
        

admin.site.register(Question, QuestionAdmin)