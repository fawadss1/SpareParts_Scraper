from scrapy.utils.project import get_project_settings
import scrapy, base64, json, re, csv

settings = get_project_settings()
headers = settings.get('HEADERS')


class SparePartsSpider(scrapy.Spider):
    name = "SpareParts-Spider"

    def __init__(self, url=None, categories_url=None, *args, **kwargs):
        super(SparePartsSpider, self).__init__(*args, **kwargs)
        self.url = url
        self.categories_url = categories_url

        self.csv_file = open('export/spareParts_data.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=["Part Name", "Manufacturer", "Compatible Car Models", "Price", "Stock Availability"])
        self.csv_writer.writeheader()

    handle_httpstatus_list = [403, 404, 502, 520]

    def start_requests(self):
        print("Starting Request")
        if self.url:
            print(f"Start Request at product Url {self.url}")
            yield scrapy.Request(self.url, headers=headers, callback=self.parse)

        elif self.categories_url:
            print(f"Start Request at categories Url {self.categories_url}")
            yield scrapy.Request(self.categories_url, headers=headers, callback=self.parseAllCats)
        
        else:
            print("No URL provided")

    def parseAllCats(self, response):
        print("Parsing All Cats")
        for link in response.xpath("//ul[@id='navigation']//a/@href").getall():
            yield scrapy.Request(url=response.urljoin(link), headers=headers, callback=self.parseCat)


    def parseCat(self, response):
        categories = response.xpath("//div[@class='categories']//ul//li//span/@data-base64").getall()
        if len(categories) > 0:
            print('Parsing Cat', response.url)
            for encoded_url in categories:
                decoded_url = response.urljoin(base64.b64decode(encoded_url).decode('utf-8'))                
                yield scrapy.Request(url=decoded_url, headers=headers, callback=self.parseCat)
        else:
            for encoded_url in response.xpath("//div[@class='art-name']/span[contains(@class,'underline')]/@data-base64").getall():
                decoded_url = response.urljoin(base64.b64decode(encoded_url).decode('utf-8'))                
                print('Getting Items', decoded_url)
                yield scrapy.Request(url=decoded_url, headers=headers, callback=self.parse)
            
            pagination = response.xpath("//div[@class='pagination']//span[contains(@class, 'paginationLink next')]/@data-base64").get()
            if pagination:
                nxt_pg_decoded_url = response.urljoin(base64.b64decode(pagination).decode('utf-8'))                
                print('Getting Next page items', nxt_pg_decoded_url)
                yield scrapy.Request(url=nxt_pg_decoded_url, headers=headers, callback=self.parseCat)


    def parse(self, response):
        if response.status != 200:
            return
        
        print('Parsing item', response.url)

        script_text = response.xpath("//script[contains(text(), 'dataLayer')]/text()").get()
        
        if script_text:
            match = re.search(r'dataLayer\.push\(\.\.\.(\[[\s\S]+?\])\);', script_text)
            if match:
                json_text = match.group(1)

                try:
                    data = json.loads(json_text)
                    
                    page_data = data[0].get("page", {})
                    product = page_data.get("products", [{}])[0]
                    content_group = page_data.get("contentGroup", [])

                    row = {
                        "Part Name": product.get("name", "N/A"),
                        "Manufacturer": product.get("brand", "N/A"),
                        "Compatible Car Models": content_group[0] if content_group else "N/A",
                        "Price": product.get("price", "N/A"),
                        "Stock Availability": product['quantity'] or "N/A"
                    }
                    self.csv_writer.writerow(row)

                except Exception as e:
                    print("JSON parsing error: %s", e)