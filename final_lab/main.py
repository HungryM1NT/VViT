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
        for day in range(12):
            self.day_table = QTableWidget()
            self.day_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.day_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.week.append(self.day_table)
            self.week[day].setColumnCount(6)
            self.week[day].setHorizontalHeaderLabels(["Study_time", "Subject", "Subject type", "Room", "", ""])
            self._update_week_tables(day)
            self.mvbox = QVBoxLayout()
            self.mvbox.addWidget(self.day_table)
            self.gboxes[day].setLayout(self.mvbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["Full name", "Subject type", "Subject", "", ""])

        self._update_teacher_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(["Name", "", ""])

        self._update_subject_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

    def _create_subject_type_table(self):
        self.subject_type_table = QTableWidget()
        self.subject_type_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.subject_type_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_type_table.setColumnCount(3)
        self.subject_type_table.setHorizontalHeaderLabels(["Name", "", ""])

        self._update_subject_type_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_type_table)
        self.subject_type_gbox.setLayout(self.mvbox)

    def _update_week_tables(self, day):
        self.cursor.execute("SELECT * FROM timetable "
                            "WHERE day=%s AND week=%s"
                            "ORDER BY study_time", (self.timetable[day][1], self.timetable[day][0]))
        records = list(self.cursor.fetchall())
        self.week[day].removeCellWidget(self.week[day].rowCount() - 1, 0)
        self.week[day].setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            rewriteButton = QPushButton("Rewrite")
            deleteRowButton = QPushButton("Delete")

            self.week[day].setItem(i, 0,
                                      QTableWidgetItem(str(r[3])))
            self.week[day].setItem(i, 1,
                                      QTableWidgetItem(str(r[4])))
            self.week[day].setItem(i, 2,
                                      QTableWidgetItem(str(r[5])))
            self.week[day].setItem(i, 3,
                                   QTableWidgetItem(str(r[6])))
            self.week[day].setCellWidget(i, 4, rewriteButton)
            self.week[day].setCellWidget(i, 5, deleteRowButton)
            rewriteButton.clicked.connect(lambda ch, key=r[:3], table=1: self._rewrite(key, table))
            deleteRowButton.clicked.connect(lambda ch, key=r[:3], table=1: self._delete(key, table))
        self.week[day].setRowCount(len(records) + 1)
        addRowButton = QPushButton("Add")
        self.week[day].removeCellWidget(self.week[day].rowCount() - 1, 1)
        self.week[day].removeCellWidget(self.week[day].rowCount() - 1, 2)
        self.week[day].setCellWidget(self.week[day].rowCount() - 1, 0, addRowButton)
        if records:
            addRowButton.clicked.connect(lambda ch, table=1: self._add(table, r[1:3]))
        else:
            addRowButton.clicked.connect(lambda ch, table=1: self._add(table, self.timetable[day]))
        self.week[day].resizeRowsToContents()

    def _update_teacher_table(self):
        self.cursor.execute('SELECT * FROM teacher ORDER BY full_name, subject_type')
        records = list(self.cursor.fetchall())
        self.teacher_table.removeCellWidget(self.teacher_table.rowCount() - 1, 0)
        self.teacher_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            rewriteButton = QPushButton("Rewrite")
            deleteRowButton = QPushButton("Delete")

            self.teacher_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.teacher_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.teacher_table.setCellWidget(i, 3, rewriteButton)
            self.teacher_table.setCellWidget(i, 4, deleteRowButton)
            rewriteButton.clicked.connect(lambda ch, key=int(r[0]), table=2: self._rewrite(key, table))
            deleteRowButton.clicked.connect(lambda ch, key=int(r[0]), table=2: self._delete(key, table))
        self.teacher_table.setRowCount(len(records) + 1)
        addRowButton = QPushButton("Add")
        self.teacher_table.removeCellWidget(self.teacher_table.rowCount() - 1, 1)
        self.teacher_table.removeCellWidget(self.teacher_table.rowCount() - 1, 2)
        self.teacher_table.setCellWidget(self.teacher_table.rowCount() - 1, 0, addRowButton)
        addRowButton.clicked.connect(lambda ch, table=2: self._add(table))

        self.teacher_table.resizeRowsToContents()

    def _update_subject_table(self):
        self.cursor.execute('SELECT name FROM subject ORDER BY name')
        records = list(self.cursor.fetchall())
        self.subject_table.removeCellWidget(self.subject_table.rowCount() - 1, 0)
        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            rewriteButton = QPushButton("Rewrite")
            deleteRowButton = QPushButton("Delete")

            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setCellWidget(i, 1, rewriteButton)
            self.subject_table.setCellWidget(i, 2, deleteRowButton)
            rewriteButton.clicked.connect(lambda ch, key=r[0], table=3: self._rewrite(key, table))
            deleteRowButton.clicked.connect(lambda ch, key=r[0], table=3: self._delete(key, table))

        addRowButton = QPushButton("Add")
        self.subject_table.removeCellWidget(self.subject_table.rowCount() - 1, 1)
        self.subject_table.removeCellWidget(self.subject_table.rowCount() - 1, 2)
        self.subject_table.setCellWidget(self.subject_table.rowCount() - 1, 0, addRowButton)
        addRowButton.clicked.connect(lambda ch, table=3: self._add(table))


        self.subject_table.resizeRowsToContents()

    def _update_subject_type_table(self):
        self.cursor.execute('SELECT name FROM subject_type ORDER BY name')
        records = list(self.cursor.fetchall())
        self.subject_type_table.removeCellWidget(self.subject_type_table.rowCount() - 1, 0)
        self.subject_type_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            rewriteButton = QPushButton("Rewrite")
            deleteRowButton = QPushButton("Delete")

            self.subject_type_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_type_table.setCellWidget(i, 1, rewriteButton)
            self.subject_type_table.setCellWidget(i, 2, deleteRowButton)
            rewriteButton.clicked.connect(lambda ch, key=r[0], table=4: self._rewrite(key, table))
            deleteRowButton.clicked.connect(lambda ch, key=r[0], table=4: self._delete(key, table))

        addRowButton = QPushButton("Add")
        self.subject_type_table.removeCellWidget(self.subject_type_table.rowCount() - 1, 1)
        self.subject_type_table.removeCellWidget(self.subject_type_table.rowCount() - 1, 2)
        self.subject_type_table.setCellWidget(self.subject_type_table.rowCount() - 1, 0, addRowButton)
        addRowButton.clicked.connect(lambda ch, table=4: self._add(table))

        self.subject_type_table.resizeRowsToContents()

    def _add(self, tableNum, *day):
        if tableNum == 1:
            self.cursor.execute("SELECT column_name FROM information_schema.columns "
                                "WHERE table_schema = 'public' AND table_name = 'timetable' ")
            columns = self.cursor.fetchall()
            print(day)
            if day:
                new_values = day[0]
            for temp in columns[3:]:
                text, ok = QInputDialog.getText(self, 'Add in timetable', 'Enter {} value:'.format(temp[0]))
                if ok and text != "":
                    new_values.append(text)
            if len(new_values) == 6:
                try:
                    self.cursor.execute("insert into "
                                        "timetable(week, day, study_time, subject, subject_type, room_numb) "
                                        "values (%s, %s, %s, %s, %s, %s);", tuple(new_values))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "Given subject/subject_type value "
                                                     "does not exist in subject/subject_type table")
        elif tableNum == 2:
            self.cursor.execute("SELECT column_name FROM information_schema.columns "
                                "WHERE table_schema = 'public' AND table_name = 'teacher' ")
            columns = self.cursor.fetchall()
            columns.pop(0)
            new_values = []
            for temp in columns:
                text, ok = QInputDialog.getText(self, 'Add in teacher', 'Enter {} value:'.format(temp[0]))
                if ok and text != "":
                    new_values.append(text)
            if len(new_values) == 3:
                try:
                    self.cursor.execute("insert into teacher(full_name, subject_type, subject) "
                                        "values (%s, %s, %s);", tuple(new_values))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "Given subject/subject_type value "
                                                     "does not exist in subject/subject_type table")
        elif tableNum == 3:
            text, ok = QInputDialog.getText(self, 'Add in subject', 'Enter subject name:')
            if ok and text != "":
                try:
                    self.cursor.execute("insert into subject values (%s);", (text,))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "This name is already used")
        elif tableNum == 4:
            text, ok = QInputDialog.getText(self, 'Add in subject_type', 'Enter subject type name:')
            if ok and text != "":
                try:
                    self.cursor.execute("insert into subject_type values (%s);", (text,))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "This name is already used")

    def _delete(self, keyWord, tableNum):
        if tableNum == 1:
            try:
                self.cursor.execute("delete from timetable where id = %s", (keyWord[0],))
                self.conn.commit()
            except:
                self.conn.commit()
                QMessageBox.about(self, "Error", "Error")
        elif tableNum == 2:
            try:
                self.cursor.execute("delete from teacher where id = %s", (keyWord,))
                self.conn.commit()
            except:
                self.conn.commit()
                QMessageBox.about(self, "Error", "Error")
        elif tableNum == 3:
            try:
                self.cursor.execute("delete from subject where name = %s", (keyWord,))
                self.conn.commit()
            except:
                self.conn.commit()
                QMessageBox.about(self, "Error", "The value is referenced in other tables")
        elif tableNum == 4:
            try:
                self.cursor.execute("delete from subject_type where name = %s", (keyWord,))
                self.conn.commit()
            except:
                self.conn.commit()
                QMessageBox.about(self, "Error", "The value is referenced in other tables")

    def _rewrite(self, keyWord, tableNum, *day):
        if tableNum == 1:
            self.cursor.execute("SELECT column_name FROM information_schema.columns "
                                "WHERE table_schema = 'public' AND table_name = 'timetable' ")
            columns = self.cursor.fetchall()
            new_values = []
            for temp in columns[3:]:
                text, ok = QInputDialog.getText(self, 'Rewrite timetable', 'Enter new {} value:'.format(temp[0]))
                if ok and text != "":
                    new_values.append(text)
            if len(new_values) == 4:
                new_values.append(keyWord[0])
                try:
                    self.cursor.execute("update timetable " 
                                        "set study_time = %s, subject = %s, subject_type = %s, room_numb = %s "
                                        "where id = %s", tuple(new_values))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "Given subject/subject_type value "
                                                     "does not exist in subject/subject_type table")
        elif tableNum == 2:
            self.cursor.execute("SELECT column_name FROM information_schema.columns "
                                "WHERE table_schema = 'public' AND table_name = 'teacher' ")
            columns = self.cursor.fetchall()
            columns.pop(0)
            new_values = []
            for temp in columns:
                text, ok = QInputDialog.getText(self, 'Rewrite teacher', 'Enter new {} value:'.format(temp[0]))
                if ok and text != "":
                    new_values.append(text)
            if len(new_values) == 3:
                new_values.append(keyWord)
                try:
                    self.cursor.execute("update teacher " 
                                        "set full_name = %s, subject_type = %s, subject = %s "
                                        "where id = %s", tuple(new_values))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "Given subject/subject_type value "
                                                     "does not exist in subject/subject_type table")
        elif tableNum == 3:
            text, ok = QInputDialog.getText(self, 'Rewrite subject', 'Enter new subject name:')
            if ok and text != "":
                try:
                    self.cursor.execute("update subject set name = %s where name = %s", (text, keyWord))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "Invalid value or the value is referenced in other tables")
        elif tableNum == 4:
            text, ok = QInputDialog.getText(self, 'Rewrite subject_type', 'Enter new subject type name:')
            if ok and text != "":
                try:
                    self.cursor.execute("update subject_type set name = %s where name = %s", (text, keyWord))
                    self.conn.commit()
                except:
                    self.conn.commit()
                    QMessageBox.about(self, "Error", "Invalid value or the value is referenced in other tables")

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
