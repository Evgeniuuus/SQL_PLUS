# --------------------------------Подключение к локальной базе данных--------------------------------
import sys
import cx_Oracle
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QTableWidget, \
    QTableWidgetItem


class SQLPlusApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация UI
        self.setWindowTitle("Подключение к SQL Plus")
        self.setGeometry(100, 100, 800, 600)

        # Создание виджетов
        self.layout = QVBoxLayout()

        self.db_label = QLabel("Введите данные для подключения:")
        self.layout.addWidget(self.db_label)

        self.username_label = QLabel("Пользователь:")
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        self.username_input.setText("Zhelinskiy")  # Значение по умолчанию
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Пароль:")
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setText("qwe")  # Значение по умолчанию
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.connect_button = QPushButton("Подключиться", self)
        self.layout.addWidget(self.connect_button)

        # Поле для ввода SQL-запроса
        self.query_label = QLabel("Введите SQL-запрос:")
        self.layout.addWidget(self.query_label)

        self.query_input = QTextEdit(self)
        self.layout.addWidget(self.query_input)

        self.execute_button = QPushButton("Выполнить запрос", self)
        self.layout.addWidget(self.execute_button)

        # Таблица для отображения результатов запроса
        self.results_table = QTableWidget(self)
        self.layout.addWidget(self.results_table)

        # Подключение обработчиков
        self.connect_button.clicked.connect(self.connect_to_db)
        self.execute_button.clicked.connect(self.execute_query)

        # Установка слоя
        self.setLayout(self.layout)

        self.connection = None

        # Установка стилей
        self.setStyle()

    def setStyle(self):
        """ Устанавливаем стили для интерфейса """
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: lime;
                font-size: 18px;
            }

            QLabel {
                font-weight: bold;
                font-size: 20px;
            }

            QLineEdit {
                background-color: black;
                color: lime;
                border: 2px solid lime;
                padding: 10px;
                font-size: 18px;
            }

            QPushButton {
                background-color: black;
                color: lime;
                border: 5px solid lime;
                padding: 10px;
                font-size: 20px;
                min-width: 200px;
                margin: 10px;
            }

            QTextEdit {
                background-color: black;
                color: lime;
                border: 2px solid lime;
                padding: 10px;
                font-size: 25px;
                min-height: 100px;
            }

            QTableWidget {
                background-color: black;
                color: lime;
                border: 2px solid lime;
                padding: 5px;
                font-size: 18px;
            }

            QTableWidget::item {
                color: lime;
                padding: 5px;
            }

            QTableWidget::horizontalHeader {
                background-color: black;
                color: lime;
                border: 2px solid lime;
            }

            QTableWidget::verticalHeader {
                background-color: black;
                color: lime;
                border: 2px solid lime;
            }

            QTableWidget::item:selected {
                background-color: darkgreen;
            }
        """)

    def connect_to_db(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Указываем параметры подключения
        host = "localhost"              # Локальный хост
        port = "1521"                   # Стандартный порт для Oracle
        sid = "XE"                      # SID (может быть другим)

        # Строка подключения Oracle
        dsn_tns = cx_Oracle.makedsn(host, port, sid)
        try:
            # Устанавливаем соединение
            self.connection = cx_Oracle.connect(username, password, dsn_tns)
            print("Подключение успешно!")
            self.db_label.setText("Подключение установлено успешно!")
        except cx_Oracle.DatabaseError as e:
            error_message = str(e)
            print(f"Ошибка подключения: {error_message}")
            self.db_label.setText(f"Ошибка подключения: {error_message}")

    def execute_query(self):
        if self.connection is None:
            self.db_label.setText("Сначала подключитесь к базе данных!")
            return

        query = self.query_input.toPlainText()
        if not query.strip():
            self.db_label.setText("Введите SQL-запрос!")
            return

        try:
            # Выполнение запроса
            cursor = self.connection.cursor()
            cursor.execute(query)

            # Получаем все строки результата
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Получаем имена столбцов

            # Устанавливаем количество строк и столбцов в таблице
            self.results_table.setRowCount(len(rows))
            self.results_table.setColumnCount(len(columns))

            # Устанавливаем заголовки столбцов
            self.results_table.setHorizontalHeaderLabels(columns)

            # Заполняем таблицу результатами
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.results_table.setItem(i, j, QTableWidgetItem(str(value)))

            cursor.close()

        except cx_Oracle.DatabaseError as e:
            error_message = str(e)
            self.db_label.setText(f"Ошибка выполнения запроса: {error_message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Объявляем окно
    window = SQLPlusApp()
    window.showMaximized()  # Растягиваем окно на весь экран
    sys.exit(app.exec_())
