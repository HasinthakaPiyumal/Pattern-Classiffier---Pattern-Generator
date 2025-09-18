class EHR_AccessManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, system_id="EHR_PROD_001"):
        if not self._initialized:
            self.system_id = system_id
            self.audit_log = []
            self.active_sessions = {}
            self._initialized = True

    def grant_access(self, user_id, patient_id):
        session_key = f"{user_id}-{patient_id}-{hash(user_id+patient_id)}"
        self.active_sessions[session_key] = {"user": user_id, "patient": patient_id, "timestamp": "now"}
        self.audit_log.append(f"User {user_id} granted access to patient {patient_id}.")
        return session_key

    def revoke_access(self, session_key):
        if session_key in self.active_sessions:
            session_info = self.active_sessions.pop(session_key)
            self.audit_log.append(f"Session for {session_info['user']} to patient {session_info['patient']} revoked.")
            return True
        return False

    def get_audit_log(self):
        return list(self.audit_log)

if __name__ == "__main__":
    ehr_manager1 = EHR_AccessManager("EHR_DEV_001")
    ehr_manager2 = EHR_AccessManager("EHR_QA_002")

    print(f"Are ehr_manager1 and ehr_manager2 the same instance? {ehr_manager1 is ehr_manager2}")
    print(f"EHR Manager 1 System ID: {ehr_manager1.system_id}")
    print(f"EHR Manager 2 System ID: {ehr_manager2.system_id}")

    session1 = ehr_manager1.grant_access("Dr. Smith", "P-101")
    session2 = ehr_manager2.grant_access("Nurse Jane", "P-102")

    print(f"Active sessions: {ehr_manager1.active_sessions}")
    print(f"Audit log: {ehr_manager2.get_audit_log()}")

    ehr_manager1.revoke_access(session1)
    print(f"Audit log after revoke: {ehr_manager1.get_audit_log()}")