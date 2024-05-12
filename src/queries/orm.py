from sqlalchemy import text, insert, select, inspect, func, cast, Integer, and_
from database  import sync_engine, async_engine, session_factory, async_session_factory
from models import workers_table, WorkersOrm, Base, ResumesOrm, WorkloadOrm, VacanciesOrm, VacanciesRepliesOrm
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager


class SyncOrm:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with session_factory() as session:
            worker_bobr = WorkersOrm(username= "Bobr")
            worker_volk = WorkersOrm(username = "Volk")
            session.add_all([worker_bobr, worker_volk])
            session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            # worker_id = 1 
            # worker_jack = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f'{workers = }')


    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_misha = session.get(WorkersOrm, worker_id)
            worker_misha.username = new_username
            session.refresh(worker_misha)
            session.commit()
    
    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title = "Python Junior Developer", compensation = 50000, workload = WorkloadOrm.fulltime, worker_id = 1
            )
            resume_jack_2 = ResumesOrm(
                title = "Python Разработчик", compensation = 150000, workload = WorkloadOrm.fulltime, worker_id = 1
            )
            resume_michael_1 = ResumesOrm(
                title = "Python Data Engineer", compensation = 250000, workload = WorkloadOrm.parttime, worker_id = 2
            )
            resume_michael_2 = ResumesOrm(
                title = "Data Scientist", compensation = 300000, workload = WorkloadOrm.fulltime, worker_id = 2
            )
            session.add_all([resume_jack_1, resume_jack_2, resume_michael_1, resume_michael_2])
            session.flush()
            session.commit()
            sync_engine.echo = True
        
    @staticmethod 
    def select_resumes_avg_compensation(like_languages: str= "Python"):
        with session_factory() as session: 
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    ) 
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_languages), 
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer)> 70000)
            )
            print(query)
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)
    
    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod 
    def join_cte_subquery_window_func(like_language: str = "Python"):
        with session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq =(
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by = r.workload).cast(Integer).label("avg_workload_compensation"),
                )
                # .select_from(r)
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = (
                select(
                    subq.c.worker_id, 
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation-subq.c.avg_workload_compensation).label("compensation_diff"),
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )
            res = session.execute(query)
            result = res.all()

            print(f'{result = }')

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session: 
            query = (
                select(WorkersOrm)
            )
            res = session.execute(query)
            result = res.scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)
    
    @staticmethod
    def select_workers_with_joined_relationship():
        with session_factory() as session: 
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_selectin_relationship():
        with session_factory() as session: 
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)
        
    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes_parttime)) #Объединение таблиц ONEtoMANY (selectinload)
            )
            res = session.execute(query)
            result = res.scalars().all() #scalars() возвращает объект ScalarResult с первым значением каждой строки результата
            print(result)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .join(WorkersOrm.resumes)
                .options(contains_eager(WorkersOrm.resumes)) #contains_eager() говорит алхимии, что мы уже подгрузили через join() какие-то 
                .filter(ResumesOrm.workload == "parttime")
                .limit(2) #Мы хотим забрать только 2 резюме
            )
            res = session.execute(query)
            result = res.unique().scalars().all() #unique() выводит только уникальные значения из таблицы
            print(result)

    @staticmethod
    def add_vacancies_and_replies():
        with session_factory() as session:
            new_vacancy = VacanciesOrm(title = "Python разработчик", compensation = 100000)
            resume_1 = session.get(ResumesOrm, 1)
            resume_2 = session.get(ResumesOrm, 2)
            resume_1.vacancies_replied.append(new_vacancy)
            resume_2.vacancies_replied.append(new_vacancy)
            session.commit()
    
    @staticmethod
    def select_resumes_with_all_relationships():
        with session_factory() as session: 
            query = (
                select(ResumesOrm)
                .options(joinedload(ResumesOrm.worker))
                .options(selectinload(ResumesOrm.vacancies_replied).load_only(VacanciesOrm.title))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(f"{result = }")






class AsyncOrm:
    @staticmethod
    async def insert_data():
        async with async_session_factory() as session:
            worker_bobr = WorkersOrm(username= "Bobr")
            worker_volk = WorkersOrm(username = "Volk")
            session.add_all([worker_bobr, worker_volk])
            await session.commit()

   

