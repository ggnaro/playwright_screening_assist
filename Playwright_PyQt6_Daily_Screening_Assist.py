from PyQt6 import QtWidgets, QtCore
import sys
from playwright.sync_api import sync_playwright
import datetime
import os

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Screening Assist')
        self.resize(400, 210)
        self.ui()
        self.status = False

    def ui(self):
        self.label_1 = QtWidgets.QLabel('請輸入Chrome瀏覽器使用者資料位置:')
        self.input_1 = QtWidgets.QLineEdit(self)   # 第一個輸入框
        # self.input_1.move(120,20)
        # self.input_1.setGeometry(10, 30, 100, 10)

        self.label_2 = QtWidgets.QLabel('輸入欲截圖目標網址:')
        self.input_2 = QtWidgets.QLineEdit(self)   # 第二個輸入框
        # self.input_2.move(120, 50)
        # self.input_2.setGeometry(20,50,100,20)

        self.label_3 = QtWidgets.QLabel('截圖檔案命名名稱:')
        self.input_3 = QtWidgets.QLineEdit(self)   # 第三個輸入框
        # self.input_3.move(120, 80)

        self.label_T = QtWidgets.QLabel('每日截圖時間(時:分):')
        # time select
        self.t1 = QtWidgets.QTimeEdit(self)
        # self.t1.setGeometry(20, 20, 120, 30)
        # self.t1.setDisplayFormat('hh:mm:ss')
        # self.t1.setTimeRange(QtCore.QTime(00, 00, 00), QtCore.QTime(24, 00, 00))
        self.t1.setDisplayFormat('hh:mm')
        self.t1.setTimeRange(QtCore.QTime(00, 00), QtCore.QTime(24, 00))

        self.label_4 = QtWidgets.QLabel('')
        self.label_5 = QtWidgets.QLabel('')
        self.label_6 = QtWidgets.QLabel('')
        self.box = QtWidgets.QWidget(self)
        # self.box.setGeometry(10,10,200,150)

        self.layout = QtWidgets.QFormLayout(self.box)
        self.layout.addRow(self.label_1, self.input_1)
        self.layout.addRow(self.label_2, self.input_2)
        self.layout.addRow(self.label_3, self.input_3)
        self.layout.addRow(self.label_T, self.t1)
        self.layout.addRow(self.label_4)
        self.layout.addRow(self.label_5)
        self.layout.addRow(self.label_6)

        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText('Submit')
        self.btn1.setGeometry(110, 155, 100, 50)
        self.btn1.clicked.connect(self.submit_text)

        self.btn2 = QtWidgets.QPushButton(self)
        self.btn2.setText('Cancel')
        self.btn2.setGeometry(210, 155, 100, 50)
        self.btn2.clicked.connect(self.clean_text)

    def hide_clock(self):
        self.now2 = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime('%H:%M:%S')
        return self.now2

    def clean_text(self):
        self.status = False
        self.input_1.setText('')
        self.input_2.setText('')
        self.input_3.setText('')
        self.label_4.setText('')
        self.label_5.setText('')

    def submit_text(self):
        self.status = True
        global browser_path, target_URL, file_name, now , today, selected_time
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        today = datetime.date.today()

        browser_path = self.input_1.text()
        target_URL = self.input_2.text()
        file_name = self.input_3.text()
        selected_time = self.t1.time().toString()


    def clock(self):
        self.now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime('%H:%M:%S')
        self.label_6.setText(self.now)
        if self.status == True:
            selected_time = self.t1.time().toString()
            if selected_time[:5] == self.hide_clock()[:5]:
                self.label_4.setText("Done! The screen file saved at: ")
                self.label_5.setText(
                    str(os.getcwd()) + "\\" + file_name + "_" + str(today) + "_" + selected_time + ".png")
                self.execut_screen()

    def execut_screen(self):
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=browser_path,
                channel="chrome",
                slow_mo=10000,
                headless=True
            )
            page = browser.new_page()
            page.goto(target_URL)
            img = page.screenshot(path="./" + file_name +"_"+ str(today) + "_" + selected_time[0:2]+selected_time[3:5] +".png")
            page.close()
            browser.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(Form.clock)
    timer.start(1000)
    sys.exit(app.exec())