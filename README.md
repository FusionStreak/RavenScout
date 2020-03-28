# RavenScout(Not released, still in development)
 Webtool for aggragate scouting for FRC Teams

## What is this?
* A webtool to allow anyone with scouting data, in a standardised CSV file, to upload their data
* Generates summaries and visuals using all the data collected 
* All original files are stored for human review in the case of errors
* Pulls some data from FMS/TheBlueAlliance
* Each new Year/Season a new standard for CSV files will have to be released and the application will be updated

## TODO
* Connect file submission to DB
* Generate visuals
* Advanced Calculations
* Pull data from FMS/TheBlueAlliance
* Make form that receives csv file, put in database, validate from TBA(categories we can), show on website in visualization

## How to Develop
* Clone the repo
* Requirements:
    * NodeJS
    * Python 3.7+ (add to "PATH")
    * pip
* Run `$ sh requirements.sh` to install pip and npm requirements for development
* Run `$ flask` to show run/development options
