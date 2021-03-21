import time
import logging
from helpers import init_logging, WebDriver, WebCrawler, crawl
from multiprocessing import Pool

###
# Initialize logging
init_logging()
logging.info("Program launched.")

# Initialize webdriver class
driver_obj = WebDriver()
driver_obj.run()

# Browse to drugs page
driver_obj.browse_to_drugs()

# Create partitions
n_partitions = 4
partitions = driver_obj.get_partitions(n_partitions=n_partitions)
driver_obj.exit()

# partitions = [(1, 77), (78, 154), (155, 232), (233, 309)]

# Create n driver objects
driver_list = [WebDriver() for i in range(n_partitions)]
crawler_list = [WebCrawler(driver=driver_list[i].driver, file_number=i+1, page_range=partitions[i])
                for i in range(n_partitions)]

for driver in driver_list:
    driver.run()

with Pool(n_partitions) as p:
    p.map(crawl, crawler_list)
