from allauth.account.adapter import DefaultAccountAdapter

class NoSignupAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to disable user signup/registration.
    """
    def is_open_for_signup(self, request):
        return False
