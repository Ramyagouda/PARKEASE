"""Create a Django superuser non-interactively for demo purposes."""
import os
import django


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_parking.settings')
    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'Admin123!'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created with password '{password}'")
    else:
        print(f"Superuser '{username}' already exists")


if __name__ == '__main__':
    main()
