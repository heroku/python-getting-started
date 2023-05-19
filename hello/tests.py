from django.test import TestCase

# Create your tests here.


# Note: The tests below rely upon static assets (for the rendered templates), so require that either:
# 1. The static assets have been processed - ie: `./manage.py collectstatic` has been run.
# 2. Or, the tests are run in debug mode (which means WhiteNoise will use auto-refresh mode),
#    using: `./manage.py test --debug-mode`
class ExampleTest(TestCase):
    def test_index_page(self):
        response = self.client.get("/")
        self.assertContains(
            response, "Getting Started with Python on Heroku", status_code=200
        )

    def test_db_page(self):
        # Each time the page is requested, the number of recorded greetings increases.

        first_response = self.client.get("/db/")
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(len(first_response.context["greetings"]), 1)

        second_response = self.client.get("/db/")
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(len(second_response.context["greetings"]), 2)
