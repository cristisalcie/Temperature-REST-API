from datetime import datetime

from flask import Flask, request, Response
from flask import json
from flask.json import jsonify

import pymongo

unique_country_id = 1
unique_country_id_available_list = []

unique_city_id = 1
unique_city_id_available_list = []

unique_temp_id = 1
unique_temp_id_available_list = []

app = Flask(__name__)

# global variables for MongoDB host (default port is 27017)
DOMAIN = 'mongodb'
PORT = 27017

# Instantiate a client connection instance
conn = pymongo.MongoClient(
    host = [ str(DOMAIN) + ":" + str(PORT) ],
    serverSelectionTimeoutMS = 3000 # 3 second timeout
)

# Look for database between '' and if it doesn't exist creates it
db_countries = conn['Tari']
db_cities = conn['Orase']
db_temps = conn['Temperaturi']


# Utility functions
def remove_country_from_database(id_country):
    cursor = coll_cities.find({"id_tara": id_country})

    for document in cursor:
        remove_city_from_database(document["id"])

    # Finish deleting the country
    coll_countries.delete_one({"id": id_country})

def remove_city_from_database(id_city):
    cursor = coll_temps.find({"id_oras": id_city})

    for document in cursor:
        remove_temp_from_database(document["id"])

    coll_cities.delete_one({"id": id_city})

def remove_temp_from_database(id_temp):
    coll_temps.delete_one({"id": id_temp})


# Countries
@app.route("/api/countries", methods=["POST"])
def post_countries():
    payload = request.get_json(silent=True)
    
    if (not payload
        or "nume" not in payload
        or "lat" not in payload
        or "lon" not in payload):

        # Error handling
        return Response(status=400)

    
    
    global unique_country_id
    if unique_country_id_available_list: # If list is NOT empty
        id = unique_country_id_available_list.pop()
    else: # List is empty
        id = unique_country_id
        unique_country_id = unique_country_id + 1

    country = {
        "id": id,
        "nume": payload["nume"],
        "lat": payload["lat"],
        "lon": payload["lon"]
    }

    try:
        coll_countries.insert_one(country)
        return jsonify({"id": id}), 201
    except pymongo.errors.DuplicateKeyError:
        return Response(status=409)
    
@app.route("/api/countries", methods=["GET"])
def get_countries():
    result = []
    cursor = coll_countries.find({})
    for document in cursor:
        result.append(
            {
            "id": document["id"],
            "nume": document["nume"],
            "lat": document["lat"],
            "lon": document["lon"]
            }
        )
    return jsonify(result), 200

@app.route("/api/countries/<int:id>", methods=["PUT"])
def post_country(id):
    payload = request.get_json(silent=True)
    if not payload:
        # Error handling
        return Response(status=400)

    if coll_countries.count_documents({"id": id}, limit = 1):
        # Country with id "id" exists
        if "id" in payload:
            if payload["id"] != id:
                # Body id is not param id!
                return Response(status=400)

        # Update info
        if "nume" in payload:
            try:
                coll_countries.update_one(
                    {"id": id}, {"$set": {"nume": payload["nume"]}})
                # Delete cities corresponding to this country
                coll_cities.delete_many({"id_tara": id})
            except pymongo.errors.DuplicateKeyError:
                return Response(status=409)
                

        if "lat" in payload:
            coll_countries.update_one(
                {"id": id}, {"$set": {"lat": payload["lat"]}})

        if "lon" in payload:
            coll_countries.update_one(
                {"id": id}, {"$set": {"lon": payload["lon"]}})

                
        return Response(status=200)
    else:
        # Country with id "id" not found
        return Response(status=404)

@app.route("/api/countries/<int:id>", methods=["DELETE"])
def delete_country(id):
    if coll_countries.count_documents({"id": id}, limit = 1):
        # Country with id "id" exists
        remove_country_from_database(id)
        return Response(status=200)
    else:
        # Country with id "id" not found
        return Response(status=404)

# Cities
@app.route("/api/cities", methods=["POST"])
def post_cities():
    payload = request.get_json(silent=True)
    
    if (not payload
        or "idTara" not in payload
        or "nume" not in payload
        or "lat" not in payload
        or "lon" not in payload):

        # Error handling
        return Response(status=400)

    if not coll_countries.count_documents({"id": payload["idTara"]}, limit = 1):
        # Country with id does not exist
        return Response(status=400)

    
    global unique_city_id
    if unique_city_id_available_list: # If list is NOT empty
        id = unique_city_id_available_list.pop()
    else: # List is empty
        id = unique_city_id
        unique_city_id = unique_city_id + 1

    city = {
        "id": id,
        "id_tara": payload["idTara"],
        "nume_oras": payload["nume"],
        "lat": payload["lat"],
        "lon": payload["lon"]
    }

    try:
        coll_cities.insert_one(city)
        return jsonify({"id": id}), 201
    except pymongo.errors.DuplicateKeyError:
        return Response(status=409)
    
