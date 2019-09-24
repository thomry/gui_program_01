from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QAction, QPushButton, qApp, QGridLayout, QLabel, QLineEdit, QTableWidget, QMessageBox, QDialog, QTableWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from search import Search, SearchOption
from book import Book
import sys

#QLineEdit는 한줄만 QTextedit는 게시판등 만드는 여러줄 수정해야할 때

class MainWindow(QWidget):

    exitAction    = None
    menubar       = None
    search_btn    = None
    search_input  = None
    search_option = SearchOption()
    table         = None

    search = Search(
        client_id       = 'znxvtMFwOB8wuolycdgS'
        , client_secret = '09_MqrPUqg'
    )


    def __init__(self):        #파이썬이 만들어졌을때 자동으로 실행된다
        super().__init__()     #super()은 자기 부모 클래스를 의미 => 자신를 실행하며 부모클래스를 실행
        self.init_ui()         #Qmainwindow안의 함수

    #Exit 액션 만들기
    def createExitAction(self):
        self.exitAction = QAction(QIcon('img/exit.png'), '끝내기', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('어플리케이션 끝내기')
        self.exitAction.triggered.connect(qApp.exit)

    # MenuBar에 메뉴 추가하기
    def addMenu(self,menuName,action):
        menu = self.menubar.addMenu(menuName)
        menu.addAction(action)

    # 윈도우 띄우기
    def showWindow(self, w, h):
        self.setWindowTitle('Main Window')
        self.setWindowIcon(QIcon('img/snowflake.png'))
        self.resize(w,h)
        self.show()

    #UI 초기화
    def init_ui(self):
        #self.createExitAction()

        #self.menubar = self.menuBar()
        #self.menubar.setNativeMenuBar(False)
        #self.addMenu('&File',self.exitAction)

        #self.statusBar().showMessage('Ready')

        grid = QGridLayout()            #gridlayout생성
        self.setLayout(grid)            #grid에 layout생성

        self.table = QTableWidget(self)
        self.table.setColumnCount(10)
        self.table.setRowCount(100)
        self.table.setHorizontalHeaderLabels(['제목','링크','이미지','저자','가격','할인가','출판사','출판일','ISBN','설명'])    #수평(가로)의헤더라벨을 넣음 가로는 vertical

        self.search_btn = QPushButton('검색')                          #전역으로 만들어야 다른 함수에서도 사용할수있음.
        self.search_btn.clicked.connect(self.onSearchClick)            #클릭을하면 onSearchClick함수로 연결이됨

        self.search_input = QLineEdit()

        grid.addWidget(QLabel('검색어: '), 0, 0)                   #검색어: 를 절대좌표 (0,0)에 넣음
        grid.addWidget(self.search_input, 0, 1)                    #입력창이 절대좌표 (0,1)에 넣음
        grid.addWidget(self.search_btn,0,2)
        grid.addWidget(self.table,1,0,1,3)                              #column 1줄을 전부쓸것이라는 명령어
        self.showWindow(500, 350)

    def onSearchClick(self):
        searchTxt = self.search_input.text()

        if searchTxt == '' or len(searchTxt) == 0:
            QMessageBox.about(self,"문제가 발생했습니다!",'검색어를 입력해주세요!')
            return

        self.search_option.query = searchTxt
        self.search_option.display = 100
        self.search.request(self.search_option)
        #print(self.search_input.text())
        #QMessageBox(None,'message',self.search_input.text())

        self.parseSearchData()

    def parseSearchData(self):
        items = self.search.get_items()
        books = []
        self.table.setRowCount(len(items))

        for data in items:
            book = Book()
            book.parser( data )

            idx = items.index( data )
            self.table.setItem(idx, 0, QTableWidgetItem(book.title))
            self.table.setItem(idx, 1, QTableWidgetItem(book.link))
            self.table.setItem(idx, 2, QTableWidgetItem(book.image_url))
            self.table.setItem(idx, 3, QTableWidgetItem(book.author))
            self.table.setItem(idx, 4, QTableWidgetItem(str(book.price)))
            self.table.setItem(idx, 5, QTableWidgetItem(str(book.discount)))
            self.table.setItem(idx, 6, QTableWidgetItem(book.publisher))
            self.table.setItem(idx, 7, QTableWidgetItem(str(book.pubdate)))
            self.table.setItem(idx, 8, QTableWidgetItem(book.isbn))
            self.table.setItem(idx, 9, QTableWidgetItem(book.description))
            books.append( book )
            print(book)




if __name__ == '__main__':       #파이썬 파일이름이 main이니?라고 물어보고 있습니다. 실행하는 순간에 '__'가 들어가며 한번만 열기위해서임.
    app = QApplication(sys.argv)
    win = MainWindow()           #mainwindow를 instance화시킴
    sys.exit(app.exec_())        #지금 설명은 안하는데 일단 프로그램 종료하는 명령어임만 알아둘 것