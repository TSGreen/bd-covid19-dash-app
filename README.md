# Data Dash for Covid-19 Data for Bangladesh

Repo for deploying a data visulation web-app of COVID-19 data in Bangladesh to Heroku. 

This app is built using Dash in Python and displays interactive Plotly visualtions. 

The data used in this repo is scraped, cleaned and analysed regularly and fed into the app. 

The app is avilable [here on Heroku](https://bangladesh-covid19.herokuapp.com/). 
Note it is deployed on Heroku's free tier so may take some time to wake from sleep. Please be patient!

The web app includes the daily test, case, death and recovery numbers along with 7-day rolling averages:
![image](https://user-images.githubusercontent.com/62939263/117174375-749a7280-adef-11eb-8634-08028e76bb94.png)

It also includes the daily positivity rate:
![image](https://user-images.githubusercontent.com/62939263/117174620-ba573b00-adef-11eb-8de9-c13d3ed35ee9.png)

It also shows the regional data on an interactive map:
![image](https://user-images.githubusercontent.com/62939263/117175117-4d907080-adf0-11eb-83db-f6ea66add389.png)
