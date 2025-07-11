from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .supabase_client import get_supabase_client

@receiver(post_save, sender=User)   # whenever user is created, added or modified
def create_user_in_supabase(sender, instance, created, **kwargs):
    if created:
        print("SIGNAL TRIGGERED FOR USER:", instance.username)
        supabase = get_supabase_client()
        data = {
            "username": instance.username,
            "email": instance.email,
            "password": instance.password,
            "is_superuser": instance.is_superuser,
            "is_staff": instance.is_staff,
            "is_active": instance.is_active,
            "date_joined": instance.date_joined.isoformat(),
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "last_login": instance.last_login.isoformat() if instance.last_login else None
        }
        try:
            result = supabase.table("auth_user").insert(data).execute()
            print("Supabase user created:", result)
        except Exception as e:
            print("Supabase ERROR:", e)


def create_user_in_supabase(sender, instance, created, **kwargs):
    if created:
        print("SIGNAL TRIGGERED FOR USER:", instance.username)
        supabase = get_supabase_client()
        data = {
            "username": instance.username,
            "email": instance.email,
            "password": instance.password,
            "is_superuser": instance.is_superuser,
            "is_staff": instance.is_staff,
            "is_active": instance.is_active,
            "date_joined": instance.date_joined.isoformat(),
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "last_login": instance.last_login.isoformat() if instance.last_login else None
        }
        try:
            result = supabase.table("auth_user").insert(data).execute()
            print("Supabase user created:", result)
        except Exception as e:
            print("Supabase ERROR:", e)