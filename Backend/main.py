import ast
# from json import dumps
import json
from fastapi import FastAPI, Form, Query, Request
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import uvicorn
from pymongo.errors import ConnectionFailure, OperationFailure

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
# db = client["testdb"]  # Replace with your database name
# collection = db["collection_name"]

# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.post("/execute_query")
# async def execute_query(request: Request):
#     print("............................entered execute query#########################")    
#     try:
#         form_data = await request.form()
#         query = form_data["query"]
#         print("mmmmmmmmmmmmmmmmmmmmmmmm", query)
#         try:
#             collection = db["mycollection"]
#             document = {"query": query}
#             collection.insert_one(document)
#             print("query sent")
#             return {"query": query}
#         except Exception as e:
#             print("aaaaaaaaaaaaaaaaaaaaaaa",e)
#     except Exception as e:
#         print("bbbbbbbbbbbbbbbbb",e)
#
# @app.post("/execute_query")
# def execute_query(query: str = Form(...), request: Request):
#     result = execute_mongo_query(query)
#     return templates.TemplateResponse("index.html", {"request": request, "result": result})


# def execute_mongo_query(query):
#     try:
#         exec(f"result = {query}")
#         return result
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.post("/execute_query")
# def execute_query(request: Request):
#     query = request.form["query"]
#     result = execute_mongo_query(query)
#     return templates.TemplateResponse("index.html", {"request": request, "result": result})


# def execute_mongo_query(query):
#     # Execute your MongoDB query here and return the result
#     result = db.command(query)
#     return result


# @app.post("/execute_query")
# async def execute_query(request: Request,query: str = Form(...)):
#    result = execute_mongo_query(query)
#    return templates.TemplateResponse("index.html", {"request": request, "result": result})

# def execute_mongo_query(query):
#     try:
#         result = db.command(query)
#         return result
#     except Exception as e:
#         return f"Error: {str(e)}"

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("mongo.html", {"request": request})

@app.post("/connect_db")
async def connect_db(request: Request, uri: str = Form(...)):

    try:
        # mongo = request.form["mongo_uri"]
        # mongo_db=mongo.json()
        # conn = MongoClient(Query)
        # uri = request.form['uri']
        conn = MongoClient(uri)
        # db = conn.akshy

        # Check the connection
        conn.admin.command('ping')
        # return "Connection successful"
        databases = conn.list_database_names()

        # Get the collections for each database
        collections = {}
        for database in databases:
            collections[database] = conn[database].list_collection_names()

        return templates.TemplateResponse("result.html", {"request": request, "databases": databases, "collections": collections})

    except ConnectionFailure as e:
        return f"Failed to connect to MongoDB: {repr(e)}"
    except Exception as e:
        return f"An error occurred: {repr(e)}"
        # # Check if the database exists
        # if db.list_collection_names():
        #     print("Database Connected...")
        # else:
        #     print("Database does not exist.")



@app.post("/execute_query")
async def execute_query(request: Request, collection: str = Form(...), query: str = Form(...),databases:  str = Form(...), collections: str = Form(...)):
    # Perform operations with the query and collection
    # You can execute the query against the specified collection here

    # Example: Log the query and collection
    print("Executing query:", query)
    print("Collection:", collection)

    # You can perform further actions with the query and selected collection,
    # such as executing the query against the database or returning the results.

    return templates.TemplateResponse("result.html", {"request": request, "databases": databases, "collections": collections})

# @app.post("/execute_query")
# async def execute_query(request: Request, mongo_uri: str = Form(...), query: str = Form(...)):
#     try:
#         client = MongoClient(mongo_uri)
#         db = client.get_database()
#         result = list(db.command(query))
#         return templates.TemplateResponse("result.html", {"request": request, "result": result})
#     except Exception as e:
#         return templates.TemplateResponse("query.html", {"request": request, "error": str(e)})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
