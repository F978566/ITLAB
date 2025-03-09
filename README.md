Setup Instructions
1. Clone the Repository
Clone this repository to your local machine:
bash

git clone <repository-url>
cd <repository-directory>

2. Configure Environment Variables
Create a .env file in the root directory with the following content:

# Database configuration
DB_USER=your_postgres_user
<br/>
DB_PASSWORD=your_secure_password
<br/>
DB_NAME=your_database_name
<br/>
DB_HOST=db
<br/>
DB_PORT=5432
<br/>
DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

Replace your_postgres_user, your_secure_password, and your_database_name with your preferred values.

Do not commit the .env file to version control (add it to .gitignore).

3. Build and Run the Application
Run the following command to build the Docker images and start the containers:

```console
docker-compose up --build
```

The --build flag ensures the application image is rebuilt if there are changes.

This command will:
Build the FastAPI app container from the Docker

https://github.com/user-attachments/assets/8e624ee8-d5b1-40d7-ae3b-d3525db238b1

file.

Start a PostgreSQL container.

Run Alembic migrations (alembic upgrade head).

Launch the FastAPI app with Uvicorn on http://localhost:8000.

4. Access the Application
Once the containers are running, access the API at:

http://localhost:8000

You can test the root endpoint (/) or any other endpoints defined in presentation/api/main.py.
5. Stop the Application
To stop the running containers, press Ctrl+C in the terminal where docker-compose up is running, or run:

```console
docker-compose down
```

To also remove the database volume (and lose all data), use:

```console

https://github.com/user-attachments/assets/a5d5c41b-e424-49f2-9e35-774a7232915d


docker-compose down -v
```
Additional Commands
Running Migrations Manually
If you need to run Alembic migrations separately:
Start the database container:

```console
docker-compose up -d db
```

Access the app container:

```console
docker-compose run app bash

https://github.com/user-attachments/assets/f9704a65-5198-48fa-8a0a-e1c040b5c018


```

Inside the container, run:

```console
alembic upgrade head
```

Development Mode
The app runs with Uvicorn's --reload flag enabled for hot reloading during development. Any changes to files in presentation/api/ will automatically restart the server.
Logs
View container logs with:

```console
docker-compose logs
```

Or for a specific service:

```console
docker-compose logs app
docker-compose logs db
```

Troubleshooting
Port Conflicts: If ports 8000 or 5432 are in use, update the ports mappings in docker-compose.yml (e.g., change 8000:8000 to 8080:8000).

Database Connection Issues: Ensure the DATABASE_URL in .env matches the PostgreSQL service configuration.

Missing Dependencies: Add any additional Python packages to requirements.txt and rebuild with docker-compose up --build.

Notes
The application uses PostgreSQL 15 and Python 3.11.

The --reload flag is included for development; remove it from the command in docker-compose.yml for production use.

Persistent database data is stored in a Docker volume named postgres_data.


Uploading 20250309-2034-513454863_jbB7VYjA.mp4…


