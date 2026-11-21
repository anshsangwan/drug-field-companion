from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from cases.models import CaseRecord, Sample
from cases.forms import CaseRecordForm, SampleForm
from auditlog.models import AuditEvent
from testing_records.models import TestKit, TestEvent, PRESUMPTIVE_DISCLAIMER
from custody.models import CustodyEvent
from reviews.models import ReviewRecord


class CaseManagementTests(TestCase):
    def setUp(self):
        self.fo_group = Group.objects.create(name='Field Officer')
        self.sup_group = Group.objects.create(name='Supervisor')

        self.officer = User.objects.create_user(
            username='officer_case_test',
            password='TestPassword123!'
        )
        self.officer.groups.add(self.fo_group)

        self.supervisor = User.objects.create_user(
            username='supervisor_case_test',
            password='TestPassword123!'
        )
        self.supervisor.groups.add(self.sup_group)

        self.client = Client()
        self.client.login(username='officer_case_test', password='TestPassword123!')

    def test_at04_create_case_missing_required_field(self):
        """AT-04: Create case with missing required field. Form re-renders with field error; no invalid case saved."""
        initial_count = CaseRecord.objects.count()
        # Missing 'title' and 'incident_datetime'
        response = self.client.post(reverse('case_create'), {
            'title': '',
            'incident_datetime': '',
            'general_location': 'Interstate 95',
            'description': 'Routine inspection',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'title', 'This field is required.')
        self.assertFormError(response.context['form'], 'incident_datetime', 'This field is required.')
        self.assertEqual(CaseRecord.objects.count(), initial_count)

    def test_at05_create_two_samples_with_same_sample_code(self):
        """AT-05: Create two samples with same sample code. Second save is rejected with clear uniqueness error."""
        case = CaseRecord.objects.create(
            case_reference='CASE-TEST-0001',
            title='Sample Uniqueness Case',
            incident_datetime=timezone.now(),
            general_location='Test Terminal',
            description='Testing uniqueness of sample codes.',
            status=CaseRecord.STATUS_DRAFT,
            created_by=self.officer
        )

        # 1. Create first sample with code 'SMP-UNIQUE-001'
        sample1 = Sample.objects.create(
            sample_code='SMP-UNIQUE-001',
            case=case,
            collected_at=timezone.now(),
            description='First package',
            packaging_reference='Bag A',
            seal_reference='SEAL-111',
            initial_condition='Intact',
            created_by=self.officer
        )
        self.assertTrue(sample1.pk)

        # 2. Attempt to create second sample with identical code via form
        form_data = {
            'sample_code': 'SMP-UNIQUE-001',
            'collected_at': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'description': 'Second duplicate package',
            'packaging_reference': 'Bag B',
            'seal_reference': 'SEAL-222',
            'initial_condition': 'Intact',
        }
        form = SampleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('sample_code', form.errors)
        self.assertIn("already registered", form.errors['sample_code'][0])

        # Also test via web view POST
        response = self.client.post(reverse('sample_create', kwargs={'case_id': case.pk}), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already registered")
        self.assertEqual(Sample.objects.filter(sample_code='SMP-UNIQUE-001').count(), 1)

    def test_at08_submit_case_for_review(self):
        """AT-08: Submit a case for review. Status changes to Submitted and audit event is created."""
        case = CaseRecord.objects.create(
            case_reference='CASE-TEST-SUBMIT',
            title='Submittable Case',
            incident_datetime=timezone.now(),
            general_location='Checkpoint Alpha',
            description='Ready for submission.',
            status=CaseRecord.STATUS_DRAFT,
            created_by=self.officer
        )
        # Add sample so submission is permitted
        Sample.objects.create(
            sample_code='SMP-SUBMIT-001',
            case=case,
            collected_at=timezone.now(),
            description='Sample under submittable case',
            packaging_reference='Pouch 1',
            seal_reference='SEAL-SUB',
            initial_condition='Intact',
            created_by=self.officer
        )

        submit_resp = self.client.post(reverse('case_submit', kwargs={'pk': case.pk}))
        self.assertEqual(submit_resp.status_code, 302)

        case.refresh_from_db()
        self.assertEqual(case.status, CaseRecord.STATUS_SUBMITTED)

        # Verify audit event
        audit = AuditEvent.objects.filter(object_id=str(case.pk), action='SUBMIT').first()
        self.assertIsNotNone(audit)
        self.assertEqual(audit.actor, self.officer)
        self.assertIn("submitted for supervisory review", audit.summary)

    def test_at13_open_case_report(self):
        """AT-13: Open a case report. Report contains case/sample/test/custody/review data and presumptive disclaimer."""
        case = CaseRecord.objects.create(
            case_reference='CASE-TEST-REP',
            title='Full Report Demonstration Case',
            incident_datetime=timezone.now(),
            general_location='Warehouse 7B',
            description='Incident requiring full report generation.',
            status=CaseRecord.STATUS_APPROVED,
            created_by=self.officer
        )
        sample = Sample.objects.create(
            sample_code='SMP-REP-001',
            case=case,
            collected_at=timezone.now(),
            description='Crystalline evidentiary specimen',
            packaging_reference='Evidence Box #9',
            seal_reference='SEAL-REP-44',
            initial_condition='Dry and sealed',
            created_by=self.officer
        )
        kit = TestKit.objects.create(
            name='Test Cobalt Kit',
            manufacturer='Test Labs Inc',
            category='Colorimetric',
            catalogue_reference='CAT-TEST-01',
            active=True
        )
        TestEvent.objects.create(
            sample=sample,
            kit=kit,
            kit_lot_number='LOT-REP-1',
            kit_expiry_date=timezone.now().date() + timedelta(days=365),
            performed_at=timezone.now(),
            performed_by=self.officer,
            observation_notes='Blue color reaction recorded',
            result_category='Presumptive positive'
        )
        CustodyEvent.objects.create(
            sample=sample,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=timezone.now(),
            from_person='Warehouse Scene',
            to_person='Officer Chen',
            location_reference='Warehouse 7B',
            seal_reference='SEAL-REP-44',
            remarks='Initial collection',
            recorded_by=self.officer
        )
        ReviewRecord.objects.create(
            case=case,
            reviewer=self.supervisor,
            decision=ReviewRecord.DECISION_APPROVED,
            comment='Formally reviewed and endorsed for laboratory submission.'
        )

        response = self.client.get(reverse('case_report', kwargs={'pk': case.pk}))
        self.assertEqual(response.status_code, 200)

        # Check all required sections and disclaimer
        self.assertContains(response, 'CASE-TEST-REP')
        self.assertContains(response, 'SMP-REP-001')
        self.assertContains(response, 'Test Cobalt Kit')
        self.assertContains(response, 'Presumptive positive')
        self.assertContains(response, 'SEAL-REP-44')
        self.assertContains(response, 'Formally reviewed and endorsed')
        self.assertContains(response, PRESUMPTIVE_DISCLAIMER)

    def test_at14_post_without_csrf_token_rejected(self):
        """AT-14: Submit a POST form without CSRF token. Django rejects the request."""
        # Use Client with enforce_csrf_checks=True
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='officer_case_test', password='TestPassword123!')

        # Make raw post without csrf token
        response = csrf_client.post(reverse('case_create'), {
            'title': 'CSRF Attack Test Case',
            'incident_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'general_location': 'Unknown',
            'description': 'Attempting post without csrf',
        })
        # Django rejects with 403 Forbidden
        self.assertEqual(response.status_code, 403)
