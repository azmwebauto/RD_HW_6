import argparse
import asyncio
import logging
import os
import time
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncEngine

from app import database, crud, serializers

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def save_to_db(engine: AsyncEngine, results: Generator[dict]):
    async with database.make_session(engine) as session:
        try:
            await crud.add_cves(session, results)
            await session.commit()
        except Exception as e:
            logging.error(e)
            await session.rollback()


async def main(filepath: str, max_open_file_limit: int = 1000):
    logging.info(filepath)
    engine = database.create_engine()

    files = tuple(os.path.join(root, file) for root, dirs, files in os.walk(filepath) for file in files if
              file.endswith(".json") and 'delta' not in file)
    saving_tasks = [
        asyncio.create_task(
            save_to_db(
                engine,
                filter(
                    lambda file: file is not None,
                    (
                        serializers.serialize_cve_record(file)
                        for file in await asyncio.gather(
                        *tuple(serializers.parse_json(file) for file in batched_files)
                    )
                    )
                )
            )
        )
        for batched_files in serializers.batcher(files, batch_size=max_open_file_limit)
    ]
    await asyncio.gather(*saving_tasks)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-max', '--max_open_file_limit',
                        type=int, default=1000, help='Maximum number of open files')
    return parser.parse_args()


if __name__ == '__main__':
    start = time.perf_counter()
    args = get_args()
    asyncio.run(main(args.file, args.max_open_file_limit))
    end = time.perf_counter()
    logging.info(f'Finished in {end - start:.2f} seconds')
