import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QTextCursor
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

class PpomppuCrawler(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ppomppu Crawler and Plotter')

        self.layout = QVBoxLayout()

        self.label = QLabel('검색어를 입력하세요:')
        self.layout.addWidget(self.label)

        self.search_input = QLineEdit(self)
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton('검색 및 그래프 표시', self)
        self.search_button.clicked.connect(self.search_and_plot)
        self.layout.addWidget(self.search_button)

        self.setLayout(self.layout)

    def search_and_plot(self):
        search_query = self.search_input.text()
        if search_query:
            data = self.crawl_ppomppu(search_query)
            if data:
                self.plot_graph(data)
        else:
            self.label.setText('검색어를 입력하세요.')

    def crawl_ppomppu(self, search_query):
        all_data = []
        page_number = 1
        while True:
            url = f'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&keyword={search_query}&page={page_number}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            result_titles = soup.select('.list_title')
            result_dates = soup.select('.eng.list_vspace')

            if not result_titles:
                break

            for title, date in zip(result_titles, result_dates):
                title_text = title.text.strip()
                date_text = date.text.strip()
                all_data.append({'title': title_text, 'date': date_text})

            page_number += 1
            print(all_data)
        return all_data

    def plot_graph(self, data):
        shopping_info = {'mall': [], 'product': [], 'price': [], 'date': []}

        for entry in data:
            # 여기에서 쇼핑몰/상품 이름/가격을 추출하는 코드를 작성하세요.
            # 예를 들어, 간단한 구분자로 가정하고 "쇼핑몰:상품:가격" 형식으로 나누겠습니다.
            parts = entry['title'].split(':')
            if len(parts) == 3:
                shopping_info['mall'].append(parts[0])
                shopping_info['product'].append(parts[1])
                shopping_info['price'].append(parts[2])
                shopping_info['date'].append(datetime.strptime(entry['date'], '%y/%m/%d %H:%M'))

        plt.figure(figsize=(10, 6))
        for i, mall in enumerate(shopping_info['mall']):
            plt.scatter(shopping_info['date'][i], int(shopping_info['price'][i]), label=mall)

        plt.title('Shopping Information Over Time')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PpomppuCrawler()
    ex.show()
    sys.exit(app.exec_())
