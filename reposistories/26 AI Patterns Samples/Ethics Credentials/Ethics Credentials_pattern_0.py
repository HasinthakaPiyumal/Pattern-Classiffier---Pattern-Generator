import uuid
import datetime

class EthicalLedger:
    def __init__(self):
        self._records = {}

    def register_credential(self, issuer, details, status="verified"):
        credential_id = str(uuid.uuid4())
        self._records[credential_id] = {
            "issuer": issuer,
            "issued_date": datetime.datetime.now().isoformat(),
            "status": status,
            "details": details
        }
        return credential_id

    def get_credential_status(self, credential_id):
        return self._records.get(credential_id, {"status": "not_found"})

class HealthcareAI:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.ethics_credentials = []

    def register_ethics_credential(self, ledger, issuer, details):
        credential_id = ledger.register_credential(issuer, details)
        self.ethics_credentials.append(credential_id)
        print(f"AI '{self.name}' registered ethical credential: {credential_id}")
        return credential_id

    def perform_diagnosis(self, patient_data):
        return f"AI '{self.name}' analyzing patient data for diagnosis."

class MedicalProfessional:
    def __init__(self, name, license_id, ethics_training_certificate_id):
        self.name = name
        self.license_id = license_id
        self.ethics_training_certificate_id = ethics_training_certificate_id

class CredentialVerifier:
    def __init__(self, ethical_ledger):
        self.ethical_ledger = ethical_ledger

    def verify_ai_system_credentials(self, ai_system):
        print(f"\nVerifying AI system '{ai_system.name}' credentials...")
        if not ai_system.ethics_credentials:
            print("  AI system has no registered ethics credentials.")
            return False
        all_verified = True
        for cred_id in ai_system.ethics_credentials:
            status_info = self.ethical_ledger.get_credential_status(cred_id)
            if status_info["status"] == "verified":
                print(f"  Credential '{cred_id}' (issued by {status_info.get('issuer')}) is VERIFIED.")
            else:
                print(f"  Credential '{cred_id}' (status: {status_info['status']}) is NOT VERIFIED.")
                all_verified = False
        return all_verified

    def verify_user_credentials(self, user):
        print(f"Verifying user '{user.name}' credentials...")
        is_license_valid = user.license_id.startswith("MD-") and len(user.license_id) == 8
        ethics_cert_status = self.ethical_ledger.get_credential_status(user.ethics_training_certificate_id)
        is_ethics_cert_verified = ethics_cert_status["status"] == "verified"

        print(f"  Medical License '{user.license_id}': {'VALID' if is_license_valid else 'INVALID'}")
        print(f"  Ethics Training Certificate '{user.ethics_training_certificate_id}': {'VERIFIED' if is_ethics_cert_verified else 'NOT VERIFIED'}")

        return is_license_valid and is_ethics_cert_verified

global_ethical_ledger = EthicalLedger()

diagnostic_ai = HealthcareAI("MediScan AI", "Assists in diagnosing medical conditions from imaging data.")

diag_cred_1 = diagnostic_ai.register_ethics_credential(
    global_ethical_ledger,
    "AI Ethics Audit Board",
    {"type": "DataDiversityCertification", "dataset_id": "DS-2023-001", "audit_report_hash": "abc123def456"}
)

diag_cred_2 = diagnostic_ai.register_ethics_credential(
    global_ethical_ledger,
    "Healthcare Compliance Authority",
    {"type": "HIPAACompliance", "version": "2023.1", "compliance_officer": "Dr. E. Thics"}
)

diag_cred_3 = diagnostic_ai.register_ethics_credential(
    global_ethical_ledger,
    "National Medical Ethics Council",
    {"type": "ClinicalUseApproval", "approval_date": "2023-10-26", "review_board_id": "EMCB-007"}
)

dr_smith_cert_id = global_ethical_ledger.register_credential(
    "Medical Ethics Training Institute",
    {"type": "AIEthicsTrainingCompletion", "course_name": "Responsible AI in Medicine", "grade": "A+"}
)
dr_smith = MedicalProfessional("Dr. Smith", "MD-123456", dr_smith_cert_id)

dr_jones_cert_id = "NOT_REGISTERED_CERT"
dr_jones = MedicalProfessional("Dr. Jones", "MD-987654", dr_jones_cert_id)

verifier = CredentialVerifier(global_ethical_ledger)

print("\n--- Attempting access for Dr. Smith ---")
ai_is_ethical = verifier.verify_ai_system_credentials(diagnostic_ai)
user_is_authorized = verifier.verify_user_credentials(dr_smith)

if ai_is_ethical and user_is_authorized:
    print(f"\nAccess GRANTED to {dr_smith.name} for {diagnostic_ai.name}.")
    print(diagnostic_ai.perform_diagnosis({"patient_id": "P-001", "imaging_data": "MRI_scan_001.jpg"}))
else:
    print(f"\nAccess DENIED to {dr_smith.name} for {diagnostic_ai.name}.")

print("\n--- Attempting access for Dr. Jones ---")
ai_is_ethical = verifier.verify_ai_system_credentials(diagnostic_ai)
user_is_authorized = verifier.verify_user_credentials(dr_jones)

if ai_is_ethical and user_is_authorized:
    print(f"\nAccess GRANTED to {dr_jones.name} for {diagnostic_ai.name}.")
else:
    print(f"\nAccess DENIED to {dr_jones.name} for {diagnostic_ai.name}.")

print("\n--- Simulating a revoked AI credential ---")
global_ethical_ledger._records[diag_cred_2]["status"] = "revoked"
print(f"Credential '{diag_cred_2}' for {diagnostic_ai.name} has been REVOKED.")

print("\n--- Re-attempting access for Dr. Smith after AI credential revocation ---")
ai_is_ethical = verifier.verify_ai_system_credentials(diagnostic_ai)
user_is_authorized = verifier.verify_user_credentials(dr_smith)

if ai_is_ethical and user_is_authorized:
    print(f"\nAccess GRANTED to {dr_smith.name} for {diagnostic_ai.name}.")
else:
    print(f"\nAccess DENIED to {dr_smith.name} for {diagnostic_ai.name}.")