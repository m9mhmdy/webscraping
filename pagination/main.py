#=======================#
import csv
import scrape
from time import sleep
#=======================#

### Configuration ###
#=======================#
# The Path of the output file
# which is in CSV format
OUTPUT = 'output.csv'

# The Path of a text file that
# keeps track of processed URLs
DONE = 'DONE.txt'
#=======================#


#=======================#
def main():
    # Load the already processed URLs
    try:
        with open(DONE, 'r') as done:
            processed_urls = [line.strip() for line in done.readlines()]
    except:
        # Handle the first run (file not created yet)
        processed_urls = []

    # Open the processed URLs file
    processed_urls_file = open(DONE, 'a')
    revisit = False

    # Start scraping
    with open(OUTPUT, 'a', encoding='utf-8', newline='\n') as outpt:
        outpt_writer = csv.writer(outpt)

        # Extract the pages
        pages = scrape.get_pages()
        if pages is None:
            print("Error: Couldn't retrieve website pages\nPlease try again later")
            quit()

        # and for each one
        for page in pages[:1]:
            # Skip if it has been processed
            if page in processed_urls:
                continue

            # Extract its items
            items = scrape.extract_items_urls(page)
            # Skip if couldn't extract the items
            if items is None:
                continue

            for item in items:
                # Skip the item if it has been processed
                if item in processed_urls:
                    continue

                # Extract the item data
                item_data = scrape.scrape_item_data(item)
                # Skip the item if couldn't scrape its data
                if item_data is None:
                    revisit = True
                    continue

                # Save the item's scraped data and its URL
                outpt_writer.writerow(item_data)
                processed_urls_file.write(item + "\n")

                sleep(2)

            if not revisit:
                # Write the page URL to the processed URLs file
                # if (and only if) all of its items
                # were scraped w/o any issues
                processed_urls_file.write(page + "\n")


    processed_urls_file.close()
#=======================#


### Start working ###
#=======================#
if __name__ == '__main__':
    main()
#=======================#
