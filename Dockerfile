FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=America/Sao_Paulo \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Set working directory
WORKDIR /app

# Copy installation files
COPY data/install/get-pip.py /app/
COPY data/install/requeriments_base.txt /app/
COPY data/install/requeriments_torch.txt /app/
COPY data/install/requeriments_ultralytics.txt /app/

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    libopenblas-dev \
    default-libmysqlclient-dev \
    libmysqlclient-dev \
    pkg-config \
    wget \
    curl \
    git \
    ca-certificates \
    gnupg \
    gpg-agent \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.11 manually without using PPA
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 python3.11-dev python3.11-distutils python3.11-venv \
    || { \
        # If direct install fails, try using the PPA
        apt-get install -y --no-install-recommends gpg-agent && \
        apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 && \
        add-apt-repository ppa:deadsnakes/ppa -y && \
        apt-get update && \
        apt-get install -y python3.11 python3.11-dev python3.11-distutils python3.11-venv; \
    } && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for SSL
ENV LDFLAGS="-L/usr/local/opt/openssl/lib" \
    CPPFLAGS="-I/usr/local/opt/openssl/include"

# Install pip and Python dependencies
RUN python3.11 get-pip.py && \
    pip3.11 install --upgrade pip && \
    pip3.11 install --upgrade setuptools setuptools-scm wheel && \
    pip3.11 install cmake

# Create a modified requirements file without dlib

# Install dlib directly from pip

# Create a modified requirements file without dlib
RUN grep -v "dlib" requeriments_base.txt > requeriments_base_nodlib.txt

# Install dlib with necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cmake \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-python-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3.11 install dlib==19.24.2 --no-cache-dir

# Install other requirements
RUN pip3.11 install -r requeriments_base_nodlib.txt --no-cache-dir && \
    pip3.11 install -r requeriments_torch.txt --no-cache-dir && \
    pip3.11 install -r requeriments_ultralytics.txt --no-cache-dir

# Copy the rest of the application
COPY . /app/

# Create a non-root user to run the application
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Command to run when the container starts
CMD ["python3.11", "manage.py", "runserver", "0.0.0.0:8000"]
