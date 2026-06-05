#!/bin/bash

echo "Starting LegalContractor backend setup"


# -------------------------------
# Conda setup
# -------------------------------

source "$(conda info --base)/etc/profile.d/conda.sh"


if conda env list | grep -q "legal-rag"; then

    echo "Conda environment legal-rag already exists"

else

    echo "Creating conda environment legal-rag"

    conda create -n legal-rag python=3.11 -y

fi



echo "Activating environment"

conda activate legal-rag





# -------------------------------
# Install Python dependencies
# -------------------------------


echo "Installing requirements"

pip install --upgrade pip

pip install -r requirements.txt






# -------------------------------
# Check / create Qdrant DB
# -------------------------------


echo "Checking Qdrant database"


if [ -d "qdrant_db" ] && [ -f "qdrant_db/meta.json" ]; then


    echo "Qdrant database already exists"

    echo "Knowledge base ready"



else


    echo "Qdrant database missing"

    echo "Building knowledge base"




    echo "Extracting CUAD data"

    python -m backend.ingestion.extract_cuad




    echo "Creating chunks"

    python -m backend.ingestion.chunker




    echo "Creating Qdrant vector database"

    python -m backend.vector_store.qdrant_store



fi





echo "Backend setup complete"


echo ""

echo "Run backend using:"

echo "conda activate legal-rag"

echo "uvicorn backend.api.main:app --reload"