from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from .schemes.data import ProcessRequest
from models import ResponseSignal, AssetTypeEnums, ProjectModel, ChunkModel, AssetModel
from models.db_schemes import DataChunk, Asset
from controllers import NLPController
from tasks.file_processing import process_project_files
import aiofiles
import logging
import os

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: int, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.state.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    
    # validate file properties
    data_controller = DataController()
    
    is_valid, result_signal = data_controller.validate_uploaded_file(file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )
    
    # Generate unique filename for the uploaded file
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunck := await file.read(app_settings.FILE_DEFAULT_CHUNCK_SIZE):
                await f.write(chunck)
    except Exception as e:
        
        logger.error(f"Error while uploading file: {e}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )
    
    # store the assets into the database
    asset_model = await AssetModel.create_instance(
        db_client=request.app.state.db_client
    )
    
    asset_resource = Asset(
        asset_project_id=project.project_id,
        asset_type=AssetTypeEnums.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    
    asset_record = await asset_model.create_asset(asset_resource)
    
    return JSONResponse(
        content={
            "signal": result_signal,
            "file_id": str(asset_record.asset_id),
        }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: int, process_request: ProcessRequest):
    
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    task = process_project_files.delay(
        project_id=project_id,
        file_id=process_request.file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size,
        do_reset=do_reset,
    )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "task_id": task.id,
        }
    )
