import json
from datetime import datetime
from itertools import islice

import aiofiles.os

TIME_FORMATS = (
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S'
)


def batcher(iterable, batch_size):
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch


async def parse_json(file_path):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        data = await f.read()
        return json.loads(data)


def __parse_datetime(datetime_str):
    for fmt in TIME_FORMATS:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{datetime_str}' does not match any known format.")


def serialize_cve_record(record: dict) -> dict | None:
    if not record:
        return None
    cve_id = record.get('cveMetadata', {}).get('cveId', None)
    published_date_str = record.get('cveMetadata', {}).get('datePublished', None)
    last_modified_date_str = record.get('cveMetadata', {}).get('dateUpdated', None)

    published_date = __parse_datetime(published_date_str) if published_date_str else None
    last_modified_date = __parse_datetime(last_modified_date_str) if last_modified_date_str else None

    if cve_id is None or published_date is None or last_modified_date is None:
        return None

    cna = record.get('containers', {}).get('cna', {})

    return dict(
        cve_id=cve_id,
        published_date=published_date,
        last_modified_date=last_modified_date,
        title=cna.get('descriptions', [{}])[0].get('value'),
        description=cna.get('descriptions', [{}])[0].get('value'),
        problem_types=", ".join(
            [
                pt.get('descriptions', [{}])[0].get('description', '')
                for pt in cna.get('problemTypes', [])
            ]
        ) if cna.get('problemTypes') else None,
        raw_info=record
    )
