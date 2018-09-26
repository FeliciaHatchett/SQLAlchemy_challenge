import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# engine = create_engine("path", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

year_date=dt.date(2017, 8, 23) - dt.timedelta(days=365)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temperature observations from the last year."""
    year_rain=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>year_date).all()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_rain = []
    for measurement in year_rain:
        rain_dict = {}
        rain_dict["date"] = measurement.date
        rain_dict["prcp"] = measurement.prcp

        all_rain.append(rain_dict)

    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    station_list=session.query(Station.station).all()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    temp=session.query(Measurement.tobs).filter(Measurement.date>year_date).all()
    
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def temp_by_dates(start):
    """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    sel=[func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)]
    
    temp_info=session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()

    return jsonify(temp_info)

@app.route("/api/v1.0/<start>/<end>")
def temp_by_range(start, end):
    """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    sel=[func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)]
    
    temp_range=session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date)>=start).filter(func.strftime("%Y-%m-%d", Measurement.date)<=end).all()

    return jsonify(temp_range)


if __name__ == '__main__':
    app.run(debug=True)