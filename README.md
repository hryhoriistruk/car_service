# Car Service API

FastAPI-based application for managing a car service using an API and a Telegram bot.

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [License](#license)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.11+
- FastAPI
- Docker
- Docker Compose

### Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/.../car_service.git
cd car_service
pip install -r requirements.txt
```

Copy the .env-example file:

```bash
cp .env-example .env
```

Edit the .env file with your configuration details.

Set up your PostgreSQL database using Docker Compose:

```bash
docker-compose up -d
```

### Usage

Run the FastAPI application:

```bash
uvicorn src.main:app --reload
```

### Applying Migrations

Apply Alembic migrations to set up the database schema:

```bash
alembic upgrade head
```

### API Endpoints

- Swagger Documentation: http://localhost:8000/docs
- Redoc Documentation: http://localhost:8000/redoc

### Configuration

Configure the application by updating the settings in .env. Make sure to set up your database connection and other
relevant options.

### License

This project is licensed under the MIT License.