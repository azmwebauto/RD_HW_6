import argparse
import asyncio
import json
import logging
import os

import aiofiles.os

from app import database, crud


async def parse_json(semaphore, file_path):
    async with semaphore:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return json.loads(await f.read())


async def main(filepath: str, max_open_file_limit: int = 1000):
    logging.info(filepath)
    semaphore = asyncio.Semaphore(max_open_file_limit)

    results = tuple(
        asyncio.create_task(parse_json(semaphore, os.path.join(root, file)))

        for root, dirs, files in os.walk(filepath)
            for file in files
                if file.endswith(".json") and 'delta' not in file
    )
    logging.info(f'reading {len(results)=}')
    results = await asyncio.gather(*results)

    logging.info(f'inserting {len(results)=}')
    async with database.make_session(database.create_engine()) as session:
        try:
            await crud.save_cve_to_db(session, results)
            await session.commit()
        except Exception as e:
            logging.exception(e)
            await session.rollback()
    logging.info('Finished!')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-f', '--max_open_file_limit',
                        type=int, default=1000, help='Maximum number of open files')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    asyncio.run(main(args.file, args.max_open_file_limit))
