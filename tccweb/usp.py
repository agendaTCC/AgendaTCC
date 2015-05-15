from xml.dom import minidom

from social.backends.oauth import BaseOAuth1


class USPOAuth(BaseOAuth1):
    """TripIt OAuth authentication backend"""
    name = 'usp'
    AUTHORIZATION_URL = 'http://127.0.0.1:5000/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://127.0.0.1:5000/oauth/request_token'
    ACCESS_TOKEN_URL = 'hhttp://127.0.0.1:5000/oauth/access_token'
    EXTRA_DATA = [('screen_name', 'screen_name')]

    def get_user_details(self, response):
        """Return user details from TripIt account"""
        try:
            first_name, last_name = response['name'].split(' ', 1)
        except ValueError:
            first_name = response['name']
            last_name = ''
        return {'username': response['screen_name'],
                'email': response['email'],
                'fullname': response['name'],
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        url = 'https://api.tripit.com/v1/get/profile'
        request = self.oauth_request(access_token, url)
        content = self.fetch_response(request)
        try:
            dom = minidom.parseString(content)
        except ValueError:
            return None

        return {
            'id': dom.getElementsByTagName('Profile')[0].getAttribute('ref'),
            'name': dom.getElementsByTagName(
                'public_display_name')[0].childNodes[0].data,
            'screen_name': dom.getElementsByTagName(
                'screen_name')[0].childNodes[0].data,
            'email': dom.getElementsByTagName(
                'is_primary')[0].parentNode.getElementsByTagName(
                'address')[0].childNodes[0].data,
        }