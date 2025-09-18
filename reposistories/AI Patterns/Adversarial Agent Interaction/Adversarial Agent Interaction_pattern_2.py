import random

class LoanApplication:
    def __init__(self, applicant_id, credit_score, income, debt, requested_amount, has_suspicious_activity=False):
        self.applicant_id = applicant_id
        self.credit_score = credit_score
        self.income = income
        self.debt = debt
        self.requested_amount = requested_amount
        self.has_suspicious_activity = has_suspicious_activity
        self.status = "Pending"
        self.reason = ""

class LoanProcessorAgent:
    def process_application(self, application: LoanApplication):
        if application.credit_score >= 650 and application.income > application.debt * 2 and application.requested_amount < application.income * 3:
            application.status = "Approved (Conditional)"
            application.reason = "Meets initial credit criteria."
        else:
            application.status = "Rejected (Initial)"
            application.reason = "Does not meet basic credit criteria."
        return application

class FraudDetectionAgent:
    def review_decision(self, application: LoanApplication):
        if application.status == "Approved (Conditional)":
            if application.has_suspicious_activity:
                application.status = "Rejected (Fraud Flag)"
                application.reason = "Suspicious activity detected, potential fraud."
                print(f"FRAUD ALERT: Application {application.applicant_id} flagged due to suspicious activity.")
            elif application.credit_score < 700 and application.requested_amount > application.income * 2:
                application.status = "Rejected (High Risk)"
                application.reason = "Approved but deemed high risk after detailed review."
                print(f"RISK ALERT: Application {application.applicant_id} flagged as high risk.")
            else:
                application.status = "Approved (Final)"
                application.reason = "Passed all fraud and risk checks."
        return application

if __name__ == "__main__":
    applications_data = [
        LoanApplication("APP001", 720, 60000, 15000, 30000, False),
        LoanApplication("APP002", 680, 50000, 10000, 40000, True),
        LoanApplication("APP003", 580, 70000, 20000, 50000, False),
        LoanApplication("APP004", 750, 80000, 10000, 15000, False),
        LoanApplication("APP005", 690, 45000, 8000, 35000, False)
    ]

    loan_processor = LoanProcessorAgent()
    fraud_detector = FraudDetectionAgent()

    results = []
    for app_data in applications_data:
        print(f"\n--- Processing Application {app_data.applicant_id} ---")
        initial_decision = loan_processor.process_application(app_data)
        print(f"Initial Decision: {initial_decision.status} - {initial_decision.reason}")

        final_decision = fraud_detector.review_decision(initial_decision)
        print(f"Final Decision: {final_decision.status} - {final_decision.reason}")
        results.append((final_decision.applicant_id, final_decision.status, final_decision.reason))

    print("\n--- Final Loan Outcomes ---")
    for app_id, status, reason in results:
        print(f"Applicant {app_id}: {status} ({reason})")