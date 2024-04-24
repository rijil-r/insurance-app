import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ActivityTrackerMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(get_user_model()):
    date_of_birth = models.DateField()

    class Meta:
        verbose_name = 'Customer'

    @property
    def age(self):
        return datetime.date.today().year - self.date_of_birth.year


class Policy(ActivityTrackerMixin):
    policy_type = models.CharField(max_length=255, unique=True)
    age_multiplier = models.DecimalField(max_digits=10, decimal_places=2, default=0.02)
    premium_to_cover_ratio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.policy_type}"

    class Meta:
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'


class Quote(ActivityTrackerMixin):

    class Status(models.TextChoices):
        NEW = 'NEW', _('New')
        QUOTED = 'QUOTED', _('Quoted')
        ACTIVE = 'ACTIVE', _('Active')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    cover = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=Status.choices, default=Status.NEW, max_length=10)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.policy.policy_type} - {self.customer.first_name} {self.customer.last_name}"

    def save(self, *args, **kwargs):
        if not self.premium:
            self.premium = self.policy.premium_to_cover_ratio * self.cover
            self.premium += self.premium * self.policy.age_multiplier * self.customer.age
        # If status is being changed to ACTIVE, set valid_from and valid_to dates
        if self.status == self.Status.ACTIVE and not self.valid_from:
            self.valid_from = datetime.date.today()
            self.valid_to = self.valid_from + datetime.timedelta(days=365)
        super().save(*args, **kwargs)
