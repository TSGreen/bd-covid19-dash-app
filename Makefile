all: scrape process deploy

scrape:
	@echo "Scraping latest data ..."
	@python scrape_national_tsdata.py
	@python scrape_regional_data.py
	@echo "Data scraped."

	
process:
	@echo "Processing raw data ..." 
	@python process_national_tsdata.py
	@python process_regionaldata.py
	@echo "Data processed."

deploy:
	@echo "Pushing to GitHub ..."
	@git add --all
	@git commit -m "Data update"
	@git push
	@echo "Deploy complete."

