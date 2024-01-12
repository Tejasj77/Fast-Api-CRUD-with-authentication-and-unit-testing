# FastAPI + Pydantic + MYSQL REST API Example

Sample API using FastAPI, Pydantic models and settings, and MYSQL as database - non-async.

The API works with a single entity, "Person" (or "People" in plural) that gets stored on a single Mongo database and collection.

The code is intended to create the whole OpenAPI documentation with the maximum detail, including full, detailed models for requests, responses and errors.

## Endpoints

Endpoints define the whole CRUD operations that can be performed on Person entities:

- POST `/users` - create authenticated user
- GET `/users/${user_id}` - get a single person by its unique ID
- POST `/blogs` - create a blog post
- GET `/blogs/{blog_id}` - get a specific blog id
- DELETE `/blogs/{blog_id}` - delete a specific blog id

## Requirements

- Python >= 3.7
- Requirements listed on [requirements.txt](requirements.txt)
- Running MongoDB server

## Infrastructure

- Run docker-compose up to deploy MYSQL and phpmyadmin
