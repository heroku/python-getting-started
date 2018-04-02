"""All application views."""

from django.views.generic.base import TemplateView

from horecatm.models import User


class BaseContextMixin(TemplateView):
    """View mixin for getting base template data."""

    def get_context_data(self, **kwargs):
        """Extend for getting users list."""
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_superuser=False)
        return context


class UserView(BaseContextMixin):
    """User template."""

    model = User
    fields = ('first_name', 'last_name', 'avatar')
    template_name = "user_form.html"
