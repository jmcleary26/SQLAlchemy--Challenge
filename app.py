import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

# Create our session (link) from Python to the DB
# session = Session(engine)

@app.route("/")
def welcome():
    return (
        f'Welcome to the Precipitation/Station Analysis API!'
        f'Available Routes:'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
   session = Session(engine)

   results = session.query(Measurement.date, Measurement.prcp).all()

   session.close()

   query_precip = []
   for date, prcp in results:
       precipitation_dict = {}
       precipitation_dict["date"] = date
       precipitation_dict["prcp"] = prcp
       query_precip.append(precipitation_dict)

    return jsonify(query_precip) 


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    results = session.query(Station.name)

    session.close()

    stationslist = []
    for station in results:
        station_dict = {}
        station_dict["Name"] = name
        stationslist.append(station_dict)

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
mostactivestation = 'USC00519281'

def tobs():
    session = Session(engine)

    latestdatestr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latestdatedt = dt.datetime.strptime(latestdatestr[0], '%Y-%m-%d')
    querydate = dt.date(latestdatedt.year -1, latestdatedt.month, latestdatedt.day)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= querydate).filter(Measurement.station == mostactivestation).all()

    session.close()

    tobslist = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobslist.append(tobs_dict)

    return jsonify(tobslist)

@app.route('/api/v1.0/<start>')
def startdate(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.ax(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    tobsstart = []
    for min, max, avg in results:
        tobsstartdict = {}
        tobsstartdict["Min"] = min
        tobsstartdict["Max"] = max
        tobsstartdict["Average"] = avg
        tobsstart.append(tobsstartdict)

    return jsonify(tobsstart)

@app.route('/api/v1.0/<start>/<end>')
def startenddate(start,stop):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.ax(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= stop).all()

    session.close()

    tobsstartend = []
    for min, max, avg in results:
        tobsstartend_dict = {}
        tobsstartend_dict["Min"] = min
        tobsstartend_dict["Max"] = max
        tobsstartend_dict["Average"] = avg
        tobsstartend.append(tobsstartend_dict)

    return jsonify(tobsstartend)






    



