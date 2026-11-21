from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

from cases.models import CaseRecord, Sample
from reviews.models import ReviewRecord
from auditlog.models import AuditEvent


class ReviewWorkflowTests(TestCase):
    def setUp(self):
        self.fo_group = Group.objects.create(name='Field Officer')
        self.sup_group = Group.objects.create(name='Supervisor')

        self.officer = User.objects.create_user(
            username='officer_review_test',
            password='TestPassword123!'
        )
        self.officer.groups.add(self.fo_group)

        self.supervisor = User.objects.create_user(
            username='supervisor_review_test',
            password='TestPassword123!'
        )
        self.supervisor.groups.add(self.sup_group)

        self.case = CaseRecord.objects.create(
            case_reference='CASE-REV-01',
            title='Supervisory Workflow Case',
            incident_datetime=timezone.now(),
            general_location='Inspection Station',
            description='Awaiting supervisor evaluation.',
            status=CaseRecord.STATUS_SUBMITTED,
            created_by=self.officer
        )
        self.sample = Sample.objects.create(
            sample_code='SMP-REV-001',
            case=self.case,
            collected_at=timezone.now(),
            description='Test sample for review',
            packaging_reference='Pouch 1',
            seal_reference='SEAL-REV',
            initial_condition='Intact',
            created_by=self.officer
        )

        self.client = Client()
        self.client.login(username='supervisor_review_test', password='TestPassword123!')

    def test_at09_supervisor_returns_case_without_comment_rejected(self):
        """AT-09: Supervisor returns a case without a comment. Action is rejected; comment is required."""
        review_url = reverse('review_create', kwargs={'case_id': self.case.pk})

        response = self.client.post(review_url, {
            'decision': ReviewRecord.DECISION_CHANGES_REQUESTED,
            'comment': '',  # Empty comment
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'comment',
            'A supervisory review comment is strictly mandatory.'
        )

        # Status must remain unchanged
        self.case.refresh_from_db()
        self.assertEqual(self.case.status, CaseRecord.STATUS_SUBMITTED)
        self.assertEqual(ReviewRecord.objects.count(), 0)

    def test_at10_supervisor_approves_submitted_case(self):
        """AT-10: Supervisor approves a submitted case. Status changes to Approved and review history is retained."""
        review_url = reverse('review_create', kwargs={'case_id': self.case.pk})

        response = self.client.post(review_url, {
            'decision': ReviewRecord.DECISION_APPROVED,
            'comment': 'Presumptive test results and custody events fully verified and compliant with SOP.',
        })
        self.assertEqual(response.status_code, 302)

        # Verify case status transitioned to Approved
        self.case.refresh_from_db()
        self.assertEqual(self.case.status, CaseRecord.STATUS_APPROVED)

        # Verify ReviewRecord is retained
        review = ReviewRecord.objects.filter(case=self.case).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.decision, ReviewRecord.DECISION_APPROVED)
        self.assertEqual(review.reviewer, self.supervisor)
        self.assertIn("fully verified", review.comment)

        # Verify AuditEvent logged
        audit = AuditEvent.objects.filter(action='REVIEW_APPROVED', object_id=str(review.pk)).first()
        self.assertIsNotNone(audit)
        self.assertEqual(audit.actor, self.supervisor)

    def test_field_officer_cannot_review_case(self):
        """Field Officer role cannot perform supervisory review."""
        fo_client = Client()
        fo_client.login(username='officer_review_test', password='TestPassword123!')
        review_url = reverse('review_create', kwargs={'case_id': self.case.pk})

        response = fo_client.get(review_url)
        self.assertEqual(response.status_code, 403)
