import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_credit_score(application_id, ssn):
    time.sleep(random.uniform(0.8, 2.2))
    score = random.randint(300, 850)
    if score < 600:
        return {"application_id": application_id, "status": "failed", "reason": f"Low credit score: {score}", "credit_score": score}
    return {"application_id": application_id, "status": "success", "credit_ok": True, "credit_score": score}

def verify_documents(application_id, document_list):
    time.sleep(random.uniform(1.0, 2.5))
    if "fake_id" in document_list:
        return {"application_id": application_id, "status": "failed", "reason": "Fake document detected"}
    if random.random() < 0.1:
        return {"application_id": application_id, "status": "failed", "reason": "Documents incomplete or invalid"}
    return {"application_id": application_id, "status": "success", "documents_ok": True}

def perform_risk_assessment(application_id, loan_amount, income):
    time.sleep(random.uniform(1.2, 2.8))
    risk_factor = loan_amount / income
    if risk_factor > 0.5 and random.random() < 0.2:
        return {"application_id": application_id, "status": "failed", "reason": "High risk detected", "risk_factor": risk_factor}
    return {"application_id": application_id, "status": "success", "risk_ok": True, "risk_factor": risk_factor}

def make_approval_decision(application_id, credit_score, documents_ok, risk_ok, loan_amount):
    time.sleep(random.uniform(0.5, 1.5))
    if not (documents_ok and risk_ok and credit_score >= 650):
        decision = "denied"
        reason = "Failed one or more critical checks"
    elif loan_amount > 100000 and credit_score < 700:
        decision = "denied"
        reason = "High loan amount with insufficient credit score"
    else:
        decision = "approved"
        reason = "All criteria met"
    return {"application_id": application_id, "status": "success", "decision": decision, "reason": reason}

def disburse_funds(application_id, loan_amount, bank_account):
    time.sleep(random.uniform(1.0, 3.0))
    if random.random() < 0.05:
        return {"application_id": application_id, "status": "failed", "reason": "Fund disbursement system error"}
    return {"application_id": application_id, "status": "success", "disbursed": True}

def process_loan_application(application_data):
    application_id = application_data["id"]
    ssn = application_data["ssn"]
    documents = application_data["documents"]
    loan_amount = application_data["loan_amount"]
    income = application_data["annual_income"]
    bank_account = application_data["bank_account"]

    print(f"\n--- Starting loan application processing for Application {application_id} ---")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_credit = executor.submit(check_credit_score, application_id, ssn)
        future_docs = executor.submit(verify_documents, application_id, documents)
        future_risk = executor.submit(perform_risk_assessment, application_id, loan_amount, income)

        for future in as_completed([future_credit, future_docs, future_risk]):
            result = future.result()
            if result["status"] == "failed":
                print(f"[{application_id}] Critical failure during initial check: {result['reason']}. Aborting.")
                return {"application_id": application_id, "overall_status": "denied", "reason": result["reason"]}
            results.update(result)

    if not (results.get("credit_ok") and results.get("documents_ok") and results.get("risk_ok")):
        print(f"[{application_id}] Initial loan checks failed. Overall status: Denied.")
        return {"application_id": application_id, "overall_status": "denied", "reason": "Pre-approval checks failed"}

    print(f"[{application_id}] All initial parallel loan checks completed successfully.")

    approval_result = make_approval_decision(
        application_id,
        results.get("credit_score", 0),
        results.get("documents_ok", False),
        results.get("risk_ok", False),
        loan_amount
    )
    results.update(approval_result)

    if approval_result["decision"] == "denied":
        print(f"[{application_id}] Loan application denied: {approval_result['reason']}. No fund disbursement.")
        results["overall_status"] = "denied"
        return results

    disbursement_result = disburse_funds(application_id, loan_amount, bank_account)
    if disbursement_result["status"] == "failed":
        print(f"[{application_id}] Failed to disburse funds: {disbursement_result['reason']}.")
        results["disbursement_status"] = "failed"
        results["overall_status"] = "approved_but_disbursement_failed"
    else:
        results["disbursement_status"] = "success"
        results["overall_status"] = "approved_and_disbursed"

    print(f"--- Finished loan application processing for Application {application_id}. Overall status: {results['overall_status']} ---")
    return results

if __name__ == "__main__":
    applications = [
        {"id": "LOAN001", "ssn": "123-45-6789", "documents": ["ID", "Paystub"], "loan_amount": 50000, "annual_income": 100000, "bank_account": "ACC123"},
        {"id": "LOAN002", "ssn": "987-65-4321", "documents": ["ID", "BankStatement"], "loan_amount": 150000, "annual_income": 80000, "bank_account": "ACC456"},
        {"id": "LOAN003", "ssn": "111-22-3333", "documents": ["ID", "fake_id"], "loan_amount": 20000, "annual_income": 60000, "bank_account": "ACC789"},
        {"id": "LOAN004", "ssn": "555-44-3333", "documents": ["ID", "Paystub"], "loan_amount": 30000, "annual_income": 40000, "bank_account": "ACC000"}
    ]

    for app in applications:
        final_status = process_loan_application(app)
        print(f"Final result for {app['id']}: {final_status['overall_status']}")
        time.sleep(1)
