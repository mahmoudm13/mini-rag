from celery import Celery
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

settings = get_settings()

async def get_setup_utils():
    settings = get_settings()
    
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    
    db_engine = create_async_engine(url=postgres_conn)
    
    db_client = async_sessionmaker(
        bind=db_engine, 
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    llm_provider_factory = LLMProviderFactory(settings)
    vector_db_provider_factory = VectorDBProviderFactory(config=settings, db_client=db_client)
    
    # generation client
    generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND,
    )
    generation_client.set_generation_model(
        model_id = settings.GENERATION_MODEL_ID,
    )
    
    # embedding client
    embedding_client = llm_provider_factory.create(
        provider=settings.EMBEDDING_BACKEND,
    )
    embedding_client.set_embedding_model(
        model_id = settings.EMBEDDING_MODEL_ID,
        embedding_size = settings.EMBEDDING_SIZE,
    )
    
    # vector db client
    vector_db_client = vector_db_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND,
    )
    await vector_db_client.connect()
    
    template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )

    return (db_engine, db_client, llm_provider_factory, vector_db_provider_factory,
            generation_client, embedding_client, vector_db_client, template_parser)

# create celery application instance
celery_app = Celery(
    "minirag",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "tasks.file_processing",
        "tasks.data_indexing",
    ],
)

# configure celery with essential settings
celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=[
        settings.CELERY_TASK_SERIALIZER
    ],
    
    # task safety - late acknowledgment prevents task loss or worker crash
    task_acks_late=settings.CELERY_TASK_ACKS_LATE,
    
    # time limit - prevent hanging tasks
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    
    # result backend - store results for status tracking
    task_ignore_resul=False,
    result_expires=3600,
    
    # worker settings
    worker_concurrency=settings.CELERY_WORKER_CONCURRENY,
    
    # connection settings for better reliability
    broker_connection_retry_on_startup=True,
    broker_connection_safety=True,
    broker_connection_max_retries=10,
    worker_cancel_long_running_tasks_on_connection_loss=True,
    
    task_routes={
        "tasks.file_processing.process_project_files": {"queue": "file_processing"},
        "tasks.data_indexing.index_data_content": {"queue": "data_indexing"},
    }
)

celery_app.conf.task_default_queue = "default"
