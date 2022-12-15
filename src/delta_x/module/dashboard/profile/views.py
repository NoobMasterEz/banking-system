from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from delta_x.module.users.forms import CustomerChangeForm
from delta_x.module.users.models import Customer


class ProfileViews(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/accounts/profile.html'
    login_url = reverse_lazy('dashboard:login')
    form_class = CustomerChangeForm

    def get_queryset(self):
        queryset = Customer.objects.all()
        return queryset

    def get_success_url(self):
        return reverse('dashboard:profile', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        customer = Customer.objects.filter(user__id=self.request.user.id).first()
        context = super().get_context_data(**kwargs)
        context['customer_form'] = CustomerChangeForm(initial={
            'address': customer.address,
            'identity_number': customer.identity_number,
            'gender': customer.gender,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
