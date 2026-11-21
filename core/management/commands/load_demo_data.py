from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta, date
from django.core.files.base import ContentFile

from cases.models import CaseRecord, Sample
from testing_records.models import TestKit, TestEvent
from custody.models import CustodyEvent
from evidence.models import EvidenceFile
from reviews.models import ReviewRecord
from auditlog.models import AuditEvent


class Command(BaseCommand):
    help = "Loads safe, realistic synthetic demo data for INT253 evaluation and testing."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing FieldTest Companion Demo Data..."))

        # 1. User Groups
        roles = ['Field Officer', 'Supervisor', 'Administrator', 'Read-only User']
        groups = {}
        for role in roles:
            group, _ = Group.objects.get_or_create(name=role)
            groups[role] = group
        self.stdout.write(self.style.SUCCESS("✓ Role groups provisioned."))

        # 2. Demo Users (Password: DemoPass123!)
        users_data = [
            ('officer_chen', 'Marcus', 'Chen', 'officer.chen@example.org', 'Field Officer', False),
            ('supervisor_ross', 'Elena', 'Ross', 'supervisor.ross@example.org', 'Supervisor', False),
            ('admin_morales', 'Carlos', 'Morales', 'admin.morales@example.org', 'Administrator', True),
            ('auditor_taylor', 'Morgan', 'Taylor', 'auditor.taylor@example.org', 'Read-only User', False),
        ]

        users = {}
        for username, first, last, email, role, is_super in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                    'is_staff': (role == 'Administrator' or is_super),
                    'is_superuser': is_super,
                    'is_active': True,
                }
            )
            user.set_password('DemoPass123!')
            user.is_staff = (role == 'Administrator' or is_super)
            user.is_superuser = is_super
            user.save()
            user.groups.clear()
            user.groups.add(groups[role])
            users[username] = user
        self.stdout.write(self.style.SUCCESS("✓ Demo user accounts created (Password: DemoPass123!)."))

        # 3. Test Kits Catalogue
        kits_data = [
            (
                "Cobalt Thiocyanate Field Screening Kit",
                "Forensic Diagnostics International",
                "Colorimetric Ampoule",
                "CAT-CT-204",
                "Wear nitrile gloves and eye protection. Ampoule contains chemical glass casing; crush within plastic safety sleeve. Do not inhale vapor."
            ),
            (
                "Marquis Presumptive Reagent Kit",
                "Reagent Solutions Ltd",
                "Acid Reagent Ampoule",
                "CAT-MQ-101",
                "Strong acid content. Use protective nitrile gloves. Neutralize used ampoules with sodium bicarbonate before authorized hazardous disposal."
            ),
            (
                "Duquenois-Levine Field Screening Kit",
                "BioScreen Forensics",
                "Multi-Ampoule Test",
                "CAT-DL-305",
                "Standard forensic PPE required. Operate in well-ventilated space. Avoid skin and ocular contact."
            ),
            (
                "Mecke Presumptive Reagent Strip",
                "Forensic Sciences Supply",
                "Colorimetric Screening Strip",
                "CAT-MK-402",
                "Protect test strips from ambient moisture and direct sunlight. Discard exposed strips in chemical disposal container."
            ),
        ]

        test_kits = {}
        for name, mfg, cat, ref, safety in kits_data:
            kit, _ = TestKit.objects.get_or_create(
                catalogue_reference=ref,
                defaults={
                    'name': name,
                    'manufacturer': mfg,
                    'category': cat,
                    'active': True,
                    'general_safety_note': safety,
                }
            )
            test_kits[ref] = kit
        self.stdout.write(self.style.SUCCESS("✓ Approved test kit catalogue metadata provisioned."))

        # 4. Fictional Cases
        now = timezone.now()

        # Case 1: Approved Case
        case1, _ = CaseRecord.objects.get_or_create(
            case_reference="DEMO-2026-001",
            defaults={
                'title': "Highway 101 Vehicle Stop Field Screening",
                'incident_datetime': now - timedelta(days=5),
                'general_location': "Highway 101 Mile Marker 42, Northbound Shoulder",
                'description': "Consensual vehicle inspection during routine commercial road safety stop. Officer detected suspected bulk packaging requiring field presumptive screening and secure chain-of-custody handling.",
                'status': CaseRecord.STATUS_APPROVED,
                'created_by': users['officer_chen'],
                'assigned_to': users['supervisor_ross'],
            }
        )

        # Sample 1 under Case 1
        s1, _ = Sample.objects.get_or_create(
            sample_code="SMP-2026-0001",
            defaults={
                'case': case1,
                'collected_at': now - timedelta(days=5, hours=-1),
                'description': "White crystalline powder inside heat-sealed transparent polyethylene pouch.",
                'packaging_reference': "Tamper-Evident Evidence Bag #4811",
                'seal_reference': "SEAL-A-1082",
                'initial_condition': "Intact, sealed, dry",
                'created_by': users['officer_chen'],
            }
        )

        # Test Event on Sample 1
        TestEvent.objects.get_or_create(
            sample=s1,
            kit=test_kits["CAT-CT-204"],
            kit_lot_number="LOT-2025-99B",
            defaults={
                'kit_expiry_date': date(2027, 8, 30),
                'performed_at': now - timedelta(days=5, hours=-2),
                'performed_by': users['officer_chen'],
                'observation_notes': "Immediate bright blue precipitate observed upon breaking ampoule within 10 seconds. Color stable for 60 seconds.",
                'result_category': TestEvent.RESULT_PRESUMPTIVE_POSITIVE,
                'limitations_note': "Screening conducted at ambient temperature (19°C). Sample sent for confirmatory GC-MS laboratory testing.",
            }
        )

        # Custody Events for Sample 1
        CustodyEvent.objects.get_or_create(
            sample=s1,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=now - timedelta(days=5, hours=-1),
            defaults={
                'from_person': "Highway 101 Field Scene",
                'to_person': "Officer Marcus Chen (Badge #409)",
                'location_reference': "Highway 101 Mile 42",
                'seal_reference': "SEAL-A-1082",
                'remarks': "Initial field securement and seal application.",
                'recorded_by': users['officer_chen'],
            }
        )
        CustodyEvent.objects.get_or_create(
            sample=s1,
            event_type=CustodyEvent.TYPE_STORED,
            event_at=now - timedelta(days=5, hours=-3),
            defaults={
                'from_person': "Officer Marcus Chen (Badge #409)",
                'to_person': "Evidence Custodian L. Gomez",
                'location_reference': "District Evidence Vault Locker #14B",
                'seal_reference': "SEAL-A-1082",
                'remarks': "Deposited in secure evidence locker pending laboratory transport.",
                'recorded_by': users['officer_chen'],
            }
        )

        # Sample 2 under Case 1
        s2, _ = Sample.objects.get_or_create(
            sample_code="SMP-2026-0002",
            defaults={
                'case': case1,
                'collected_at': now - timedelta(days=5, hours=-1),
                'description': "Brown compressed plant material wrapped in plastic film.",
                'packaging_reference': "Tamper-Evident Evidence Bag #4812",
                'seal_reference': "SEAL-A-1083",
                'initial_condition': "Intact, double-wrapped",
                'created_by': users['officer_chen'],
            }
        )

        TestEvent.objects.get_or_create(
            sample=s2,
            kit=test_kits["CAT-DL-305"],
            kit_lot_number="LOT-2025-44A",
            defaults={
                'kit_expiry_date': date(2027, 4, 15),
                'performed_at': now - timedelta(days=5, hours=-2),
                'performed_by': users['officer_chen'],
                'observation_notes': "No upper layer purple coloration observed after 90 seconds. Result negative under kit criteria.",
                'result_category': TestEvent.RESULT_PRESUMPTIVE_NEGATIVE,
                'limitations_note': "Clear daylight lighting.",
            }
        )

        CustodyEvent.objects.get_or_create(
            sample=s2,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=now - timedelta(days=5, hours=-1),
            defaults={
                'from_person': "Highway 101 Field Scene",
                'to_person': "Officer Marcus Chen (Badge #409)",
                'location_reference': "Highway 101 Mile 42",
                'seal_reference': "SEAL-A-1083",
                'remarks': "Initial field securement.",
                'recorded_by': users['officer_chen'],
            }
        )

        # Review record for Case 1
        ReviewRecord.objects.get_or_create(
            case=case1,
            reviewer=users['supervisor_ross'],
            defaults={
                'decision': ReviewRecord.DECISION_APPROVED,
                'comment': "All field test entries and custody signatures reviewed and verified in accordance with departmental evidentiary standards. Approved for confirmatory analytical submission.",
            }
        )

        # Dummy evidence file for Case 1
        if not case1.evidence_files.exists():
            dummy_content = b"%PDF-1.4\n1 0 obj\n<< /Title (Fictional Field Evidence Log) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
            ev = EvidenceFile(
                case=case1,
                sample=s1,
                uploaded_by=users['officer_chen'],
                original_filename="tamper_seal_verification_log.pdf",
                content_type="application/pdf",
                file_size=len(dummy_content),
                caption="High-resolution scan of intact evidence integrity seal SEAL-A-1082."
            )
            ev.file.save("tamper_seal_verification_log.pdf", ContentFile(dummy_content))
            ev.save()

        # Case 2: Submitted Case (Awaiting Review)
        case2, _ = CaseRecord.objects.get_or_create(
            case_reference="DEMO-2026-002",
            defaults={
                'title': "Seaport Cargo Container Screening",
                'incident_datetime': now - timedelta(days=1),
                'general_location': "Commercial Seaport Terminal Gate 7, Berth 3",
                'description': "Inter-agency cargo container random screening inspection. Detected anomalous packaged materials inside shipping crate requiring presumptive documentation.",
                'status': CaseRecord.STATUS_SUBMITTED,
                'created_by': users['officer_chen'],
            }
        )

        s3, _ = Sample.objects.get_or_create(
            sample_code="SMP-2026-0003",
            defaults={
                'case': case2,
                'collected_at': now - timedelta(days=1, hours=-1),
                'description': "Brick-shaped solid white compressed matter encased in amber packaging tape.",
                'packaging_reference': "Heavy Duty Tamper Bag #8821",
                'seal_reference': "SEAL-B-4491",
                'initial_condition': "Intact, sealed, heavy tape layer",
                'created_by': users['officer_chen'],
            }
        )

        TestEvent.objects.get_or_create(
            sample=s3,
            kit=test_kits["CAT-MQ-101"],
            kit_lot_number="LOT-2026-02C",
            defaults={
                'kit_expiry_date': date(2027, 11, 20),
                'performed_at': now - timedelta(days=1, hours=-2),
                'performed_by': users['officer_chen'],
                'observation_notes': "Immediate orange to faint dark brown coloration within 20 seconds.",
                'result_category': TestEvent.RESULT_INCONCLUSIVE,
                'limitations_note': "Dockside lighting constraints; ampoule color change ambiguous between reagent stages. Confirmatory lab GC-MS strictly required.",
            }
        )

        CustodyEvent.objects.get_or_create(
            sample=s3,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=now - timedelta(days=1, hours=-1),
            defaults={
                'from_person': "Port Terminal Berth 3 Crate Inspection",
                'to_person': "Officer Marcus Chen (Badge #409)",
                'location_reference': "Seaport Terminal Gate 7",
                'seal_reference': "SEAL-B-4491",
                'remarks': "Secured from container inspection bay.",
                'recorded_by': users['officer_chen'],
            }
        )

        # Case 3: Draft Case (Work in Progress)
        case3, _ = CaseRecord.objects.get_or_create(
            case_reference="DEMO-2026-003",
            defaults={
                'title': "Transit Terminal Unattended Property Field Check",
                'incident_datetime': now - timedelta(hours=4),
                'general_location': "Central Rail Transit Concourse West",
                'description': "Unattended luggage secured by transit security personnel. Field officer dispatched to inspect and log contents.",
                'status': CaseRecord.STATUS_DRAFT,
                'created_by': users['officer_chen'],
            }
        )

        s4, _ = Sample.objects.get_or_create(
            sample_code="SMP-2026-0004",
            defaults={
                'case': case3,
                'collected_at': now - timedelta(hours=3),
                'description': "Small glass dropper bottle containing 15ml clear liquid.",
                'packaging_reference': "Rigid Plastic Specimen Container #910",
                'seal_reference': "SEAL-C-8812",
                'initial_condition': "Intact, dropper sealed with wax",
                'created_by': users['officer_chen'],
            }
        )

        CustodyEvent.objects.get_or_create(
            sample=s4,
            event_type=CustodyEvent.TYPE_COLLECTION,
            event_at=now - timedelta(hours=3),
            defaults={
                'from_person': "Central Transit Security Desk",
                'to_person': "Officer Marcus Chen (Badge #409)",
                'location_reference': "Transit Concourse West",
                'seal_reference': "SEAL-C-8812",
                'remarks': "Secured from transit security personnel.",
                'recorded_by': users['officer_chen'],
            }
        )

        # Audit Events
        AuditEvent.objects.get_or_create(
            object_type="CaseRecord",
            object_id=str(case1.id),
            action="CREATE",
            defaults={
                'actor': users['officer_chen'],
                'summary': f"Created case {case1.case_reference} ({case1.title}).",
                'ip_address': '127.0.0.1'
            }
        )
        AuditEvent.objects.get_or_create(
            object_type="ReviewRecord",
            object_id=str(case1.id),
            action="REVIEW_APPROVED",
            defaults={
                'actor': users['supervisor_ross'],
                'summary': f"Supervisor approved case {case1.case_reference} documentation.",
                'ip_address': '127.0.0.1'
            }
        )

        self.stdout.write(self.style.SUCCESS("✓ Complete synthetic demo data loaded successfully!"))
        self.stdout.write(self.style.NOTICE("""
Available Demo Accounts (Password: DemoPass123!):
  - Field Officer: officer_chen
  - Supervisor:    supervisor_ross
  - Administrator: admin_morales
  - Read-only:     auditor_taylor
"""))
