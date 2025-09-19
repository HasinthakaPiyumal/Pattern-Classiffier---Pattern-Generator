import pandas as pd
import numpy as np
import datetime
import random

class PatientEHRDataGenerator:
    def __init__(self, num_patients=50, start_date='2022-01-01', end_date='2023-01-01'):
        self.patients = [f'PAT{i:03d}' for i in range(num_patients)]
        self.diagnoses = ['Hypertension', 'Diabetes', 'Asthma', 'COPD', 'Heart Failure', 'Pneumonia', 'Stroke', 'Appendicitis']
        self.medications = ['Lisinopril', 'Metformin', 'Albuterol', 'Warfarin', 'Insulin', 'Antibiotic X', 'Pain Reliever Y']
        self.lab_tests = ['Blood Glucose', 'Creatinine', 'Hemoglobin A1C', 'Cholesterol', 'White Blood Cell Count']
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.admission_types = ['Emergency', 'Elective', 'Urgent']

    def _generate_admission(self, patient_id, current_date):
        admission_date = current_date + datetime.timedelta(days=random.randint(0, 30))
        discharge_date = admission_date + datetime.timedelta(days=random.randint(1, 15))
        return {
            'admission_id': f'ADM_{patient_id}_{admission_date.strftime("%Y%m%d")}_{random.randint(100,999)}',
            'patient_id': patient_id,
            'admission_date': admission_date,
            'discharge_date': discharge_date,
            'admission_type': random.choice(self.admission_types),
            'length_of_stay_days': (discharge_date - admission_date).days
        }

    def _generate_diagnosis(self, admission_id, patient_id, admission_date):
        num_diagnoses = random.randint(1, 4)
        return [{
            'admission_id': admission_id,
            'patient_id': patient_id,
            'diagnosis_code': f'DX_{random.choice(self.diagnoses).replace(" ", "_")}',
            'diagnosis_date': admission_date + datetime.timedelta(days=random.randint(0, 2))
        } for _ in range(num_diagnoses)]

    def _generate_medication(self, admission_id, patient_id, admission_date):
        num_meds = random.randint(1, 5)
        return [{
            'admission_id': admission_id,
            'patient_id': patient_id,
            'medication_name': random.choice(self.medications),
            'prescription_date': admission_date + datetime.timedelta(days=random.randint(0, 5))
        } for _ in range(num_meds)]

    def _generate_lab_result(self, admission_id, patient_id, admission_date):
        num_labs = random.randint(1, 3)
        return [{
            'admission_id': admission_id,
            'patient_id': patient_id,
            'lab_test_name': random.choice(self.lab_tests),
            'lab_value': round(random.uniform(50, 200), 2),
            'lab_date': admission_date + datetime.timedelta(days=random.randint(0, 3))
        } for _ in range(num_labs)]

    def simulate_ehr_data(self):
        all_admissions = []
        all_diagnoses = []
        all_medications = []
        all_lab_results = []

        current_date = self.start_date
        while current_date <= self.end_date:
            for patient_id in self.patients:
                if random.random() < 0.3:
                    admission = self._generate_admission(patient_id, current_date)
                    all_admissions.append(admission)
                    admission_id = admission['admission_id']
                    adm_date = admission['admission_date']

                    all_diagnoses.extend(self._generate_diagnosis(admission_id, patient_id, adm_date))
                    all_medications.extend(self._generate_medication(admission_id, patient_id, adm_date))
                    all_lab_results.extend(self._generate_lab_result(admission_id, patient_id, adm_date))
            current_date += datetime.timedelta(days=random.randint(15, 45))

        return {
            'admissions': pd.DataFrame(all_admissions),
            'diagnoses': pd.DataFrame(all_diagnoses),
            'medications': pd.DataFrame(all_medications),
            'lab_results': pd.DataFrame(all_lab_results)
        }

