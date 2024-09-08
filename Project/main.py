import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog


class DecimalToBinaryConverter(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем интерфейс
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Конвертер дробных чисел из 10-й в 2-ю систему счисления')

        # Элементы интерфейса
        self.layout = QVBoxLayout()

        self.input_label = QLabel('Введите дробное число в 10-й системе счисления:')
        self.layout.addWidget(self.input_label)

        self.input_line_edit = QLineEdit(self)
        self.layout.addWidget(self.input_line_edit)

        self.convert_button = QPushButton('Перевести в двоичную систему', self)
        self.convert_button.clicked.connect(self.convert_to_binary)
        self.layout.addWidget(self.convert_button)

        self.read_button = QPushButton('Читать из файла', self)
        self.read_button.clicked.connect(self.read_from_file)
        self.layout.addWidget(self.read_button)

        self.write_button = QPushButton('Записать в файл', self)
        self.write_button.clicked.connect(self.write_to_file)
        self.layout.addWidget(self.write_button)

        self.result_label = QLabel('')
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.show()

    def convert_to_binary(self):
        try:
            # Получаем ввод пользователя
            decimal_number = self.input_line_edit.text()

            # Проверяем, что введено корректное число
            if not decimal_number.replace('.', '', 1).isdigit():
                raise ValueError("Введите корректное дробное число.")

            # Преобразование в десятичное число
            decimal_number = float(decimal_number)

            # Проверка, чтобы не было отрицательных или слишком больших чисел
            if decimal_number < 0:
                raise ValueError("Отрицательные числа не допускаются.")

            # Преобразование числа в двоичную систему
            binary_representation = self.decimal_to_binary(decimal_number)

            # Проверка на превышение 32 разрядов
            if len(binary_representation.replace('.', '')) > 32:
                raise ValueError("Двоичное представление превышает 32 разряда.")

            # Вывод результата
            self.result_label.setText(f'Двоичное представление: {binary_representation}')
        except ValueError as e:
            self.show_error_message(str(e))

    def decimal_to_binary(self, decimal_number):
        # Преобразование целой и дробной части
        whole_part = int(decimal_number)
        fractional_part = decimal_number - whole_part

        # Преобразуем целую часть
        binary_whole_part = bin(whole_part).replace('0b', '')

        # Преобразуем дробную часть
        binary_fractional_part = []
        while fractional_part > 0 and len(binary_fractional_part) < 32 - len(binary_whole_part):
            fractional_part *= 2
            bit = int(fractional_part)
            binary_fractional_part.append(str(bit))
            fractional_part -= bit

        binary_fractional_part_str = ''.join(binary_fractional_part)

        if binary_fractional_part_str:
            return f'{binary_whole_part}.{binary_fractional_part_str}'
        else:
            return binary_whole_part

    def show_error_message(self, message):
        # Создание окна с сообщением об ошибке
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle('Ошибка ввода')
        error_dialog.exec_()

    def read_from_file(self):
        # Открываем диалог для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть файл', '', 'Text Files (*.txt)')

        if file_name:
            try:
                with open(file_name, 'r') as file:
                    decimal_number = file.read().strip()
                    self.input_line_edit.setText(decimal_number)
                    self.convert_to_binary()  # Автоматически преобразуем прочитанное число
            except Exception as e:
                self.show_error_message(f"Ошибка при чтении файла: {e}")

    def write_to_file(self):
        # Открываем диалог для выбора файла
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Text Files (*.txt)')

        if file_name:
            try:
                with open(file_name, 'w') as file:
                    binary_representation = self.result_label.text().replace('Двоичное представление: ', '')
                    file.write(binary_representation)
            except Exception as e:
                self.show_error_message(f"Ошибка при записи в файл: {e}")


def main():
    app = QApplication(sys.argv)
    converter = DecimalToBinaryConverter()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()