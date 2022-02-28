import numpy as np

#import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station



# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]<br/>"
        f'/api/v1.0/[start]/[end]'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation values
    precipitation_info = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_info.append(precipitation_dict)

    return jsonify(precipitation_info)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    ##Find most active stations temps for last year
    sel_active = [measurement.date, measurement.tobs]
    date_str = "2016-08-23"
    waihee = "USC00519281"

    ##results = session.query(measurement.station, measurement.tobs)(*sel_active).\
    results = session.query(*sel_active).\
        filter(measurement.date> date_str).\
        filter(measurement.station == waihee).\
        group_by(measurement.date).\
        order_by(measurement.date.desc()).all()

    session.close()

        # Create a dictionary from the row data and append to a tempurature list for most Waihee
    waihee_temps = []
    for station, tobs in results:
        waihee_temp_dict = {}
        waihee_temp_dict["station"] = station
        waihee_temp_dict["tobs"] = tobs
        waihee_temps.append(waihee_temp_dict)

    return jsonify(waihee_temps)


@app.route("/api/v1.0/[start]")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    ##Find the min, max and average temps reported starting in Y 2017
    sel_summary = [func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs)]
    date_str = "2016-12-31"

    
    results = session.query(*sel_summary).\
        filter(measurement.date> date_str).all()


    session.close()

    Y2017_Summary = list(np.ravel(results))

    return jsonify(Y2017_Summary)

@app.route("/api/v1.0/[start]/[end]")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    ##Find the min, max and average temps reported starting in Feb 2017
    sel_summary_feb = [func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs)]
    date_str_1 = "2017-01-31"
    date_str_2 = "2017-03-01"

    
    results = session.query(*sel_summary_feb).\
        filter(measurement.date> date_str_1).\
        filter(measurement.date< date_str_2).all()


    session.close()

    Feb2017_Summary = list(np.ravel(results))

    return jsonify(Feb2017_Summary)
    

if __name__ == '__main__':
    app.run(debug=True)
