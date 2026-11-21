from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from cases.models import CaseRecord, Sample
from custody.models import CustodyEvent


class CustodyTests(TestCase):
    def setUp(self):
        self.fo_group = Group.objects.create(name='Field Officer')
        self.officer = User.objects.create_user(
            username='officer_custody',
            password='TestPassword123!'
        )
        self.officer.groups.add(self.fo_group)

        self.case = CaseRecord.objects.create(
            case_reference='CASE-CUSTODY-01',
            title='Chain of Custody Verification Case',
            incident_datetime=timezone.now(),
            general_location='Patrol Station',
            description='Tracking custody ledger.',
            status=CaseRecord.STATUS_DRAFT,
            created_by=self.officer
        )
        self.sample = Sample.objects.create(
            sample_code='SMP-CUSTODY-01',
            case=self.case,
            collected_at=timezone.now(),
            description='Specimen for custody tracking',
            packaging_reference='Evidence Bag 99',
            seal_reference='SEAL-CUST-1',
            initial_condition='Intact',
            created_by=self.officer
        )

        self.client = Client()
        self.client.login(username='officer_custody', password='TestPassword123!')

    def test_at11_add_custody_events_in_chronological_order(self):
        """AT-11: Add custody events. Events appear in chronological order with actor and timestamps."""
        t1 = timezone.now() - timedelta(hours=3)
        t2 = timezone.now() - timedelta(hours=1)

        # Event 1: Initial Collection at t1
        e1 = CustodyEvent.objects.create(
            sample=self.sample,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=t1,
            from_person='Scene Location',
            to_person='Officer Marcus Chen',
            location_reference='Mile 42 Station',
            seal_reference='SEAL-CUST-1',
            remarks='First collection',
            recorded_by=self.officer
        )

        # Event 2: Transfer to Vault at t2
        url = reverse('custody_event_create', kwargs={'sample_id': self.sample.pk})
        response = self.client.post(url, {
            'event_type': CustodyEvent.TYPE_STORED,
            'event_at': t2.strftime('%Y-%m-%dT%H:%M'),
            'from_person': 'Officer Marcus Chen',
            'to_person': 'Custodian Gomez',
            'location_reference': 'Central Evidence Vault Locker #5',
            'seal_reference': 'SEAL-CUST-1',
            'remarks': 'Secured in locker',
        })
        self.assertEqual(response.status_code, 302)

        # Query events from sample
        events = list(self.sample.custody_events.order_by('event_at'))
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].event_type, CustodyEvent.TYPE_COLLECTION)
        self.assertEqual(events[1].event_type, CustodyEvent.TYPE_STORED)
        self.assertEqual(events[1].recorded_by, self.officer)
        self.assertFalse(events[1].is_out_of_sequence)

        # Detail page renders events in order
        sample_resp = self.client.get(reverse('sample_detail', kwargs={'pk': self.sample.pk}))
        self.assertEqual(sample_resp.status_code, 200)
        self.assertContains(sample_resp, 'Scene Location')
        self.assertContains(sample_resp, 'Central Evidence Vault Locker #5')

    def test_out_of_sequence_custody_event_flagged(self):
        """Custody event timestamp earlier than prior event should be flagged as out of sequence."""
        t_later = timezone.now()
        t_earlier = timezone.now() - timedelta(hours=5)

        # Create later event first
        CustodyEvent.objects.create(
            sample=self.sample,
            event_type=CustodyEvent.TYPE_RECEIVED,
            event_at=t_later,
            from_person='Officer A',
            to_person='Officer B',
            location_reference='Locker 1',
            recorded_by=self.officer
        )

        # Add earlier event later
        e_retro = CustodyEvent.objects.create(
            sample=self.sample,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=t_earlier,
            from_person='Scene',
            to_person='Officer A',
            location_reference='Field',
            recorded_by=self.officer
        )

        e_retro.refresh_from_db()
        self.assertTrue(e_retro.is_out_of_sequence)
