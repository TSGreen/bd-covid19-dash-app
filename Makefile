all: scrape deploy

scrape:
	@echo "Scraping latest data"
	@python scrape_timeseries_data.py
	@python scrape_district_data.py 

deploy:
	@echo "Pushing to GitHub"
	@git add --all
	@git commit -m "Data update"
	@git push

