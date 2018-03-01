import requests
import urllib


class FitBit:
    """Class to handle all fitbit operation"""

    # App settings from fitbit as regards the app
    CLIENT_ID = '22CMV9'
    CLIENT_SECRET = '7a9eedc7247ef8e4c64d896aeb9a06f6'

    AUTHORIZE_URI = 'https://www.fitbit.com/oauth2/authorize'
    TOKEN_REQUEST_URI = 'https://api.fitbit.com/oauth2/token'

    def ComposeAuthorizationURI(self, scope, REDIRECT_URI):
        """Method helps to compose authorization uri with the intended params"""

        # parameters for authorization
        params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': REDIRECT_URI
        }

        # encode the parameters
        urlparams = urllib.parse.urlencode(params)
        # construct and return authorization_uri
        return self.AUTHORIZE_URI + '?' + urlparams

    def RequestAccessToken(self, code, REDIRECT_URI):
        """Method to get exchange access_code with access token from fitbits"""

        # Authentication header
        client_id = self.CLIENT_ID.encode('utf-8')
        secret = self.CLIENT_SECRET.encode('utf-8')

        headers = {
            'Authorization': 'Basic MjJDTVY5OjdhOWVlZGM3MjQ3ZWY4ZTRjNjRkODk2YWViOWEwNmY2',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # parameters for requesting tokens
        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': REDIRECT_URI
        }

        # request for token
        response = requests.post(
            self.TOKEN_REQUEST_URI,
            data=params,
            headers=headers)

        if response.status_code != 200:
            raise Exception("Action unsuccessful " + str(response.status_code))

        # get the tokens
        response = response.json()
        token = dict()
        token['access_token'] = response['access_token']
        token['refresh_token'] = response['refresh_token']

        return token

    def RefreshToken(self, token):
        """ Refresh expired access token """

        # authentication header
        client_id = self.CLIENT_ID.encode('utf-8')
        secret = self.CLIENT_SECRET.encode('utf-8')
        headers = {
            'Authorization': 'Basic MjJDTVY5OjdhOWVlZGM3MjQ3ZWY4ZTRjNjRkODk2YWViOWEwNmY2DQo=',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # parameters for refresh token request
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token['refresh_token']
        }

        # request for token
        response = requests.post(self.TOKEN_REQUEST_URL, data=params, headers=headers)

        if response.status_code != 200:
            raise Exception("Action unsuccessful")

        # replace tokens
        token['access_token'] = response.access_token
        token['refresh_token'] = response.refresh_token

        return token

    def fitbit_sync(self, token):
        """Method makes weight call to API"""

        headers = {
            'Authorization': 'Bearer ' + token['access_token']
        }

        url = 'https://api.fitbit.com/1/user/-/body/weight/date/today/1d.json'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            token = self.RefreshToken(token)
            self.fitbit_sync(token)
        else:
            raise Exception("Action unsuccessful")

    def fitbit_act(self, token):
        """Method makes activity call to API"""

        headers = {
            'Authorization': 'Bearer ' + token['access_token']
        }

        url = 'https://api.fitbit.com/1/user/-/activities/date/2018-03-02.json'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            token = self.RefreshToken(token)
            self.fitbit_act(token)
        else:
            raise Exception("Action unsuccessful")
