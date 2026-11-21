from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from cases.models import CaseRecord, Sample
from evidence.models import EvidenceFile


class EvidenceTests(TestCase):
    def setUp(self):
        self.fo_group = Group.objects.create(name='Field Officer')
        self.officer = User.objects.create_user(
            username='officer_evidence',
            password='TestPassword123!'
        )
        self.officer.groups.add(self.fo_group)

        self.case = CaseRecord.objects.create(
            case_reference='CASE-EVIDENCE-01',
            title='Evidence Management Case',
            incident_datetime=timezone.now(),
            general_location='Evidence Harbor',
            description='Testing evidence upload and validation.',
            status=CaseRecord.STATUS_DRAFT,
            created_by=self.officer
        )

        self.client = Client()
        self.client.login(username='officer_evidence', password='TestPassword123!')

    def test_at12_upload_disallowed_file_rejected(self):
        """AT-12: Upload disallowed or oversized file. Upload is rejected; no public file URL is exposed."""
        upload_url = reverse('evidence_upload', kwargs={'case_id': self.case.pk})

        # 1. Attempt uploading executable .exe file
        disallowed_file = SimpleUploadedFile(
            "malicious_script.exe",
            b"MZ\x90\x00\x03\x00\x00\x00binarycontent",
            content_type="application/x-msdownload"
        )
        response = self.client.post(upload_url, {
            'file': disallowed_file,
            'caption': 'Attempting invalid file extension upload',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'file',
            "Unsupported file format '.exe'. Only permitted attachments are: .jpg, .jpeg, .png, .pdf"
        )
        self.assertEqual(EvidenceFile.objects.count(), 0)

    def test_upload_oversized_file_rejected(self):
        """File exceeding size limit is rejected."""
        upload_url = reverse('evidence_upload', kwargs={'case_id': self.case.pk})
        # Simulate oversized file > 10MB
        oversized = SimpleUploadedFile(
            "huge_photo.jpg",
            b"0" * (11 * 1024 * 1024),
            content_type="image/jpeg"
        )
        response = self.client.post(upload_url, {
            'file': oversized,
            'caption': 'Oversized photo',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'file',
            "File size exceeds maximum allowed limit of 10 MB."
        )
        self.assertEqual(EvidenceFile.objects.count(), 0)

    def test_valid_evidence_upload_and_authenticated_download(self):
        """Valid file uploads securely and is served only via authenticated download endpoint."""
        upload_url = reverse('evidence_upload', kwargs={'case_id': self.case.pk})
        valid_file = SimpleUploadedFile(
            "evidence_seal.png",
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDRdummyimagecontent",
            content_type="image/png"
        )
        response = self.client.post(upload_url, {
            'file': valid_file,
            'caption': 'Tamper seal intact photograph',
        })
        self.assertEqual(response.status_code, 302)

        evidence = EvidenceFile.objects.filter(case=self.case).first()
        self.assertIsNotNone(evidence)
        self.assertEqual(evidence.original_filename, "evidence_seal.png")

        # Authenticated download succeeds
        download_url = reverse('evidence_download', kwargs={'pk': evidence.pk})
        dl_resp = self.client.get(download_url)
        self.assertEqual(dl_resp.status_code, 200)
        self.assertEqual(dl_resp['Content-Type'], 'image/png')

        # Anonymous request is redirected to login
        anon_client = Client()
        anon_resp = anon_client.get(download_url)
        self.assertEqual(anon_resp.status_code, 302)
        self.assertIn(reverse('login'), anon_resp.url)
