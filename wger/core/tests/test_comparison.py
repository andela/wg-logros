from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerTestCase


def comparison(self):
    '''
    Helper function to test the comparison page
    '''
    response = self.client.get(
        reverse('core:comparison'))
    self.assertEqual(response.status_code, 200)
