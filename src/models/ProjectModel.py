from .db_schemes import Project
from .BaseDataModel import BaseDataModel
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import async_sessionmaker

class ProjectModel(BaseDataModel):
    
    def __init__(self, db_client: async_sessionmaker):
        super().__init__(db_client=db_client)
    
    @classmethod
    async def create_instance(cls, db_client: async_sessionmaker):
        instance = cls(db_client)
        return instance
    
    async def create_project(self, project: Project):
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)

        return project
    
    async def get_project_or_create_one(self, project_id: str):
        
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(select(Project).where(Project.project_id == project_id))
                project = result.scalar_one_or_none()
                if project is None:
                    project_rec = Project(
                        project_id=project_id,
                    )
                    project = await self.create_project(project_rec)
                
                return project
        
    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        async with self.db_client() as session:
            async with session.begin():
                total_documents = await session.execute(select(
                    func.count(Project.project_id)
                ))                
                
                total_documents = total_documents.scalar_one()
                
                total_pages = total_documents // page_size
                if total_documents % total_pages != 0:
                    total_pages += 1
                
                query = select(Project).offset((page - 1) * page_size).limit(page_size)
                projects = await session.execute(query).scalars().all()
                
                return projects, total_pages
