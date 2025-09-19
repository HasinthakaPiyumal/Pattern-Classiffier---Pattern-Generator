import uuid
import datetime
import random

class PHIExtractionService:
    def process(self, patient_record):
        print(f"Service: Extracting PHI from record ID {patient_record['record_id']}...")
        phi_fields = ['name', 'address', 'dob', 'ssn', 'phone', 'email']
        extracted_phi = {field: patient_record.get(field) for field in phi_fields if field in patient_record}
        patient_record['extracted_phi'] = extracted_phi
        print(f"Service: PHI extracted for record ID {patient_record['record_id']}.")
        return patient_record

class AnonymizeIdentifiersService:
    def process(self, patient_record):
        if not patient_record.get('extracted_phi'):
            return {'status': 'failed', 'reason': 'No PHI extracted for anonymization'}
        print(f"Service: Anonymizing identifiers for record ID {patient_record['record_id']}...")
        new_record = patient_record.copy()
        new_record['anonymous_id'] = str(uuid.uuid4())
        new_record.pop('name', None)
        new_record.pop('ssn', None)
        new_record.pop('address', None)
        new_record.pop('phone', None)
        new_record.pop('email', None)
        new_record.pop('extracted_phi', None)

        print(f"Service: Identifiers anonymized for record ID {patient_record['record_id']}. New ID: {new_record['anonymous_id']}")
        return new_record

class ScrambleDatesService:
    def process(self, patient_record):
        if not patient_record.get('anonymous_id'):
            return {'status': 'failed', 'reason': 'Record not anonymized yet'}
        print(f"Service: Scrambling dates for record ID {patient_record['record_id']}...")
        date_fields = ['dob', 'admission_date', 'discharge_date']
        for field in date_fields:
            if field in patient_record and patient_record[field]:
                try:
                    original_date = datetime.datetime.strptime(patient_record[field], '%Y-%m-%d').date()
                    shift = random.randint(-30, 30)
                    scrambled_date = original_date + datetime.timedelta(days=shift)
                    patient_record[field] = scrambled_date.strftime('%Y-%m-%d')
                    print(f"  - Scrambled {field} from {original_date} to {scrambled_date}")
                except ValueError:
                    print(f"  - Could not scramble invalid date for {field}: {patient_record[field]}")
        patient_record['dates_scrambled'] = True
        print(f"Service: Dates scrambled for record ID {patient_record['record_id']}.")
        return patient_record

class AggregateDataService:
    def process(self, patient_record):
        if not patient_record.get('dates_scrambled'):
            return {'status': 'failed', 'reason': 'Dates not scrambled'}
        print(f"Service: Aggregating data for record ID {patient_record['record_id']}...")
        patient_record['ready_for_aggregation'] = True
        print(f"Service: Data aggregated for record ID {patient_record['record_id']}.")
        return patient_record

class StoreAnonymizedDataService:
    def process(self, patient_record):
        if not patient_record.get('ready_for_aggregation'):
            return {'status': 'failed', 'reason': 'Data not ready for storage (not aggregated)'}
        print(f"Service: Storing anonymized data for record ID {patient_record['record_id']}...")
        storage_location = f"s3://anonymized-data/records/{patient_record['anonymous_id']}.json"
        patient_record['storage_location'] = storage_location
        patient_record['stored_status'] = 'completed'
        print(f"Service: Anonymized data stored at {storage_location} for record ID {patient_record['record_id']}.")
        return patient_record

class PatientDataAnonymizationPipeline:
    def __init__(self, services):
        self.services = services

    def run_pipeline(self, initial_data):
        current_data = initial_data.copy()
        print(f"\n--- Starting Patient Data Anonymization Pipeline for Record ID: {current_data.get('record_id')} ---")
        for service in self.services:
            print(f"Executing step: {service.__class__.__name__}")
            result = service.process(current_data)
            if result.get('status') == 'failed':
                print(f"Pipeline failed at {service.__class__.__name__}: {result.get('reason')}")
                return result
            current_data = result
        print(f"--- Patient Data Anonymization Pipeline completed for Record ID: {current_data.get('record_id')} ---")
        return current_data

if __name__ == "__main__":
    phi_extraction = PHIExtractionService()
    anonymize_identifiers = AnonymizeIdentifiersService()
    scramble_dates = ScrambleDatesService()
    aggregate_data = AggregateDataService()
    store_anonymized = StoreAnonymizedDataService()

    anonymization_pipeline = PatientDataAnonymizationPipeline([
        phi_extraction,
        anonymize_identifiers,
        scramble_dates,
        aggregate_data,
        store_anonymized
    ])

    patient_record_1 = {
        'record_id': 'PAT-001',
        'name': 'John Doe',
        'dob': '1980-05-15',
        'ssn': 'XXX-XX-1234',
        'address': '123 Main St, Anytown, USA',
        'phone': '555-123-4567',
        'email': 'john.doe@example.com',
        'admission_date': '2022-01-10',
        'diagnosis': 'Influenza',
        'treatment': 'Antivirals',
        'discharge_date': '2022-01-15'
    }

    final_anonymized_record_1 = anonymization_pipeline.run_pipeline(patient_record_1)
    print("\nFinal Anonymized Record 1:")
    print(final_anonymized_record_1)

    patient_record_2 = {
        'record_id': 'PAT-002',
        'diagnosis': 'Common Cold',
        'admission_date': '2023-03-01'
    }

    final_anonymized_record_2 = anonymization_pipeline.run_pipeline(patient_record_2)
    print("\nFinal Anonymized Record 2:")
    print(final_anonymized_record_2)
