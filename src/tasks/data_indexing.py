from celery_app import celery_app, get_setup_utils
from models import ProjectModel, ChunkModel, ResponseSignal
from helpers.config import get_settings
from controllers import NLPController
from tqdm.auto import tqdm
import asyncio
import logging

logger = logging.getLogger("celery.task")

@celery_app.task(bind=True, name="tasks.data_indexing.index_data_content",
                 autoretry_for=(Exception,),
                 retry_kwargs={"max_retries": 3, "countdown": 60})
def index_data_content(self, project_id: int, do_reset: bool):
    
    return asyncio.run(
        _index_data_content(self, project_id, do_reset)
    )

async def _index_data_content(task_instance, project_id: int, do_reset: bool):
    
    db_engine, vector_db_client = None, None
    
    try:
        (db_engine, db_client, llm_provider_factory, vector_db_provider_factory,
        generation_client, embedding_client, vector_db_client, template_parser) = await get_setup_utils()

        logger.warning("Setup utils were loaded!")

        project_model = await ProjectModel.create_instance(
            db_client=db_client,
        )
        
        chunk_model = await ChunkModel.create_instance(
            db_client=db_client,
        )
        
        project = await project_model.get_project_or_create_one(
            project_id=project_id,
        )
        
        if not project:
            task_instance.update_state(
                state="FAILURE",
                meta={
                    "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value,
                }
            )
            
            raise Exception(f"No project found for project_id: {project_id}")
        
        nlp_controller = NLPController(
            vector_db_client=vector_db_client,
            generation_client=generation_client,
            embedding_client=embedding_client,
            template_parser=template_parser,
        )
        
        has_records = True
        page_no = 1
        inserted_items_counts = 0
        idx = 0
        
        # create collection if not existed
        collection_name = nlp_controller.create_collection_name(project_id=project.project_id)
        
        _ = await vector_db_client.create_collection(
            collection_name=collection_name, 
            embedding_size=embedding_client.embedding_size, 
            do_reset=do_reset,
        )
        
        # setup batching
        total_chunks_count = await chunk_model.get_total_chunks_count(project_id=project.project_id)
        pbar = tqdm(total=total_chunks_count, desc="Vector Indexing", position=0)
        
        while has_records:
            page_chunks = await chunk_model.get_project_chunks(
                project_id=project.project_id,
                page_no=page_no,
            )

            if not page_chunks or len(page_chunks) == 0:
                has_records = False
                break
            
            chunks_ids = [ c.chunk_id for c in page_chunks ]
            idx += len(page_chunks)
            
            is_inserted = await nlp_controller.index_into_vector_db(
                project=project,
                chunks=page_chunks,
                chunks_ids=chunks_ids,
            )
            
            if not is_inserted:
                task_instance.update(
                    state="FAILURE",
                    meta={
                        "signal": ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value,
                    }
                )
                
                raise Exception(f"Can not insert into vectorDB | project_id: {project_id}")
            
            page_no += 1
            pbar.update(len(page_chunks))
            inserted_items_counts += len(page_chunks)
        
        task_instance.update_state(
            state="SUCCESS",
            meta={
                "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
            }
        )
        
        return {
            "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
            "inserted_items_count": inserted_items_counts,
        }
        
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
    finally:
        try:
            if db_engine:
                await db_engine.dispose()
            
            if vector_db_client:
                await vector_db_client.disconnect()
        except Exception as e:
            logger.error(f"Task failed while cleaning: {str(e)}")
