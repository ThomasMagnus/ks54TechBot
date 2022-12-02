class UserApp:
    def __init__(self, type_app: str = '',
                 user_name: str = '',
                 cabinet: str = '',
                 problem_device: str = '',
                 problem_text: str = '',
                 app_number: str = ''):
        self.type_app = type_app
        self.user_name = user_name
        self.cabinet = cabinet
        self.problem_device = problem_device
        self.problem_text = problem_text
        self.app_number = app_number

    def create_app(self) -> str:
        return f'Номер заявки: {self.app_number}\n' \
               f'Тип заявки: {self.type_app}\n' \
               f'ФИО: {self.user_name}\n' \
               f'Кабинет: {self.cabinet}\n' \
               f'Наименование проблемного устройства: {self.problem_device}\n' \
               f'Описание проблемы: {self.problem_text}'
