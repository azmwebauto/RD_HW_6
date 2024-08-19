from datetime import datetime
from typing import Iterable

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


def __parse_datetime(datetime_str):
    for fmt in (
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S'
    ):
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{datetime_str}' does not match any known format.")


def serialize_cve_record(record: dict) -> dict | None:
    cve_id = record.get('cveMetadata', {}).get('cveId', None)
    published_date_str = record.get('cveMetadata', {}).get('datePublished', None)
    last_modified_date_str = record.get('cveMetadata', {}).get('dateUpdated', None)

    published_date = __parse_datetime(published_date_str) if published_date_str else None
    last_modified_date = __parse_datetime(last_modified_date_str) if last_modified_date_str else None

    if cve_id is None or published_date is None or last_modified_date is None:
        return None

    cna = record.get('containers', {}).get('cna', {})
    title = cna.get('descriptions', [{}])[0].get('value')
    description = cna.get('descriptions', [{}])[0].get('value')
    problem_types = ", ".join(
        [
            pt.get('descriptions', [{}])[0].get('description', '')
            for pt in cna.get('problemTypes', [])
        ]
    ) if cna.get('problemTypes') else None

    cve_record = dict(
        cve_id=cve_id,
        published_date=published_date,
        last_modified_date=last_modified_date,
        title=title,
        description=description,
        problem_types=problem_types,
        raw_info=record
    )
    return cve_record


async def save_cve_to_db(session: AsyncSession, data_list: Iterable[dict]):
    await session.execute(
        insert(models.CveModel),
        [
            serialized_record
            for serialized_record in (serialize_cve_record(data) for data in data_list)
            if serialized_record is not None
        ]
    )
