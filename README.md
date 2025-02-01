# SpareParts Scraper

This is a Scrapy-based web scraper designed to extract data from websites related to spare parts.

## Key Features
- Crawl and extract spare parts data.
- Store scraped data in csv format.
- Handle pagination and dynamic content.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/fawadss1/SpareParts_Scraper.git
cd SpareParts_Scraper
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install scrapy
```

## 🕷️ Running the Scrapy Spider

### 1. Run the Spider
```sh
python Run_Spider.py
```

## ⚙️ Project Structure
```
SpareParts_Scraper/
│── spiders/           # Contains Scrapy spiders
│── scrapy.cfg         # Scrapy project configuration file
│── items.py           # Defines data structure for scraped items
│── middlewares.py     # Scrapy middlewares
│── pipelines.py       # Data processing pipeline
│── settings.py        # Project settings
│── README.md          # This file
export/                # This Directory contians the output spareParts_data.csv
Run_Spider             # This script is run the spider
```

