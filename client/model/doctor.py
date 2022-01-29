from .healthcare_professional import HealthcareProfessional


class Doctor(HealthcareProfessional):

    def __init__(self) -> None:
        super().__init__()

    def issue_prescription(self, prescription) -> None:
        pass

