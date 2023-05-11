import argparse
import json
import os
import subprocess
from io import StringIO
from pathlib import Path
import logging
from typing import Any

import pandas as pd

logging.basicConfig(
    format='Date-Time : %(asctime)s : [%(levelname)s] : [%(name)s] : Line No. : %(lineno)d - %(message)s',
    filename='/data/data_acquisition.log', level=logging.DEBUG)
log = logging.getLogger('data_acquisition')


def _deserialize_to_json(content: str) -> Any:
    """
    Given data (content) produced by WikiExtractor script, transform the structure to a JSON object
    :param content: the generated data by WikiExtractor script
    :return: the transformed version as a JSON object
    """
    content_buf = StringIO(content)
    lines = content_buf.readlines()
    concatenated_lines = ",".join(lines)
    json_array_as_str = f'[{concatenated_lines}]'
    return json.loads(json_array_as_str)


def _derive_output_file(fn: str, dest_dir: str) -> Path:
    """
    Given a filename representing the dump file, construct a corresponding filename for the output DataFrame
    :param fn: the pickle filename of the destination data frame
    :param output_dir: the destination directory of the data frame
    :return: the name of the pickle file which will contain the DataFrame data
    """
    fn_output = str(Path(fn).stem + '.pickle')
    return Path.joinpath(Path(dest_dir).absolute(), Path(fn_output))


def _execute_extraction_to_pandas(src_file: str) -> pd.DataFrame:
    """
    Convert a dump file of Wikimedia into Pandas DataFrame containing extracted text
    :param src_file: the name of the dump file
    :return: the Pandas DataFrame.
    """
    proc_result = subprocess.run(['python', '-m', 'wikiextractor.WikiExtractor',
                                  '-o', '-', '-b', '2M', '--json',
                                  src_file],
                                 check=False,
                                 stdout=subprocess.PIPE,
                                 text=True)
    if proc_result.returncode != 0:
        print(proc_result.stderr)
        print(f'Captured STDOUT subprocess(WikiExtractor): {proc_result.stdout}')
        log.error(f'Return code: {proc_result.returncode}')
        log.error(proc_result.stderr)
        log.warning(f'STDOUT of subprocess(WikiExtractor): {proc_result.stdout}')
        raise SystemExit(1)
    json_data = _deserialize_to_json(proc_result.stdout)
    return pd.DataFrame.from_records(json_data)


def _extract_text_and_save(source: str, dest_dir: str) -> None:
    """
    Extract texts from the dump file and save the texts as a pickle DataFrame file
    :param source: the name of dump file
    :param dest_dir: the destination directory where the pickle DataFrame file will be saved in
    """
    dest_fn = _derive_output_file(source, dest_dir)
    df_converted = _execute_extraction_to_pandas(source)
    log.debug(f'Conversion to Pandas DateFrame succeeded. Writing dataframe to {dest_fn}')
    df_converted.to_pickle(dest_fn)
    log.debug(f'File {dest_fn} successfully written to filesystem.')


def extract_texts_to_pandas(source: str, dest_dir: str) -> None:
    """
    This function takes a src which can be the name of the dump file itself or the directory name containing one or
    multiple dump files. For each dump file extract texts from the dump file and save the texts as a pickle DataFrame
    file
    :param source: the source path which is the filename itself or the directory containing one or more dump file
    :param dest_dir: destination directory where data frame is saved
    """

    if Path(source).is_dir():
        # convert all files in dir
        for root, _, files in os.walk(source):
            print(len(files))
            for f in files:
                if Path(f).suffix == '.bz2':
                    full_file_path = str(Path.joinpath(Path(root), Path(f)))
                    _extract_text_and_save(full_file_path, dest_dir)
    else:
        # convert single file
        _extract_text_and_save(source, dest_dir)


if __name__ == '__main__':
    """
    This script wraps the functionality of WikiExtractor which extracts text from a Wikimedia dump file.
    The extracted texts will be stored in a DataFrame which is stored on filesystem as a pickle file.
    The script accepts arguments which are information where the script can locate the dump given and where 
    the converted output file is stored.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help='the dump file or the directory containing dump files containing texts from '
                                      'Wikipedia.', required=True )
    parser.add_argument('--output_dir', help='the output directory where extracted texts wil be saved in.',
                        required=True )
    args = parser.parse_args()
    src = args.src
    output_dir = args.output_dir
    log.debug('Program parameters successfully processed.')
    extract_texts_to_pandas(src, output_dir)
    log.debug('Script data_acquisition ended.')
