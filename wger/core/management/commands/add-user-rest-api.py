from optparse import make_option
from django.core.management.base import BaseCommand
from wger.core.models import UserProfile, User
from django.contrib.auth import authenticate
'''
Custom command permitting users to create user accounts
'''


class Command(BaseCommand):
    '''
    Enables a user to create other users via the API
    '''

    option_list = BaseCommand.option_list + (
        make_option(
            '--username',
            action='store_true',
            dest='username',
            default=False,
            help='username of user to receive permissions'
        ),
        make_option(
            '--password',
            action='store_true',
            dest='password',
            default=False,
            help='password of user to give permissions'
        )
    )

    help = '''Permit user to create user accounts

        Example:
        python manage.py add-user-rest-api <username> --username --password <password>
    '''

    def handle(self, *args, **options):
        self.stdout.write('** Updating User permissions')
        if (options.get('username') & options.get('password')) is False:
            self.stdout.write('Please select both --username and --password')
            return
        try:
            name = options.get('username')
            username = str(args[0])
            password = options.get('password')
            password = str(args[1])
        except IndexError:
            self.stdout.write('Please provide both the username and admin\'s password')
            return

        admin = authenticate(username='admin', password=password)
        if admin:
            print("Admin has been authenticated. Authorizing {0}".format(name))

        if admin is not None:
            self.stdout.write('username: {}'.format(username))
            try:
                user = User.objects.get(username=username)
                user_profile = user.userprofile
                user_profile.can_create_users_via_api = True
                user_profile.save()
                self.stdout.write(
                    'User permissions for {} successfully updated'.format(
                        username
                    )
                )
                return
            except User.DoesNotExist:
                self.stdout.write('Please supply valid username')
                return
        else:
            self.stdout.write('Admin not authorized. Provide correct password')
