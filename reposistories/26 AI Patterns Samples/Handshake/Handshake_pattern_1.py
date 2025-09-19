import time
import json
import random

def get_expected_lab_schema():
    return [
        {"test_name": "Glucose", "type": "float", "unit": "mg/dL"},
        {"test_name": "Cholesterol_HDL", "type": "float", "unit": "mg/dL"},
        {"test_name": "White_Blood_Cell_Count", "type": "int", "unit": "/uL"},
        {"test_name": "C_Reactive_Protein", "type": "float", "unit": "mg/L"}
    ]

def receive_lab_data_batch(simulate_inconsistency=False):
    sample_data = [
        {"Glucose": 95.0, "Cholesterol_HDL": 55.0, "White_Blood_Cell_Count": 7500, "C_Reactive_Protein": 2.1},
        {"Glucose": 102.5, "Cholesterol_HDL": 48.2, "White_Blood_Cell_Count": 6800, "C_Reactive_Protein": 1.5},
        {"Glucose": 88.0, "Cholesterol_HDL": 60.1, "White_Blood_Cell_Count": 8100, "C_Reactive_Protein": 0.9}
    ]
    if simulate_inconsistency:
        if random.random() < 0.25:
            for record in sample_data:
                if "Glucose" in record:
                    record["Blood_Sugar"] = record.pop("Glucose")
        elif random.random() < 0.15:
            for record in sample_data:
                record.pop("Cholesterol_HDL", None)
        elif random.random() < 0.10:
            for record in sample_data:
                record["C_Reactive_Protein"] = "High" if record["C_Reactive_Protein"] > 2.0 else "Normal"
    return sample_data

def validate_lab_data_schema(expected_schema, current_data_sample):
    if not current_data_sample:
        return ["No lab data received for validation."]
    sample_record = current_data_sample[0]
    inconsistencies = []
    for expected_test in expected_schema:
        test_name = expected_test["test_name"]
        expected_type = expected_test["type"]
        if test_name not in sample_record:
            inconsistencies.append(f"Missing expected lab test: '{test_name}'")
        else:
            actual_value = sample_record[test_name]
            if expected_type == "float" and not isinstance(actual_value, (float, int)):
                inconsistencies.append(f"Type mismatch for '{test_name}': expected {expected_type}, got {type(actual_value).__name__}")
            elif expected_type == "int" and not isinstance(actual_value, int):
                inconsistencies.append(f"Type mismatch for '{test_name}': expected {expected_type}, got {type(actual_value).__name__}")
    for current_test_name in sample_record:
        if not any(t["test_name"] == current_test_name for t in expected_schema):
            inconsistencies.append(f"Unexpected lab test detected: '{current_test_name}'")
    return inconsistencies

def alert_clinical_team(message):
    print(f"!!! CLINICAL ALERT !!! Data Engineering Team: {message}")

def run_handshake_process_healthcare():
    print("Starting Healthcare Disease Prediction System Lab Data Handshake Monitor...")
    expected_lab_schema = get_expected_lab_schema()
    print(f"Expected Lab Schema: {json.dumps(expected_lab_schema, indent=2)}")
    for i in range(5):
        print(f"\n--- Checking for lab data schema inconsistencies (Iteration {i+1}) ---")
        current_lab_data = receive_lab_data_batch(simulate_inconsistency=True)
        print(f"Sample Current Lab Data (first record): {json.dumps(current_lab_data[0] if current_lab_data else {}, indent=2)}")
        inconsistencies = validate_lab_data_schema(expected_lab_schema, current_lab_data)
        if inconsistencies:
            alert_message = "Critical lab data schema inconsistency detected! " + "; ".join(inconsistencies)
            alert_clinical_team(alert_message)
        else:
            print("No lab data schema inconsistencies detected. Data is consistent with expectations.")
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_handshake_process_healthcare()