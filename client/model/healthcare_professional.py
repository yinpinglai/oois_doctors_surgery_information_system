from .employee import Employee


class HealthcareProfessional(Employee):

    def __init__(self) -> None:
        super().__init__()

    def consultation(self) -> str:
        return f'{self.name} is performing consultation.'

