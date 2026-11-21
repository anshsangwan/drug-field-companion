from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date

from cases.models import CaseRecord, Sample
from testing_records.models import TestKit, TestEvent, PRESUMPTIVE_DISCLAIMER
from testing_records.forms import TestEventForm


class TestingRecordsTests(TestCase):
    def setUp(self):
        self.fo_group = Group.objects.create(name='Field Officer')
        self.officer = User.objects.create_user(
            username='officer_testing',
            password='TestPassword123!'
        )
        self.officer.groups.add(self.fo_group)

        self.case = CaseRecord.objects.create(
            case_reference='CASE-TEST-TESTING',
            title='Presumptive Testing Case',
            incident_datetime=timezone.now(),
            general_location='Inspection Dock',
            description='Field presumptive screening tests.',
            status=CaseRecord.STATUS_DRAFT,
            created_by=self.officer
        )
        self.sample = Sample.objects.create(
            sample_code='SMP-TEST-001',
            case=self.case,
            collected_at=timezone.now(),
            description='Test sample for screening',
            packaging_reference='Bag 1',
            seal_reference='SEAL-88',
            initial_condition='Intact',
            created_by=self.officer
        )
        self.kit = TestKit.objects.create(
            name='Marquis Field Reagent',
            manufacturer='Forensic Labs',
            category='Colorimetric',
            catalogue_reference='CAT-MQ-01',
            active=True
        )

        self.client = Client()
        self.client.login(username='officer_testing', password='TestPassword123!')

    def test_at06_add_test_event_with_allowed_result_category(self):
        """AT-06: Add test event with an allowed result category. Event is linked to correct sample and disclaimer is visible."""
        # 1. Check GET form contains presumptive disclaimer
        form_url = reverse('test_event_create', kwargs={'sample_id': self.sample.pk})
        get_response = self.client.get(form_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, PRESUMPTIVE_DISCLAIMER)

        # 2. POST valid test event with 'Presumptive positive'
        performed_time = timezone.now()
        post_response = self.client.post(form_url, {
            'kit': self.kit.pk,
            'kit_lot_number': 'LOT-TEST-001',
            'kit_expiry_date': (performed_time.date() + timedelta(days=365)).strftime('%Y-%m-%d'),
            'performed_at': performed_time.strftime('%Y-%m-%dT%H:%M'),
            'observation_notes': 'Distinct purple color shift in 10 seconds.',
            'result_category': TestEvent.RESULT_PRESUMPTIVE_POSITIVE,
            'limitations_note': 'Conducted under direct sunlight.',
        })
        self.assertEqual(post_response.status_code, 302)

        # 3. Verify event is properly saved and linked to sample
        test_event = TestEvent.objects.filter(sample=self.sample).first()
        self.assertIsNotNone(test_event)
        self.assertEqual(test_event.result_category, TestEvent.RESULT_PRESUMPTIVE_POSITIVE)
        self.assertEqual(test_event.kit, self.kit)
        self.assertEqual(test_event.performed_by, self.officer)

        # 4. Verify specimen detail page displays the disclaimer and result
        sample_resp = self.client.get(reverse('sample_detail', kwargs={'pk': self.sample.pk}))
        self.assertEqual(sample_resp.status_code, 200)
        self.assertContains(sample_resp, PRESUMPTIVE_DISCLAIMER)
        self.assertContains(sample_resp, 'Presumptive positive')

    def test_at07_submit_result_outside_defined_choices_rejected(self):
        """AT-07: Attempt to submit a result outside defined choices. Server-side validation rejects it."""
        form_url = reverse('test_event_create', kwargs={'sample_id': self.sample.pk})
        response = self.client.post(form_url, {
            'kit': self.kit.pk,
            'kit_lot_number': 'LOT-INVALID',
            'kit_expiry_date': (timezone.now().date() + timedelta(days=100)).strftime('%Y-%m-%d'),
            'performed_at': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'observation_notes': 'Testing invalid choice',
            'result_category': 'Confirmed 100% Illegal Substance',  # Invalid unapproved choice!
            'limitations_note': '',
        })
        # Server-side validation rejects and re-renders form with error
        self.assertEqual(response.status_code, 200)
        self.assertIn('result_category', response.context['form'].errors)
        self.assertTrue(any('Select a valid choice' in err for err in response.context['form'].errors['result_category']))
        self.assertFalse(TestEvent.objects.filter(result_category='Confirmed 100% Illegal Substance').exists())

    def test_expired_kit_requires_limitations_note(self):
        """Test that using an expired kit requires explicit justification in limitations_note."""
        yesterday = timezone.now().date() - timedelta(days=10)
        performed_time = timezone.now()

        form = TestEventForm(data={
            'kit': self.kit.pk,
            'kit_lot_number': 'LOT-EXPIRED',
            'kit_expiry_date': yesterday.strftime('%Y-%m-%d'),
            'performed_at': performed_time.strftime('%Y-%m-%dT%H:%M'),
            'observation_notes': 'Ampoule crushed',
            'result_category': TestEvent.RESULT_INCONCLUSIVE,
            'limitations_note': '',  # Empty limitations note on expired kit
        })
        self.assertFalse(form.is_valid())
        self.assertIn('limitations_note', form.errors)
        self.assertIn('expired', form.errors['limitations_note'][0].lower())