class PatientRiskFeatureIntegrator:
    """
    Implements the Design Holistically pattern for Healthcare patient risk assessment.
    Data extraction from EHR and feature engineering are integrated from the start,
    directly producing ML-ready features for patient risk by incorporating domain
    knowledge early. This avoids a fragmented 'pipeline jungle'.
    """
    def __init__(self, raw_ehr_data):
        self.admissions_df = raw_ehr_data['admissions']
        self.diagnoses_df = raw_ehr_data['diagnoses']
        self.medications_df = raw_ehr_data['medications']
        self.lab_results_df = raw_ehr_data['lab_results']
        self.processed_data = None

    def _calculate_readmission_target(self, admission_df, all_admissions_df, window_days=30):
        admission_df['readmission_30d'] = 0
        for index, row in admission_df.iterrows():
            discharge_date = row['discharge_date']
            patient_id = row['patient_id']
            subsequent_admissions = all_admissions_df[
                (all_admissions_df['patient_id'] == patient_id) &
                (all_admissions_df['admission_date'] > discharge_date) &
                (all_admissions_df['admission_date'] <= discharge_date + datetime.timedelta(days=window_days))
            ]
            if not subsequent_admissions.empty:
                admission_df.loc[index, 'readmission_30d'] = 1
        return admission_df

    def integrate_and_extract_risk_features(self):
        print("Holistically integrating EHR data and extracting patient risk features...")

        self.admissions_df = self._calculate_readmission_target(self.admissions_df.copy(), self.admissions_df)

        admission_diagnosis = pd.merge(self.admissions_df, self.diagnoses_df, on=['admission_id', 'patient_id'], how='left')
        admission_diagnosis['diagnosis_count'] = admission_diagnosis.groupby('admission_id')['diagnosis_code'].transform('nunique')
        admission_diagnosis['has_diabetes'] = admission_diagnosis['diagnosis_code'].apply(lambda x: 1 if 'Diabetes' in str(x) else 0)
        admission_diagnosis['has_heart_failure'] = admission_diagnosis['diagnosis_code'].apply(lambda x: 1 if 'Heart_Failure' in str(x) else 0)
        
        admission_features = admission_diagnosis.groupby('admission_id').agg(
            patient_id=('patient_id', 'first'),
            admission_date=('admission_date', 'first'),
            discharge_date=('discharge_date', 'first'),
            admission_type=('admission_type', 'first'),
            length_of_stay_days=('length_of_stay_days', 'first'),
            readmission_30d=('readmission_30d', 'first'),
            num_unique_diagnoses=('diagnosis_count', 'first'),
            ever_had_diabetes=('has_diabetes', 'max'),
            ever_had_heart_failure=('has_heart_failure', 'max')
        ).reset_index()

        admission_medication = pd.merge(self.admissions_df[['admission_id', 'patient_id']], self.medications_df, on=['admission_id', 'patient_id'], how='left')
        med_counts = admission_medication.groupby('admission_id')['medication_name'].nunique().reset_index(name='num_unique_medications')
        admission_features = pd.merge(admission_features, med_counts, on='admission_id', how='left').fillna(0)

        admission_lab = pd.merge(self.admissions_df[['admission_id', 'patient_id']], self.lab_results_df, on=['admission_id', 'patient_id'], how='left')
        avg_glucose = admission_lab[admission_lab['lab_test_name'] == 'Blood Glucose'].groupby('admission_id')['lab_value'].mean().reset_index(name='avg_blood_glucose_during_admission')
        admission_features = pd.merge(admission_features, avg_glucose, on='admission_id', how='left').fillna(0)

        admission_features['patient_age_at_admission'] = admission_features['patient_id'].apply(lambda x: random.randint(30, 90))

        self.processed_data = admission_features
        return self.processed_data

if __name__ == '__main__':
    print("--- Healthcare Patient Risk Assessment (Holistic Design) ---")
    print("Simulating raw EHR data (admissions, diagnoses, medications, lab results)...")
    ehr_generator = PatientEHRDataGenerator(num_patients=70, start_date='2022-01-01', end_date='2023-06-30')
    raw_ehr_data = ehr_generator.simulate_ehr_data()
    print(f"Generated {raw_ehr_data['admissions'].shape[0]} admission records.")
    print(f"Generated {raw_ehr_data['diagnoses'].shape[0]} diagnosis records.")

    risk_integrator = PatientRiskFeatureIntegrator(raw_ehr_data)
    patient_risk_features_df = risk_integrator.integrate_and_extract_risk_features()

    print("\nHolistically Integrated Patient Risk Features (first 5 rows):")
    print(patient_risk_features_df.head())
    print(f"\nTotal patient risk feature records generated: {patient_risk_features_df.shape[0]}")
    print("\nThese features, including the 'readmission_30d' target, are now ready for an ML model, avoiding a 'pipeline jungle'.")