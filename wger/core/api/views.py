# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import User
from django.utils import translation
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit)
from wger.config.models import GymConfig
from wger.gym.models import (
    AdminUserNote,
    GymUserConfig,
    Contract
)
from wger.core.api.serializers import (
    UsernameSerializer, LanguageSerializer, DaysOfWeekSerializer,
    LicenseSerializer, RepetitionUnitSerializer, WeightUnitSerializer,
    UserCreationSerializer, UserprofileSerializer)
from wger.utils.permissions import (UpdateOnlyPermission, WgerPermission, CreateUsersViaAPI)


class UserRegisterViewSet(viewsets.ModelViewSet):

    '''
    API endpoint for user registration
    '''
    serializer_class = UserCreationSerializer
    permission_classes = (CreateUsersViaAPI,)
    queryset = User.objects.all()

    def perform_create(self, request):
        """
        Create user from API
        """
        creator = UserProfile.objects.get(user=self.request.user)

        # Check if they can be allowed to create users
        if creator and creator.can_add_user:
            serialized = self.get_serializer(data=self.request.data)
            if serialized.is_valid():
                username = serialized.data['username']
                email = serialized.data['email']
                password = self.request.data['password']

                api_user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=password)
                api_user.save()
                api_user.userprofile.added_by = creator.user.username
                api_user.userprofile.save()

                language = Language.objects.get(
                    short_name=translation.get_language())
                api_user.userprofile.notification_language = language
                # Set default gym, if needed
                gym_config = GymConfig.objects.get(pk=1)
                if gym_config.default_gym:
                    api_user.userprofile.gym = gym_config.default_gym

                    # Create gym user configuration object
                    config = GymUserConfig()
                    config.gym = gym_config.default_gym
                    config.user = api_user
                    config.save()

                return Response({'detail': 'User created successfully'}, status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Please check the credentials and try again'},
                                status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'detail': 'Application not allowed to access this resource'},
                            status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for workout objects
    '''
    is_private = True
    serializer_class = UserprofileSerializer
    permission_classes = (WgerPermission, UpdateOnlyPermission)
    ordering_fields = '__all__'

    def get_queryset(self):
        '''
        Only allow access to appropriate objects
        '''
        return UserProfile.objects.filter(user=self.request.user)

    def get_owner_objects(self):
        '''
        Return objects to check for ownership permission
        '''
        return [(User, 'user')]

    @detail_route()
    def username(self, request, pk):
        '''
        Return the username
        '''

        user = self.get_object().user
        return Response(UsernameSerializer(user).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name', 'short_name')


class DaysOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = DaysOfWeek.objects.all()
    serializer_class = DaysOfWeekSerializer
    ordering_fields = '__all__'
    filter_fields = ('day_of_week', )


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for workout objects
    '''
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name', 'short_name', 'url')


class RepetitionUnitViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for repetition units objects
    '''
    queryset = RepetitionUnit.objects.all()
    serializer_class = RepetitionUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class WeightUnitViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for weight units objects
    '''
    queryset = WeightUnit.objects.all()
    serializer_class = WeightUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )
