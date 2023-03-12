import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Shedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_subject_tab()
        self._create_subject_type_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="8_lab",
                                     user="postgres",
                                     password="2022",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)

        self._create_monday_table()
        self._create_tuesday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teacher")

        self.teacher_gbox = QGroupBox("Teachers")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teacher_gbox)

        self._create_teacher_table()

        self.update_teacher_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_teacher_button)
        self.update_shedule_button.clicked.connect(self._update_teacher)

        self.teacher_tab.setLayout(self.svbox)

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.subject_gbox = QGroupBox("Subjects")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.update_subject_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subject_button)
        self.update_shedule_button.clicked.connect(self._update_subject)

        self.subject_tab.setLayout(self.svbox)

    def _create_subject_type_tab(self):
        self.subject_type_tab = QWidget()
        self.tabs.addTab(self.subject_type_tab, "Subject types")

        self.subject_type_gbox = QGroupBox("Subject types")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subject_type_gbox)

        self._create_subject_type_table()

        self.update_subject_type_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subject_type_button)
        self.update_shedule_button.clicked.connect(self._update_subject_type)

        self.subject_type_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(4)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "", ""])

        self._update_tuesday_table()

        self.tvbox = QVBoxLayout()
        self.tvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.tvbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(4)
        self.teacher_table.setHorizontalHeaderLabels(["Full name", "Subject type", "Subject", ""])

        self._update_teacher_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(2)
        self.subject_table.setHorizontalHeaderLabels(["Name", ""])

        self._update_subject_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

    def _create_subject_type_table(self):
        self.subject_type_table = QTableWidget()
        self.subject_type_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_type_table.setColumnCount(2)
        self.subject_type_table.setHorizontalHeaderLabels(["Name", ""])

        self._update_subject_type_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_type_table)
        self.subject_type_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Понедельник'")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 3, joinButton)

#            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.monday_table.resizeRowsToContents()

    def _update_tuesday_table(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Вторник'")
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.tuesday_table.setItem(i, 0,
                                          QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                          QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 2,
                                          QTableWidgetItem(str(r[4])))
            self.tuesday_table.setCellWidget(i, 3, joinButton)

#           joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.tuesday_table.resizeRowsToContents()

    def _update_teacher_table(self):
        self.cursor.execute('SELECT full_name, subject_type, subject FROM teacher ORDER BY full_name, subject_type')
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.teacher_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)

#            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.teacher_table.resizeRowsToContents()

    def _update_subject_table(self):
        self.cursor.execute('SELECT name FROM subject ORDER BY name')
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setCellWidget(i, 1, joinButton)

        #            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.subject_table.resizeRowsToContents()

    def _update_subject_type_table(self):
        self.cursor.execute('SELECT name FROM subject_type ORDER BY name')
        records = list(self.cursor.fetchall())

        self.subject_type_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.subject_type_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_type_table.setCellWidget(i, 1, joinButton)

        #            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.subject_type_table.resizeRowsToContents()

    # def _change_day_from_table(self, rowNum):
    #     row = list()
    #     for i in range(self.monday_table.columnCount()):
    #         try:
    #             row.append(self.monday_table.item(rowNum, i).text())
    #         except:
    #             row.append(None)
    #
    #         try:
    #             self.cursor.execute("UPDATE SQL запрос на изменение одной строки в базе данных", (row[0],))
    #             self.conn.commit()
    #         except:
    #             QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
        self._update_monday_table()
        self._update_tuesday_table()

    def _update_teacher(self):
        self._update_teacher_table()

    def _update_subject(self):
        self._update_subject()

    def _update_subject_type(self):
        self._update_subject_type_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