@app.route("/api/cities", methods=["GET"])
def get_cities():
    result = []
    cursor = coll_cities.find({})
    for document in cursor:
        result.append(
            {
            "id": document["id"],
            "idTara": document["id_tara"],
            "nume": document["nume_oras"],
            "lat": document["lat"],
            "lon": document["lon"]
            }
        )
    return jsonify(result), 200

@app.route("/api/cities/country/<int:id_tara>", methods=["GET"])
def get_city(id_tara):
    result = []
    cursor = coll_cities.find({})
    for document in cursor:
        if id_tara == document["id_tara"]:
            result.append(
                {
                "id": document["id"],
                "idTara": document["id_tara"],
                "nume": document["nume_oras"],
                "lat": document["lat"],
                "lon": document["lon"]
                }
            )
    return jsonify(result), 200

@app.route("/api/cities/<int:id>", methods=["PUT"])
def post_city(id):
    payload = request.get_json(silent=True)
    if not payload:
        # Error handling
        return Response(status=400)

    if coll_cities.count_documents({"id": id}, limit = 1):
        # City with id "id" exists
        if "id" in payload:
            if payload["id"] != id:
                # Body id is not param id!
                return Response(status=400)

        # Update info
        if "nume" in payload:
            try:
                coll_cities.update_one(
                    {"id": id}, {"$set": {"nume_oras": payload["nume"]}})
                # Delete all temperatures of this city
                coll_temps.delete_many({"id_oras": id})
            except pymongo.errors.DuplicateKeyError:
                return Response(status=409)
                

        if "idTara" in payload:
            try:
                coll_cities.update_one(
                    {"id": id}, {"$set": {"id_tara": payload["idTara"]}})
            except pymongo.errors.DuplicateKeyError:
                return Response(status=409)

        if "lat" in payload:
            coll_cities.update_one(
                {"id": id}, {"$set": {"lat": payload["lat"]}})

        if "lon" in payload:
            coll_cities.update_one(
                {"id": id}, {"$set": {"lon": payload["lon"]}})

                
        return Response(status=200)
    else:
        # Country with id "id" not found
        return Response(status=404)

@app.route("/api/cities/<int:id>", methods=["DELETE"])
def delete_city(id):
    if coll_countries.count_documents({"id": id}, limit = 1):
        # Country with id "id" exists
        remove_city_from_database(id)
        return Response(status=200)
    else:
        # Country with id "id" not found
        return Response(status=404)



# Temperatures
@app.route("/api/temperatures", methods=["POST"])
def post_temperatures():
    payload = request.get_json(silent=True)
    
    if (not payload
        or "id_oras" not in payload
        or "valoare" not in payload):

        # Error handling
        return Response(status=400)

    if not coll_cities.count_documents({"id": payload["id_oras"]}, limit = 1):
        # City with id does not exist
        return Response(status=400)

    
    global unique_temp_id
    if unique_temp_id_available_list: # If list is NOT empty
        id = unique_temp_id_available_list.pop()
    else: # List is empty
        id = unique_temp_id
        unique_temp_id = unique_temp_id + 1

    timestamp = datetime.datetime.now().timestamp()
    today = datetime.today().strftime('%Y-%m-%d')

    temp = {
        "id": id,
        "valoare": payload["valoare"],
        "timestamp": today + ":" + timestamp,
        "id_oras": payload["id_oras"]
    }

    try:
        coll_temps.insert_one(temp)
        return jsonify({"id": id}), 201
    except pymongo.errors.DuplicateKeyError:
        return Response(status=409)
    
@app.route("/api/temperatures", methods=["GET"])
def get_temperatures():
    lat = request.args.get("lat")
    lon =  request.args.get("lon")
    fromDate = request.args.get("from")
    untilDate = request.args.get("until")
    
    result = []
    cursor = coll_temps.find({})
    
    for document in cursor:
        todayDate = document["timestamp"].split(":")[0]

        
        if lat is not None and document["lat"] != lat:
            continue
        if lon is not None and document["lon"] != lon:
            continue
        if fromDate is not None:
            a = datetime.strptime(todayDate, "%Y-%m-%d")
            b = datetime.strptime(fromDate, "%Y-%m-%d")
            if a < b:
                continue
        if untilDate is not None:
            a = datetime.strptime(todayDate, "%Y-%m-%d")
            b = datetime.strptime(untilDate, "%Y-%m-%d")
            if a > b:
                continue

        result.append(
            {
            "id": document["id"],
            "valoare": document["valoare"],
            "timestamp": todayDate
            }
        )

    return jsonify(result), 200

