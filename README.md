# Files API

Section 1: Setup

1.  Install a Virtual Environment: To begin, we need to create a virtual environment for our project. Open your terminal and navigate to the project root directory. Execute the following command to set up the virtual environment, assuming you have python 3 installed:

```
python -m venv venv
```

2.  Activate the Virtual Environment: Once the virtual environment is created, activate it using the command below (could be different depending on the OS):

```
source venv/Scripts/activate
```

3.  Install Required Development Packages: Now, let's install the necessary development packages by running the following command:

```
pip install -r requirements.txt
```

4.  Run the App: To launch the Files API, enter the following command:

```
python -m uvicorn src.main:app --reload --workers 1 --host 127.0.0.1 --port 8000
```

5. Go the the API: The api swagger docs should be running on http://127.0.0.1:8000/docs
