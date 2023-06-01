# Import some necessary modules
# pip install kafka-python
# pip install pymongo
# pip install "pymongo[srv]"
from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json




# replace here with your mongodb url 
uri = "mongodb+srv://jairh3110:gitachi131@cluster0.gdfwizt.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))xd
# Send a ping to confirm a successful connection

#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# Connect to MongoDB and pizza_data database

try:
    print("entro a linea 30")
    print("entro a la segunda linea")
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.devices
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

consumer = KafkaConsumer('test',bootstrap_servers=[
     'my-kafkaf-0.my-kafkaf-headless.jairh3110.svc.cluster.local:9092'
    ])
# Parse received data from Kafka
for msg in consumer:
    record = json.loads(msg.value)
    print(record)
    message= record['message']
    usuarioid= record['usuarioid']

    # Create dictionary and ingest data into MongoDB
    try:
       meme_rec = {'message':message,'usuarioid':usuarioid }
       print (meme_rec)
       meme_id = db.publicacionmessage.insert_one(meme_rec)
       print("Data inserted with record ids", meme_id)

       #subprocess.call(['sh', './test.sh'])

    except:
       print("Could not insert into MongoDB")




    try:
       agg_result= db.devices.aggregate(
       [{
         "$group" : 
         {  "_id" : "$message", 
            "n"    : {"$sum": 1}
         }}
       ])
       db.devices_summarymessage.delete_many({})
       for i in agg_result:
         print(i)
         summary_id = db.devices_summarymessage.insert_one(i)
         print("Summary inserted with record ids", summary_id)

    except Exception as e:
       print(f'group by caught {type(e)}: ')
       print(e)
    