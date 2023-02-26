import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()

        self.num_1 = "Null"
        self.num_2 = "Null"
        self.op = "Null"

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_fourth = QHBoxLayout()
        self.hbox_fifth = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_fourth)
        self.vbox.addLayout(self.hbox_fifth)

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)
        self.input.setText("0")
        self.input.setReadOnly(True)

        self.b_ac = QPushButton("AC", self)
        self.b_c = QPushButton("C", self)
        self.b_b = QPushButton("<-", self)
        self.b_div = QPushButton("/", self)

        self.b_7 = QPushButton("7", self)
        self.b_8 = QPushButton("8", self)
        self.b_9 = QPushButton("9", self)
        self.b_mul = QPushButton("*", self)

        self.b_4 = QPushButton("4", self)
        self.b_5 = QPushButton("5", self)
        self.b_6 = QPushButton("6", self)
        self.b_sub = QPushButton("-", self)

        self.b_1 = QPushButton("1", self)
        self.b_2 = QPushButton("2", self)
        self.b_3 = QPushButton("3", self)
        self.b_sum = QPushButton("+", self)

        self.b_00 = QPushButton("00", self)
        self.b_0 = QPushButton("0", self)
        self.b_comma = QPushButton(",", self)
        self.b_result = QPushButton("=", self)

        self.hbox_first.addWidget(self.b_ac)
        self.hbox_first.addWidget(self.b_c)
        self.hbox_first.addWidget(self.b_b)
        self.hbox_first.addWidget(self.b_div)

        self.hbox_second.addWidget(self.b_7)
        self.hbox_second.addWidget(self.b_8)
        self.hbox_second.addWidget(self.b_9)
        self.hbox_second.addWidget(self.b_mul)

        self.hbox_third.addWidget(self.b_4)
        self.hbox_third.addWidget(self.b_5)
        self.hbox_third.addWidget(self.b_6)
        self.hbox_third.addWidget(self.b_sub)

        self.hbox_fourth.addWidget(self.b_1)
        self.hbox_fourth.addWidget(self.b_2)
        self.hbox_fourth.addWidget(self.b_3)
        self.hbox_fourth.addWidget(self.b_sum)

        self.hbox_fifth.addWidget(self.b_00)
        self.hbox_fifth.addWidget(self.b_0)
        self.hbox_fifth.addWidget(self.b_comma)
        self.hbox_fifth.addWidget(self.b_result)

        self.b_00.clicked.connect(lambda: self._button("00"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_comma.clicked.connect(lambda: self._button("."))
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))

        self.b_div.clicked.connect(lambda: self._operation("/"))
        self.b_mul.clicked.connect(lambda: self._operation("*"))
        self.b_sub.clicked.connect(lambda: self._operation("-"))
        self.b_sum.clicked.connect(lambda: self._operation("+"))
        self.b_result.clicked.connect(lambda: self._result())

        self.b_ac.clicked.connect(lambda: self._allclear())
        self.b_c.clicked.connect(lambda: self._clear())
        self.b_b.clicked.connect(lambda: self._back())

    def _allclear(self):
        self.input.setText("0")
        self.num_1 = "Null"
        self.num_2 = "Null"
        self.op = "Null"
        self.streak = 0

    def _clear(self):
        self.input.setText("0")
        self.streak = 0

    def _back(self):
        line = self.input.text()
        if line[:-1]:
            self.input.setText(line[:-1])
        else:
            self.input.setText("0")
        self.streak = 0

    def _button(self, param):
        line = self.input.text()
        if param != "." and float(line) == 0 and line.count(".") != 1:
            if param == "00":
                self.input.setText("0")
            else:
                self.input.setText(param)
        elif param != "." or line.count(".") != 1:
            self.input.setText(line + param)
        self.streak = 0

    def _operation(self, op):
        if self.input.text():
            self.num_1 = float(self.input.text())
        self.op = op
        self.input.setText("0")
        self.streak = 0

    def _result(self):
        if self.input.text() and self.streak != 1:
            self.num_2 = float(self.input.text())
        if self.op == "+":
            if self.num_1 != "Null" and self.num_2 != "Null":
                if int(self.num_1 + self.num_2) == self.num_1 + self.num_2:
                    self.input.setText(str(int(self.num_1 + self.num_2)))
                else:
                    self.input.setText(str(self.num_1 + self.num_2))
        elif self.op == "-":
            if int(self.num_1 - self.num_2) == self.num_1 - self.num_2:
                self.input.setText(str(int(self.num_1 - self.num_2)))
            else:
                self.input.setText(str(self.num_1 - self.num_2))
        elif self.op == "*":
            if int(self.num_1 * self.num_2) == self.num_1 * self.num_2:
                self.input.setText(str(int(self.num_1 * self.num_2)))
            else:
                self.input.setText(str(self.num_1 * self.num_2))
        elif self.op == "/":
            if self.num_2 != 0:
                if int(self.num_1 / self.num_2) == self.num_1 / self.num_2:
                    self.input.setText(str(int(self.num_1 / self.num_2)))
                else:
                    self.input.setText(str(self.num_1 / self.num_2))
        self.num_1 = float(self.input.text())
        self.streak = 1


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())
