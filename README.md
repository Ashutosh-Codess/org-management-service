# Org Management Service (FastAPI + MongoDB)

## Overview
This backend implements a multi-tenant architecture using FastAPI and MongoDB.  
Each organization gets its own collection (org_<organization_name>).  
A Master Database stores global metadata and admin user details.

## Features
- Create organization
- Get organization details
- Update organization (rename + sync)
- Delete organization
- Admin login (JWT authentication)
- Password hashing (Argon2)

## Local Setup
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload

## Environment Variables
MONGO_URI=<your mongodb uri>
JWT_SECRET=<your jwt secret>

## Deployment (Render)
- Add environment variables in Render dashboard  
- Start command: ash start.sh

## Endpoints
POST /org/create  
GET /org/get  
PUT /org/update  
DELETE /org/delete  
POST /admin/login  

