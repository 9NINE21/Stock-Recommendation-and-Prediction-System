from django.db import models
from django.contrib.auth.models import User  # Optional if linking submissions to users
import json

class QuestionnaireSubmission(models.Model):
    MARKET_CAP_CHOICES = [
        ('Largecap', 'Large-cap'),
        ('Midcap', 'Mid-cap'),
        ('Smallcap', 'Small-cap'),
    ]

    INVESTMENT_AMOUNT_CHOICES = [
        ('Low-Price', 'Less than NPR 25,000'),
        ('Mid-Price', 'NPR 25,000 – NPR 40,000'),
        ('High-Price', 'More than NPR 40,000'),
    ]

    INVESTMENT_PREFERENCE_CHOICES = [
        ('HighGrowthPotential', 'High Growth Potential'),
        ('UndervaluedwithStableReturns', 'Undervalued with Stable Returns'),
    ]

    RISK_APPETITE_CHOICES = [
        ('Low', 'Low (prefer stable, low-volatility stocks)'),
        ('Medium', 'Moderate (willing to accept some risk for potential returns)'),
        ('High', 'High (comfortable with high risk for higher returns)'),
    ]

    INVESTMENT_DURATION_CHOICES = [
        ('Shortterm', 'Short-term investment (1-2 years)'),
        ('Longterm', 'Long-term investment (over 2 years)'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional
    market_cap = models.CharField(max_length=50, choices=MARKET_CAP_CHOICES)
    investment_amount = models.CharField(max_length=50, choices=INVESTMENT_AMOUNT_CHOICES)
    investment_preference = models.CharField(max_length=50, choices=INVESTMENT_PREFERENCE_CHOICES)
    risk_appetite = models.CharField(max_length=50, choices=RISK_APPETITE_CHOICES)
    investment_duration = models.CharField(max_length=50, choices=INVESTMENT_DURATION_CHOICES)
    recommendations = models.TextField(null=True, blank=True)
    clicked_stock = models.CharField(max_length=100, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def set_recommendations(self, stock_list):
        """Store recommendations as a JSON string."""
        self.recommendations = json.dumps(stock_list)

    def get_recommendations(self):
        """Retrieve recommendations as a Python list."""
        if self.recommendations:
            return json.loads(self.recommendations)
        return []
    
    def __str__(self):
        return f"Submission by {self.user.username if self.user else 'Anonymous'} on {self.submitted_at}"
