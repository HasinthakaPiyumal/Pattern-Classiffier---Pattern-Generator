import hashlib
import json
import datetime
import uuid

class BlockchainRegistry:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': []
        }
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_ethical_record(self, record_type, entity_id, description, issuer, status="compliant"):
        last_block = self.get_last_block()
        proof = len(self.chain)
        previous_hash = self.hash_block(last_block)
        new_block = self.create_block(proof, previous_hash)

        credential_id = str(uuid.uuid4())
        record_data = {
            "credential_id": credential_id,
            "record_type": record_type,
            "entity_id": entity_id,
            "description": description,
            "issuer": issuer,
            "status": status,
            "block_index": new_block['index']
        }
        new_block['data'].append(record_data)
        print(f"Registered ethical record '{record_type}' for '{entity_id}' with ID: {credential_id}")
        return credential_id

    def get_record_status(self, credential_id):
        for block in reversed(self.chain):
            for record in block['data']:
                if record.get("credential_id") == credential_id:
                    return record.get("status", "unknown")
        return "not_found"

class LoanRecommendationAI:
    def __init__(self, name, model_version):
        self.name = name
        self.model_version = model_version
        self.ethics_compliance_records = []

    def register_ethics_compliance(self, registry, record_type, description, issuer):
        record_id = registry.add_ethical_record(record_type, self.name, description, issuer)
        self.ethics_compliance_records.append(record_id)
        return record_id

    def recommend_loan(self, applicant_data):
        return f"AI '{self.name}' processing loan application for {applicant_data.get('name')}."

class BankEmployee:
    def __init__(self, name, employee_id, ethics_certification_id, financial_reg_cert_id):
        self.name = name
        self.employee_id = employee_id
        self.ethics_certification_id = ethics_certification_id
        self.financial_reg_cert_id = financial_reg_cert_id

class ComplianceOfficer:
    def __init__(self, blockchain_registry):
        self.registry = blockchain_registry

    def verify_ai_system_compliance(self, ai_system):
        print(f"\nVerifying AI system '{ai_system.name}' (v{ai_system.model_version}) compliance...")
        if not ai_system.ethics_compliance_records:
            print("  AI system has no registered compliance records.")
            return False
        all_compliant = True
        for record_id in ai_system.ethics_compliance_records:
            status = self.registry.get_record_status(record_id)
            if status == "compliant":
                print(f"  Record '{record_id}' is COMPLIANT.")
            else:
                print(f"  Record '{record_id}' (status: {status}) is NOT COMPLIANT.")
                all_compliant = False
        return all_compliant

    def verify_employee_certifications(self, employee):
        print(f"Verifying employee '{employee.name}' certifications...")
        ethics_status = self.registry.get_record_status(employee.ethics_certification_id)
        fin_reg_status = self.registry.get_record_status(employee.financial_reg_cert_id)

        is_ethics_certified = ethics_status == "compliant"
        is_fin_reg_certified = fin_reg_status == "compliant"

        print(f"  AI Ethics Certification '{employee.ethics_certification_id}': {'COMPLIANT' if is_ethics_certified else 'NOT COMPLIANT'}")
        print(f"  Financial Regulations Certification '{employee.financial_reg_cert_id}': {'COMPLIANT' if is_fin_reg_certified else 'NOT COMPLIANT'}")

        return is_ethics_certified and is_fin_reg_certified

financial_ethics_chain = BlockchainRegistry()

loan_ai = LoanRecommendationAI("FairLend AI", "1.0.3")

loan_ai.register_ethics_compliance(
    financial_ethics_chain,
    "FairnessAuditReport",
    "Audit confirmed no discriminatory bias based on protected characteristics (race, gender, etc.)",
    "Independent AI Audit Firm"
)

loan_ai.register_ethics_compliance(
    financial_ethics_chain,
    "ExplainabilityReport",
    "Model provides clear, human-understandable reasons for loan decisions, compliant with 'right to explanation'.",
    "Internal AI Governance Committee"
)

loan_ai.register_ethics_compliance(
    financial_ethics_chain,
    "RegulatoryCompliance",
    "Certified compliance with Equal Credit Opportunity Act (ECOA) and other fair lending laws.",
    "Financial Regulatory Body"
)

emma_ethics_cert_id = financial_ethics_chain.add_ethical_record(
    "EmployeeCertification",
    "Emma Lee",
    "Completed 'Ethical AI in Finance' training.",
    "Bank HR & Compliance"
)
emma_fin_reg_cert_id = financial_ethics_chain.add_ethical_record(
    "EmployeeCertification",
    "Emma Lee",
    "Certified in Financial Regulations and Fair Lending Practices.",
    "Financial Industry Training Board"
)
emma_lee = BankEmployee("Emma Lee", "EMP-001", emma_ethics_cert_id, emma_fin_reg_cert_id)

david_ethics_cert_id = financial_ethics_chain.add_ethical_record(
    "EmployeeCertification",
    "David Chen",
    "Completed 'Ethical AI in Finance' training.",
    "Bank HR & Compliance"
)
david_chen = BankEmployee("David Chen", "EMP-002", david_ethics_cert_id, "UNREGISTERED_FIN_REG_CERT")

officer = ComplianceOfficer(financial_ethics_chain)

print("\n--- Attempting access for Emma Lee ---")
ai_is_compliant = officer.verify_ai_system_compliance(loan_ai)
employee_is_certified = officer.verify_employee_certifications(emma_lee)

if ai_is_compliant and employee_is_certified:
    print(f"\nAccess GRANTED to {emma_lee.name} for {loan_ai.name}.")
    print(loan_ai.recommend_loan({"name": "Applicant A", "credit_score": 720, "income": 80000}))
else:
    print(f"\nAccess DENIED to {emma_lee.name} for {loan_ai.name}.")

print("\n--- Attempting access for David Chen ---")
ai_is_compliant = officer.verify_ai_system_compliance(loan_ai)
employee_is_certified = officer.verify_employee_certifications(david_chen)

if ai_is_compliant and employee_is_certified:
    print(f"\nAccess GRANTED to {david_chen.name} for {loan_ai.name}.")
else:
    print(f"\nAccess DENIED to {david_chen.name} for {loan_ai.name}.")

print("\n--- Simulating a compliance issue with the AI system ---")
loan_ai.ethics_compliance_records.append(financial_ethics_chain.add_ethical_record(
    "FairnessAuditReport",
    loan_ai.name,
    "Subsequent audit found minor bias in specific loan categories. Previous compliance record is now invalid.",
    "Independent AI Audit Firm",
    status="non_compliant"
))

print("\n--- Re-attempting access for Emma Lee after AI compliance issue ---")
ai_is_compliant = officer.verify_ai_system_compliance(loan_ai)
employee_is_certified = officer.verify_employee_certifications(emma_lee)

if ai_is_compliant and employee_is_certified:
    print(f"\nAccess GRANTED to {emma_lee.name} for {loan_ai.name}.")
else:
    print(f"\nAccess DENIED to {emma_lee.name} for {loan_ai.name}.")