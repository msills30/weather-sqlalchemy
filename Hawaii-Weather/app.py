# Import the dependencies.

import numpy as np
import datetime as dt
import scipy.stats as st


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, request,jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    
    """The precipitation between 08/23/2016 - 08/23/2017"""
    wther = [Measurement.date,Measurement.prcp]
    results = session.query(*wther).\
    filter(Measurement.date > '2016-08-22').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    
    session.close()

     # Convert the query results into a list of dictionaries
    precipitation_data = []
    for date, prcp in results:
        data = {
            "date": date,
            "precipitation": prcp
        }
        precipitation_data.append(data)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def station():
    unique_list = session.query(Measurement.station).\
                  group_by(Measurement.station).\
                  order_by(Measurement.station).all()

    session.close()
    # Convert the query results into a list of dictionaries
    
    station_title = []
    for station in unique_list:
        stat = {
            "station": station[0]   
        }
        station_title.append(stat)

    return jsonify(station_title)


@app.route("/api/v1.0/tobs")
def tobs():
    statt = [Measurement.date,Measurement.tobs]
    station_temp = session.query(*statt).\
        filter(Measurement.date >= '2016-08-18').\
        filter(Measurement.station == 'USC00519281').\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    # Convert the query results into a list of dictionaries
    temp_data = []
    for date, tobs in station_temp:
        tdata = {
            "date": date,
            "temperature": tobs
        }
        temp_data.append(tdata)

    return jsonify(temp_data)

## Thank you Mothanna battah helping me solve this portion
@app.route("/api/v1.0/<start>")
def start(start):

    data = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    results = session.query(*data).\
        filter(Measurement.date >= start).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)


    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

    data = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    results = session.query(*data).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)


    
if __name__ == '__main__':
    app.run(debug=True)
