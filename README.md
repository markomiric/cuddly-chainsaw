# Files API

Section 1: Setup

**1\. Install a Virtual Environment:**
To begin, we need to create a virtual environment for our project. Open your terminal and navigate to the project root directory. Execute the following command to set up the virtual environment, assuming you have python 3 installed:

```
python -m venv venv
```

**2\. Activate the Virtual Environment:**
Once the virtual environment is created, activate it using the command below (could be different depending on the OS):

```
source venv/Scripts/activate
```

**3\. Install Required Development Packages:**
Now, let's install the necessary development packages by running the following command:

```
pip install -r requirements.txt
```

**4\. Run the App: To launch the Files API, enter the following command:**

```
python -m uvicorn src.main:app --reload --workers 1 --host 127.0.0.1 --port 8000
```

**5\. Go the the API:**
The api swagger docs should be running on http://127.0.0.1:8000/docs

**6\. Retrieve stored files' relative paths:**

To retrieve the relative paths of all stored files, you can use the following `curl` command:

rust

```rust
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/files' \
  -H 'accept: application/json'
```

You should receive a response body like this:

json

```json
{
  "files": [".gitkeep"]
}
```

**7\. Upload files:**

To upload a file, you can use the following `curl` command:

bash

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/files/upload?upload_path=test_folder' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.png;type=image/png'
```

You will receive a response like this:

json

```json
{
  "message": "Successfully uploaded image.png"
}
```

You can also upload to a nested folder, such as "test_folder/nested_test_folder", using the following `curl` command:

bash

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/files/upload?upload_path=test_folder/nested_test_folder' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.png;type=image/png'
```

You will receive a similar response confirming the successful upload.

**8\. Download files:**

To download a file, you can use the following `curl` command:

bash

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/files/download?filename=test_folder/image.png' \
  -H 'accept: application/json'
```

You can also use wildcards to download multiple files. For example, to download all PNG files within the "test_folder":

bash

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/files/download?filename=test_folder/*.png' \
  -H 'accept: application/json'
```

If you have multiple files with a similar name, you can use wildcards to download them. For instance, to download all files containing "image" in their name:

bash

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/files/download?filename=*image*' \
  -H 'accept: application/json'
```

**Renaming and moving files:**

To rename and move a file to a different directory, you can use the following `curl` command:

bash

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/files/rename?source_path=test_folder/image.png&destination_path=other_folder/image_copy.png' \
  -H 'accept: application/json'
```

You will receive a response like this:

json

```json
{
  "message": "File image.png renamed to image_copy.png"
}
```

Make sure to replace the paths and filenames accordingly in the `curl` commands to match your specific use case.

Please note that these examples assume you are running the API locally at `http://127.0.0.1:8000`.
