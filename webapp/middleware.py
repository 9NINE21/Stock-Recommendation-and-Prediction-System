from django.shortcuts import redirect
from django.urls import reverse

class CheckAgreementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip if user is not authenticated
        if request.user.is_authenticated:
            # Check if the request is for the admin area
            if request.path.startswith('/admin/'):
                # Allow access to all admin URLs
                return self.get_response(request)
            
            # Check if user has agreed to terms in the session
            if not request.session.get('has_agreed_to_terms', False):
                # Allow access to the agreement page or logout, but restrict other pages
                allowed_paths = [
                    reverse('user-agreement'),
                    reverse('user-logout'),  # Add logout or other non-restricted URLs here
                ]
                if request.path not in allowed_paths:
                    return redirect('user-agreement')

        response = self.get_response(request)
        return response

