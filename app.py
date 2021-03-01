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

    

