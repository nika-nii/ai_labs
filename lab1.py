import sys
from annealing import run
from PySide2.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QWidget,
    QLabel
)
import matplotlib.pyplot as plt
from PySide2.QtCore import SIGNAL, Slot, QObject
from PySide2.QtGui import QFont

class Application(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.layout = QHBoxLayout()

        self.inputLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.nForm = QLineEdit("9")
        self.temp_start_Form = QLineEdit('30')
        self.temp_stop_Form = QLineEdit('0.5')
        self.alphaForm = QLineEdit('0.98')
        self.stepsForm = QLineEdit('1000')
        self.runButton = QPushButton("Запустить")
        self.boardLabel = QLabel("")
        chessFont = QFont("Consolas", 12)
        self.boardLabel.setFont(chessFont)

        self.visualLayout = QVBoxLayout()
        self.visualLayout.addWidget(self.boardLabel)

        self.formLayout.addRow("N:", self.nForm)
        self.formLayout.addRow("Tmax:", self.temp_start_Form)
        self.formLayout.addRow("Tmin:", self.temp_stop_Form)
        self.formLayout.addRow("alpha:", self.alphaForm)
        self.formLayout.addRow("Кол-во шагов:", self.stepsForm)

        self.inputLayout.addLayout(self.formLayout)
        self.inputLayout.addWidget(self.runButton)

        self.layout.addLayout(self.inputLayout)
        self.layout.addLayout(self.visualLayout)
        self.setLayout(self.layout)

        QObject.connect(self.runButton, SIGNAL('pressed()'), self.run_solve)

    @Slot()
    def run_solve(self):
        plt.close()
        (temp_start, temp_stop, alpha, steps, n) = (
            float(self.temp_start_Form.text()),
            float(self.temp_stop_Form.text()),
            float(self.alphaForm.text()),
            int(self.stepsForm.text()),
            int(self.nForm.text())
        )
        solution = run(temp_start, temp_stop, alpha, steps, n)
        if solution['final_energy'] != 0:
            self.boardLabel.setText('Решение не найдено' + '\nЛучшее решение ' + str(solution['final_energy']))
        else:
            self.boardLabel.setText(solution['solution'])
        g_step, g_temp, g_energy, g_bad_decisions = solution['plot_data']
        plt.title("График")
        plt.grid()
        plt.xlabel('Шаги')
        plt.ylabel('Количество')
        plt.plot(g_step, g_temp, label="Температура")
        plt.plot(g_step, g_energy, label="Энергия")
        plt.plot(g_step, g_bad_decisions, label="Плохие решения")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Application()
    widget.show()

    sys.exit(app.exec_())