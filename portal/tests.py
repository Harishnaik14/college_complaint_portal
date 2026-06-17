from django.test import TestCase
from django.urls import reverse
from .forms import AnnouncementForm, ComplaintForm
from .models import Complaint


class ComplaintFormTests(TestCase):
    def test_form_requires_subject_and_description(self):
        form = ComplaintForm(data={
            'category': 'Facilities',
            'subject': '',
            'description': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('description', form.errors)


class AnnouncementFormTests(TestCase):
    def test_form_requires_title_and_message(self):
        form = AnnouncementForm(data={
            'title': '',
            'message': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('message', form.errors)


class PortalAccessTests(TestCase):
    def test_home_redirects_non_admin_to_submit_page(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('submit_complaint'))


class ComplaintModelTests(TestCase):
    def test_default_status_is_pending(self):
        complaint = Complaint.objects.create(
            category='Facilities',
            subject='Test Subject',
            description='Need maintenance.'
        )
        self.assertEqual(complaint.status, 'Pending')
