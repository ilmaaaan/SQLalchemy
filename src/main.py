import os
import sys
import asyncio


sys.path.insert(1, os.path.join(sys.path[0], ".."))

from queries.orm import SyncOrm, AsyncOrm
from queries.core import SyncCore, AsyncCore


SyncOrm.create_tables()
SyncOrm.insert_data()
SyncOrm.select_workers()
SyncOrm.update_workers()
SyncOrm.insert_additional_resumes()
SyncOrm.join_cte_subquery_window_func()
SyncOrm.select_workers_with_lazy_relationship()
SyncOrm.select_workers_with_joined_relationship()
SyncOrm.select_workers_with_selectin_relationship()
SyncOrm.select_workers_with_condition_relationship()
SyncOrm.select_workers_with_condition_relationship_contains_eager()
SyncOrm.add_vacancies_and_replies()
SyncOrm.select_resumes_with_all_relationships()

# SyncOrm.insert_resumes()
# SyncOrm.select_resumes_avg_compensation()

# SyncCore.create_tables()
# SyncCore.insert_workers()
# SyncCore.select_workers()
# SyncCore.update_workers()

# asyncio.run(insert_data())

