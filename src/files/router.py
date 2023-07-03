import os

from io import BytesIO
from pathlib import Path
from typing import Annotated
from zipfile import ZipFile, ZIP_DEFLATED
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from src.config import logger
from src.utils import TimedRoute

WILDCARD = "*"
DATA_FOLDER = f"{Path(__file__).parent.parent.parent.resolve()}/data"


router = APIRouter(route_class=TimedRoute, tags=["files"])


@router.get("/files")
async def get_files():
    """
    Get a list of relative paths to files.

    Returns:
        dict: A dictionary containing a list of relative paths to files.
    """

    relative_paths = []
    for root, _, files in os.walk(DATA_FOLDER):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), DATA_FOLDER).replace(os.sep, "/")
            relative_paths.append(relative_path)
    return {"files": relative_paths}


@router.post("/files/upload")
async def upload_file(file: UploadFile, upload_path: Annotated[str, "The path where the file should be uploaded"] = ""):
    """
    Upload a file.

    Args:
        file (UploadFile): The file to be uploaded.
        upload_path (str, optional): The path where the file should be uploaded. Defaults to an empty string.

    Returns:
        dict: A dictionary containing a message indicating the result of the file upload.
    """

    if os.path.isfile(upload_path):
        return {"message": f"File {upload_path} already exists"}

    upload_path = os.path.normpath(f"{DATA_FOLDER}/{upload_path}")

    try:
        Path(upload_path).mkdir(parents=True, exist_ok=True)
        file_path = f"{upload_path}/{file.filename}"
        with open(file_path, "wb") as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        logger.error(f"Exception: {e}")
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@router.get("/files/download")
async def download_file(filename: Annotated[str, "The name or path to the file to download"]):
    """
    Download a file.

    Args:
        filename (str): The name or path to the file to download.

    Returns:
        FileResponse or StreamingResponse or dict: The file to download or a message indicating file not found.
    """

    if WILDCARD in filename:
        files = sorted(Path(DATA_FOLDER).rglob(filename))
        if len(files) == 1:
            return FileResponse(path=str(files[0]), media_type="application/octet-stream", filename=files[0].name)
        elif len(files) > 1:
            zip_io = BytesIO()
            with ZipFile(zip_io, mode="w", compression=ZIP_DEFLATED) as zip:
                for file_path in files:
                    zip.write(file_path, Path(file_path).name)

            return StreamingResponse(
                iter([zip_io.getvalue()]),
                media_type="application/x-zip-compressed",
                headers={"Content-Disposition": f"attachment; filename=files.zip"},
            )

    file_path = os.path.normpath(f"{DATA_FOLDER}/{filename}")
    if Path(file_path).is_file():
        return FileResponse(path=file_path, media_type="application/octet-stream", filename=Path(file_path).name)

    return {"message": f"File {filename} not found"}


@router.post("/files/rename")
async def rename_file(
    source_path: Annotated[str, "The path to the file to rename"],
    destination_path: Annotated[str, "The new path for the file"],
):
    """
    Rename a file.

    Args:
        source_path (str): The path to the file to rename.
        destination_path (str): The new path for the file.

    Returns:
        dict: A dictionary containing a message indicating the result of the file renaming.
    """

    source_path = os.path.normpath(f"{DATA_FOLDER}/{source_path}")
    if not os.path.isfile(source_path):
        return {"message": f"File source path does not exist"}

    destination_path = os.path.normpath(f"{DATA_FOLDER}/{destination_path}")
    if os.path.isfile(destination_path):
        return {"message": f"File in destination already exists"}

    dirs, _ = os.path.split(destination_path)

    if dirs:
        Path(dirs).mkdir(parents=True, exist_ok=True)

    Path(source_path).rename(destination_path)

    return {"message": f"File {Path(source_path).name} renamed to {Path(destination_path).name}"}
