from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import shutil
import os


from backend.router.query_router import handle_request

from backend.document_loader.loader import load_document

from backend.redline.generator import create_redline_doc




# -------------------------
# Create FastAPI App
# -------------------------

app = FastAPI(
    title="LegalContractor API"
)




# -------------------------
# CORS
# -------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:3000"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)





# -------------------------
# Request Schema
# -------------------------

class ChatRequest(BaseModel):

    message: str







# -------------------------
# Health Check
# -------------------------

@app.get("/")
def health_check():


    return {

        "status": "LegalContractor backend running"

    }







# -------------------------
# Normal RAG Chat API
# -------------------------

@app.post("/chat")
def chat(

    request: ChatRequest

):


    response = handle_request(


        user_query=request.message


    )



    return {


        "answer": response


    }









# -------------------------
# Agentic Contract Review API
# File + Optional Query
# -------------------------

@app.post("/review")
async def review_contract(


    file: UploadFile = File(...),


    query: str = Form(

        "Review this contract"

    )


):




    # create temp folder

    os.makedirs(

        "temp",

        exist_ok=True

    )





    file_path = (

        "temp/"

        +

        file.filename

    )





    # save uploaded file temporarily

    with open(

        file_path,

        "wb"

    ) as buffer:



        shutil.copyfileobj(


            file.file,


            buffer


        )







    # Extract document text

    document_text = load_document(


        file_path


    )








    # Run Agentic RAG
    # query can be:
    #
    # "Review this contract"
    # OR
    # "Find only GDPR risks"
    # OR
    # "Check termination clauses"


    result = handle_request(


        user_query=query,


        document_text=document_text


    )









    # Dynamic redline filename


    original_name = (

        file.filename

        .split(".")[0]

    )




    output_name = (

        original_name

        +

        "_redlined.docx"

    )








    # Generate DOCX


    redline_file = create_redline_doc(


        result["suggested_rewrites"],


        output_name


    )








    return {


        "review": result,


        "redline_file": redline_file


    }









# -------------------------
# Download Redlined Contract
# -------------------------

@app.get("/download/{filename}")
def download_redline(


    filename: str


):


    return FileResponse(


        filename,


        filename=filename,


        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"


    )