# sqlalchemy-challenge

Kathy Harris – Submission of SQLAlchemy Homework – Surf’s Up!


In this assignment, I was tasked to research climate information for my vacation to Hawaii using SQLAlchemy to help with my trip planning.  First step was to do a Climate Exploration and analyze both precipitation and temperature observations of the weather stations in provided in Hawaii.sqllite .  Please see Climate_Starter_Homework.ipynb for this analysis. The second step was to design a Flask API to display the results of my queries.  Please see app.py for that step.  The following routes were created:


Routes

•	/ 	 			                Home page that list all routes

•	/api/v1.0/precipitation		Dictionary of the Date and Precipitation

•	/api/v1.0/stations 		    Lists the stations in the dataset

•	/api/v1.0/tobs			      Lists the temperature data over the last    12 months available for Waihee – the most active station

•	/api/v1.0/<start> 		    Lists the maximum, minimum and average temperatures (In that order) from January 1, 2017, to latest date in the dataset
  
•	/api/v1.0/<start>/<end>	  Lists the maximum, minimum and average temperatures (In that order) in February 2017 
