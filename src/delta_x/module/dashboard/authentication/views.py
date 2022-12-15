from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.edit import CreateView

from delta_x.module.email.tasks import send_email_reply
from delta_x.module.users.forms import CustomerCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

    def clean(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)

        if username and password:
            backend = AllowAllUsersModelBackend()
            self.user_cache = backend.authenticate(self.request, username=username, password=password)
            if not self.user_cache:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Please confirm your email so you can log in.",
                code='inactive',
            )


class SignUpViewSet(SuccessMessageMixin, CreateView):
    template_name = 'dashboard/accounts/register.html'
    success_url = reverse_lazy('dashboard:login')
    form_class = CustomerCreationForm
    success_message = "Your profile was created successfully"


class ResetForm(PasswordResetForm):
    def send_mail(self,
                  subject_template_name,
                  email_template_name,
                  context, from_email,
                  to_email,
                  html_email_template_name):
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        send_email_reply.apply_async(kwargs={
            "subject_template_name": subject,
            "email_template_name": body,
            "context": context,
            "from_email": from_email,
            "to_email": to_email,
            "html_email_template_name": html_email_template_name})

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = get_user_model().get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user.email,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )


class LoginViewSet(LoginView):
    authentication_form = LoginForm
    template_name = 'dashboard/accounts/login.html'
    next_page = reverse_lazy('dashboard:index')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class LogoutViewSet(LogoutView):
    next_page = reverse_lazy('dashboard:login')

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        auth_logout(self.request)
        if self.next_page:
            return resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return self.request.path


class ResetPasswordViewSet(SuccessMessageMixin, PasswordResetView):
    template_name = "dashboard/accounts/password_reset.html"
    email_template_name = 'dashboard/accounts/password_reset_email.html'
    subject_template_name = 'dashboard/accounts/password_reset_subject.txt'
    form_class = ResetForm
    from_email = settings.EMAIL_HOST_USER
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("dashboard:password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class PasswordResetConfirmViewSet(PasswordResetConfirmView):
    template_name = "dashboard/accounts/password_reset_confirm.html"


class PasswordResetCompleteViewSet(PasswordResetCompleteView):
    template_name = "dashboard/accounts/password_reset_complete.html"