@app.route("/api/temperatures/cities/<int:id_oras>", methods=["GET"])
def get_temperatures_cities(id_oras):
    fromDate = request.args.get("from")
    untilDate = request.args.get("until")

    result = []
    cursor = coll_temps.find({"id_oras": id_oras})

    for document in cursor:
        todayDate = document["timestamp"].split(":")[0]

        if fromDate is not None:
            a = datetime.strptime(todayDate, "%Y-%m-%d")
            b = datetime.strptime(fromDate, "%Y-%m-%d")
            if a < b:
                continue
        if untilDate is not None:
            a = datetime.strptime(todayDate, "%Y-%m-%d")
            b = datetime.strptime(untilDate, "%Y-%m-%d")
            if a > b:
                continue
        
        result.append(
            {
            "id": document["id"],
            "valoare": document["valoare"],
            "timestamp": todayDate
            }
        )

    return jsonify(result), 200

@app.route("/api/temperatures/countries/<int:id_tara>", methods=["GET"])
def get_temperatures_countries(id_tara):
    fromDate = request.args.get("from")
    untilDate = request.args.get("until")

    result = []
    city_cursor = coll_cities.find({"id_tara": id_tara})

    for city_document in city_cursor:
        temp_cursor = coll_temps.find(
            {
                "id_oras": city_document["id"]
            }
        )
        for temp_document in temp_cursor:
            todayDate = temp_document["timestamp"].split(":")[0]

            if fromDate is not None:
                a = datetime.strptime(todayDate, "%Y-%m-%d")
                b = datetime.strptime(fromDate, "%Y-%m-%d")
                if a < b:
                    continue
            if untilDate is not None:
                a = datetime.strptime(todayDate, "%Y-%m-%d")
                b = datetime.strptime(untilDate, "%Y-%m-%d")
                if a > b:
                    continue

            result.append(
                {
                "id": temp_document["id"],
                "valoare": temp_document["valoare"],
                "timestamp": temp_document["timestamp"].split(":")[0]
                }
            )

    return jsonify(result), 200

@app.route("/api/temperatures/<int:id>", methods=["PUT"])
def post_temperature(id):
    payload = request.get_json(silent=True)
    if not payload:
        # Error handling
        return Response(status=400)

    if coll_temps.count_documents({"id": id}, limit = 1):
        # Temperature with id "id" exists
        if "id" in payload:
            if payload["id"] != id:
                # Body id is not param id!
                return Response(status=400)

        today = datetime.today().strftime('%Y-%m-%d')
        timestamp = datetime.datetime.now().timestamp()
        # Update info
        if "idOras" in payload:
            try:
                coll_temps.update_one(
                    {"id": id}, {"$set": {"id_oras": payload["idOras"],
                    "timestamp": today + ":" + timestamp}})
            except pymongo.errors.DuplicateKeyError:
                return Response(status=409)
                
        if "valoare" in payload:
            coll_cities.update_one(
                {"id": id}, {"$set": {"valoare": payload["valoare"],
                    "timestamp": today + ":" + timestamp}})

                
        return Response(status=200)
    else:
        # Country with id "id" not found
        return Response(status=404)

@app.route("/api/temperatures/<int:id>", methods=["DELETE"])
def delete_temperature(id):
    if coll_temps.count_documents({"id": id}, limit = 1):
        # Country with id "id" exists
        remove_temp_from_database(id)
        return Response(status=200)
    else:
        # Country with id "id" not found
        return Response(status=404)


if __name__ == '__main__':
    # Look for database between '' and if it doesn't exist create it
    db = conn['Tema2_SPRC']


    # Look for collection between '' from database and if it doesn't
    # exist creates it
    coll_countries = db['Tari']

    # If index doesn't exist then it will be created.
    coll_countries.create_index(
        [('id', pymongo.ASCENDING)],
        unique=True)

    # If index doesn't exist then it will be created.
    coll_countries.create_index(
        [('nume', pymongo.ASCENDING)],
        unique=True)




    # Look for collection between '' from database and if it doesn't
    # exist create it
    coll_cities = db['Orase']

    # If index doesn't exist then it will be created.
    coll_cities.create_index(
        [('id', pymongo.ASCENDING)],
        unique=True)
 
    # If index doesn't exist then it will be created.
    coll_cities.create_index(
        [('id_tara', pymongo.ASCENDING),
        ('nume_oras', pymongo.ASCENDING)],
        unique=True)




    # Look for collection between '' from database and if it doesn't
    # exist create it
    coll_temps = db['Temperaturi']

    # If index doesn't exist then it will be created.
    coll_temps.create_index(
        [('id', pymongo.ASCENDING)],
        unique=True)
 
    # If index doesn't exist then it will be created.
    coll_temps.create_index(
        [('id_oras', pymongo.ASCENDING),
        ('timestamp', pymongo.ASCENDING)],
        unique=True)

    # Clean database to prepare for checker
    coll_countries.delete_many({})
    coll_cities.delete_many({})
    coll_temps.delete_many({})
    app.run('0.0.0.0', port=80, debug=False)

