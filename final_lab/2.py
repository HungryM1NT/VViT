import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QInputDialog)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')
        self.timetable = []
        for i in range(1, 3):
            for j in self.days:
                self.timetable.append([str(i), j])
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

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)

        self.gboxes = []
        for i in self.timetable:
            self.day_gbox = QGroupBox(i[1])
            self.gboxes.append(self.day_gbox)
            if i[0] == '1':
                self.shbox1.addWidget(self.day_gbox)
            else:
                self.shbox2.addWidget(self.day_gbox)
        self._create_week_tables()

        self.update_shedule_button = QPushButton("Update")
        self.shbox3.addWidget(self.update_shedule_button)
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
        self.update_teacher_button.clicked.connect(self._update_teacher)

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
        self.update_subject_button.clicked.connect(self._update_subject)

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
        self.update_subject_type_button.clicked.connect(self._update_subject_type)

        self.subject_type_tab.setLayout(self.svbox)

    def _create_week_tables(self):
        self.week = []

        self.cursor.execute("SELECT column_name FROM information_schema.columns "
                            "WHERE table_schema = 'public' AND table_name = 'timetable' ")
        self.timetable_columns = []
        for i in self.cursor.fetchall():
            self.timetable_columns.append(i[0])
        self.timetable_columns.pop(0)
        self.timetable_columns.pop(0)
        self.timetable_columns.pop(0)
        print(self.timetable_columns)

        for day in range(12):
            self.day_table = QTableWidget()
            self.day_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.day_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.week.append(self.day_table)
            self.week[day].setColumnCount(len(self.timetable_columns) + 2)
            self.week[day].setHorizontalHeaderLabels(self.timetable_columns + ["", ""])
            self._update_week_tables(day)
            self.mvbox = QVBoxLayout()
            self.mvbox.addWidget(self.day_table)
            self.gboxes[day].setLayout(self.mvbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.cursor.execute("SELECT column_name FROM information_schema.columns "
                            "WHERE table_schema = 'public' AND table_name = 'teacher' ")
        self.teacher_columns = []
        for i in self.cursor.fetchall():
            self.teacher_columns.append(i[0])
        self.teacher_columns.pop(0)
        print(self.teacher_columns)

        self.teacher_table.setColumnCount(len(self.teacher_columns) + 2)
        self.teacher_table.setHorizontalHeaderLabels(self.teacher_columns + ["", ""])

        self._update_teacher_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.cursor.execute("SELECT column_name FROM information_schema.columns "
                            "WHERE table_schema = 'public' AND table_name = 'subject' ")
        self.subject_columns = []
        for i in self.cursor.fetchall():
            self.subject_columns.append(i[0])
        print(self.subject_columns)

        self.subject_table.setColumnCount(len(self.subject_columns) + 2)
        self.subject_table.setHorizontalHeaderLabels(self.subject_columns + ["", ""])

        self._update_subject_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

    def _create_subject_type_table(self):
        self.subject_type_table = QTableWidget()
        self.subject_type_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.subject_type_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.cursor.execute("SELECT column_name FROM information_schema.columns "
                            "WHERE table_schema = 'public' AND table_name = 'subject_type' ")
        self.subject_type_columns = []
        for i in self.cursor.fetchall():
            self.subject_type_columns.append(i[0])
        print(self.subject_type_columns)

        self.subject_type_table.setColumnCount(len(self.subject_type_columns) + 2)
        self.subject_type_table.setHorizontalHeaderLabels((self.subject_type_columns + ["", ""]))

        self._update_subject_type_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_type_table)
        self.subject_type_gbox.setLayout(self.mvbox)

    def _update_week_tables(self, day):
        self.cursor.execute("SELECT * FROM timetable "
                            "WHERE day=%s AND week=%s"
                            "ORDER BY study_time", (self.timetable[day][1], self.timetable[day][0]))
        records = list(self.cursor.fetchall())
        print(records)
        self.week[day].setRowCount(len(records) + 2)
        if records:
            for i, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Rewrite")
                for k in range(3, len(r)):
                    self.week[day].setItem(i, k - 3, QTableWidgetItem(str(r[k])))
                self.week[day].setCellWidget(i, len(r) - 3, joinButton)
                #joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
        else:
            createButton = QPushButton("Create")
            self.week[day].setCellWidget(0, 0, createButton)

        self.week[day].resizeRowsToContents()

    def _update_teacher_table(self):
        self.cursor.execute('SELECT full_name, subject_type, subject FROM teacher ORDER BY full_name, subject_type')
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 2)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Rewrite")

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

        self.subject_table.setRowCount(len(records) + 2)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Rewrite")

            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setCellWidget(i, 1, joinButton)

        #            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

        self.subject_table.resizeRowsToContents()

    def _update_subject_type_table(self):
        self.cursor.execute('SELECT name FROM subject_type ORDER BY name')
        records = list(self.cursor.fetchall())

        self.subject_type_table.setRowCount(len(records) + 2)

        for i, r in enumerate(records):
            r = list(r)
            rewriteButton = QPushButton("Rewrite")

            self.subject_type_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_type_table.setCellWidget(i, 1, rewriteButton)
            rewriteButton.clicked.connect(lambda ch, num=i: self._change_subject_type(num))

        self.subject_type_table.resizeRowsToContents()

    def _change_subject_type(self, rowNum):
        row = list()

         # for i in range(self.monday_table.columnCount()):
         #     try:
         #         row.append(self.monday_table.item(rowNum, i).text())
         #     except:
         #         row.append(None)
         #
         #     try:
         #         self.cursor.execute("UPDATE SQL запрос на изменение одной строки в базе данных", (row[0],))
         #         self.conn.commit()
         #     except:
         #         QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
        for i in range(12):
            self._update_week_tables(i)

    def _update_teacher(self):
        self._update_teacher_table()

    def _update_subject(self):
        self._update_subject_table()

    def _update_subject_type(self):
        self._update_subject_type_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
