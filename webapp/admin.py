from django.contrib import admin
from .models import QuestionnaireSubmission

@admin.register(QuestionnaireSubmission)
class QuestionnaireSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'market_cap', 'investment_amount', 'investment_preference', 'risk_appetite', 'investment_duration', 'recommendations','clicked_stock','submitted_at')
    search_fields = ('user__username', 'market_cap')  # Add searchable fields
    list_filter = ('market_cap', 'risk_appetite')  # Add filters
    readonly_fields = ('user', 'market_cap', 'investment_amount', 'investment_preference', 'risk_appetite', 
                       'investment_duration', 'recommendations', 'clicked_stock', 'submitted_at')
    # readonly_fields = ('recommendations',)

    def recommendations_list(self, obj):
        return ', '.join(obj.get_recommendations())
