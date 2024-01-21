import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QPushButton, QMessageBox, QSizePolicy
from PyQt5.QtGui import QTextCursor
import requests

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Top News Headlines")

        layout = QVBoxLayout()

        self.news_browser = QTextBrowser()
        self.news_browser.setOpenExternalLinks(True)  # Enable clickable hyperlinks
        self.news_browser.setStyleSheet("font-size: 14px; color: #000000;")  # Set font size and text color
        layout.addWidget(self.news_browser)

        fetch_button = QPushButton("Fetch News")
        fetch_button.clicked.connect(self.fetch_news)
        fetch_button.setStyleSheet("background-color: #87CEEB; color: #000000;")  # Set button color and text color
        layout.addWidget(fetch_button)

        self.setLayout(layout)

        # Set a minimum size for the window
        self.setMinimumSize(800, 600)

    def get_top_news(self, api_key):
        try:
            url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
            response = requests.get(url)

            response.raise_for_status()  # Raise an HTTPError for bad responses

            news_data = response.json()
            articles = news_data.get('articles', [])
            return articles
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch news. {str(e)}")
            return None

    def fetch_news(self):
        # Replace 'YOUR_API_KEY' with your actual News API key
        api_key = '05a5f10653e2403a85ee3d25a56783c8'
        news_articles = self.get_top_news(api_key)

        self.news_browser.clear()

        if news_articles:
            first_5_headlines = news_articles[:5]
            last_5_headlines = news_articles[-5:]

            self.news_browser.append("<b> 5 Most Reported Stories:</b>")
            self.news_browser.append("<br>")  # Add an extra line for spacing

            for idx, article in enumerate(first_5_headlines, start=1):
                hyperlink = f"<span style=\"font-size: 16px;\">{article['title']}</span><br>{article['description']}<br><a href=\"{article['url']}\">Read more</a>: {article['url']}<br><br>"
                self.news_browser.insertHtml(hyperlink)

            self.news_browser.append("<br>")  # Add an extra line for spacing

            self.news_browser.append("<b> 5 Least Reported Stories:</b>")
            self.news_browser.append("<br>")  # Add an extra line for spacing

            for idx, article in enumerate(last_5_headlines, start=len(news_articles) - 4):
                hyperlink = f"<span style=\"font-size: 16px;\">{article['title']}</span><br>{article['description']}<br><a href=\"{article['url']}\">Read more</a>: {article['url']}<br><br>"
                self.news_browser.insertHtml(hyperlink)

            # Make the window full screen
            self.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewsApp()
    window.show()
    sys.exit(app.exec_())
