"""For adding features in admin."""
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Align the editing choices to be inline."""

    model = Choice
    extra = 3

    class ChoiceInline(admin.StackedInline):
        """Align the editing choice to be inline."""

        model = Choice
        extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Configuration for showing information on the admin page."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['publication_date', 'end_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'publication_date', 'was_published_recently')
    list_filter = ['publication_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
