from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from models import WorkloadOrm

#DTO - Data Transfer Object
class WorkersAddDTO(BaseModel): #Сначала создаем класс для добавления в него инфы, потом, для вывода (WorkersDTO)
    username: str

class WorkersDTO(WorkersAddDTO): #Класс для выведения информации о работниках 
    id: int 

class ResumesAddDTO(BaseModel):
    title: str 
    compensation: Optional[int]
    workload: WorkloadOrm
    worker_id: int 

class ResumesDTO(ResumesAddDTO):
    id: int 
    created_at: datetime 
    updated_at: datetime

class ResumesRelDTO(ResumesDTO): #Классы relationship для установки отношений между WorkersDTO и ResumesDTO
    worker: "WorkersDTO"

class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]


#Напишем пример использования pydantic моделей в выводе результатов запроса в БД
# with session_factory() as session:
#     query = (
#         select(WorkersOrm)
#         .limit(2)
#     )
#     res = session.execute(query)
#     result = res.scalars().all()
#     print(f"{result}") #Стандартный вывод ответа в формате ORM моделей, которые вручную очень тяжело привести к JSON
#     result_dto = [WorkersDTO.model_validate(row, from_attributes=True) for row in result]
#     print(f"{result_dto = }") #Вывод в вормате pydantic, который уже алхимия сама переведет в JSON

