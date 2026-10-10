import os
import unittest
import tempfile
from app import app, init_db, get_db

class ApplyNowTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for testing
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms easily
        self.client = app.test_client()
        
        # Initialize the temporary database
        with app.app_context():
            init_db()

    def tearDown(self):
        # Close and remove the temporary database
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_home_page_get(self):
        """Test that the home page loads successfully via GET."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job Application', response.data)
        
    def test_valid_application_post(self):
        """Test submitting a valid application via POST."""
        form_data = {
            'full_name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'position': 'Python Developer',
            'experience_level': '3–5 Years', # Valid choice
            'cover_letter': 'This is a cover letter that is definitely longer than 30 characters and describes why I am a great fit for this position.',
            'consent': 'yes'
        }
        response = self.client.post('/apply', data=form_data)
        
        # Should redirect to success page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/application-success/AN-', response.headers['Location'])
        
        # Follow the redirect to check the success page
        success_response = self.client.get(response.headers['Location'])
        self.assertEqual(success_response.status_code, 200)
        self.assertIn(b'Application Submitted Successfully!', success_response.data)
        self.assertIn(b'Jane Doe', success_response.data)

    def test_missing_required_fields(self):
        """Test submitting with missing required fields."""
        response = self.client.post('/apply', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Full name must be at least 2 characters', response.data)

    def test_invalid_email(self):
        """Test submitting an invalid email format."""
        form_data = {
            'full_name': 'Jane Doe',
            'email': 'not-an-email',
            'position': 'Python Developer',
            'experience_level': '3-5 Years',
            'cover_letter': 'This is a valid cover letter but the email is wrong so it should fail.',
            'consent': 'yes'
        }
        response = self.client.post('/apply', data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please provide a valid email address.', response.data)
        
    def test_invalid_reference_404(self):
        """Test an unknown application reference returns 404."""
        response = self.client.get('/application-success/AN-INVALID123')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
