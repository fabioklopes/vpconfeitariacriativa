from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Pricing, FixedCost, ProLabore, History
from .middleware import get_current_user


def _create_history(instance, action, changes=None):
    user = get_current_user()
    try:
        model_name = instance.__class__.__name__
        object_repr = str(instance)
        History.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_repr=object_repr,
            changes=changes or {},
        )
    except Exception:
        # Avoid breaking business logic if history cannot be recorded
        pass


@receiver(post_save, sender=Pricing)
def pricing_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    _create_history(instance, action)


@receiver(post_delete, sender=Pricing)
def pricing_deleted(sender, instance, **kwargs):
    _create_history(instance, 'delete')


@receiver(post_save, sender=FixedCost)
def fixedcost_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    _create_history(instance, action)


@receiver(post_delete, sender=FixedCost)
def fixedcost_deleted(sender, instance, **kwargs):
    _create_history(instance, 'delete')


@receiver(post_save, sender=ProLabore)
def prolabore_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    _create_history(instance, action)


@receiver(post_delete, sender=ProLabore)
def prolabore_deleted(sender, instance, **kwargs):
    _create_history(instance, 'delete')
