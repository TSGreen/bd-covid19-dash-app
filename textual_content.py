"""
This script contains the textual comments for the web-app. 

@author: Tim Green 
Created: May 2021
"""

class TextualContent():
    """Class for storing the textual content for the web-app."""
    
    def __init__(self):
        pass
    
    def introduction(self, latest_update):
        text = f"""
        An interactive exploration of Covid-19 data for Bangladesh.
        
        Data source: [IEDCR](https://iedcr.gov.bd/).
        Data on this page last updated: {latest_update.day} \
            {latest_update.month_name()} {latest_update.year}.
        """
        return text 
    
    def daily_data(self):
        text = """
        #### Comments:
        * The number of daily confirmed cases appeared to level out and 
        decrease at the beginning of July, but this very closely maps the 
        decrease in testing at this time, so it most likely to be due to 
        insufficient testing. The rate of testing declined almost immediately 
        after the government announced on 29 June that a charge would be 
        imposed for COVID tests (which had hitherto been free at government 
        run facilities).
        * It is encouraging that by late August, despite the number of daily 
        tests leveling out at a slightly higher rate than in July, there is 
        modest decline in number of confirmed daily cases.
        * The daily figures vary with day of the week, with lower numbers 
        reported on weekends and higher numbers mid-week (Tues & Weds).
        * Significant drops in the daily figures were observed around 26 May 
        2020, 2 August 2020 and 14 May 2021 because of the Eid holidays at 
        these times.
        * There is a spike in recoveries on 15 June due to a change in 
        reporting policy. The health ministry included recoveries at home 
        (i.e. outside of hospitals) from this date.
        * The WHO have suggested a positivity rate below 5% is indicative 
        that an outbreak is under control. In Bangladesh the positivity rate 
        remained above 5% from 5 April 2020 right up until around mid-December
        2020. The positivity rate again rose to above five per cent in 
        mid-March 2021 where it remains (true as of 02/07/21). 
        """
        return text
    
    def regional_data(self, totalcases_regional, totalcases_national):
        text = f"""
        #### Comments:
        * These numbers are now outdated as their publication was ceased on 15/12/20.
        However, they are still useful as an illustrative distribution of cases around 
        the country.
        It should be noted that during the course of 2020, there was little 
        variation in how cases were geographically spread  being concentrated
         on the large urban areas, in particular Dhaka city.   
        * For reader's reference, the sum of all the regional data published 
        as of 15/12/20 was {totalcases_regional}, but the total confirmed cases 
        nationwide now stands at {totalcases_national}.                                                                               
        """
        return text

    def page_credit(self):
        text = """
        Page built in Python by [Timothy Green](https://github.com/TSGreen). 
        [Source code](https://github.com/TSGreen/bd-covid19-dash-app).
        """
        return text
