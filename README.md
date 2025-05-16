# EM_test_project

A FastAPI project for testing and verification.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Unix or MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Start the application with:
```
uvicorn main:app --reload
```

Or run the main.py file directly:
```
python main.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the automatic API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
