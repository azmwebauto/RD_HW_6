from sqlalchemy import insert

from app import models


async def add_cves(session, cves):
    await session.execute(
        insert(models.CveModel),
        cves
    )
