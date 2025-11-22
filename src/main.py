from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.mongo_conn = AsyncIOMotorClient( settings.MONGODB_URL )
    app.state.db_client = app.state.mongo_conn[settings.MONGODB_DATABASE]
    
    llm_provider_factory = LLMProviderFactory(settings)
    vector_db_provider_factory = VectorDBProviderFactory(settings)
    
    # generation client
    app.state.generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND,
    )
    app.state.generation_client.set_generation_model(
        model_id = settings.GENERATION_MODEL_ID,
    )
    
    # embedding client
    app.state.embedding_client = llm_provider_factory.create(
        provider=settings.EMBEDDING_BACKEND,
    )
    app.state.embedding_client.set_embedding_model(
        model_id = settings.EMBEDDING_MODEL_ID,
        embedding_size = settings.EMBEDDING_SIZE,
    )
    
    # vector db client
    app.state.vector_db_client = vector_db_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND,
    )
    app.state.vector_db_client.connect()
    
    app.state.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )
    
    yield
    
    app.state.mongo_conn.close()
    app.state.vector_db_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
