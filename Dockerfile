# Set base image (host OS)  
FROM pytorch/pytorch:2.1.1-cuda12.1-cudnn8-devel

ENV PATH=/usr/local/cuda/:${PATH} 
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH  

# Update system packages and install build dependencies
RUN apt-get update && \      
    apt-get upgrade -y && \    
    apt-get install -y git build-essential g++ && \    
    apt-get clean    

RUN pip install packaging wheel

# Install unsloth training framework
RUN pip install --upgrade --force-reinstall --no-cache-dir torch==2.1.1 triton  \
    --index-url https://download.pytorch.org/whl/cu121
COPY . .
COPY ./requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt
# Cleanup step  
RUN apt-get remove -y git build-essential && \  
    apt-get autoremove -y && \  
    apt-get clean && \  
    rm -rf /var/lib/apt/lists/*

# Application setup
WORKDIR /app
# COPY api ./api
EXPOSE 9090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090", "--reload"]  
