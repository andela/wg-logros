from django.core.urlresolvers import reverse


def comparison(self):
    '''
    Helper function to test the comparison page
    '''
    response = self.client.get(
        reverse('core:comparison'))
    self.assertEqual(response.status_code, 200)
