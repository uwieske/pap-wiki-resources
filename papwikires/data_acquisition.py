import argparse
import json
import subprocess
from io import StringIO
from pathlib import Path
import logging

import pandas as pd

logging.basicConfig(format='Date-Time : %(asctime)s : [%(levelname)s] : [%(name)s] : Line No. : %(lineno)d - %(message)s',
                    filename='/data/data_acquisition.log', level=logging.DEBUG)
log = logging.getLogger('data_acquisition')


def _deserialize_to_json(content):
    """
    Given data (content) produced by WikiExtractor script, transform the structure to a JSON object.
    :param content: the geenrated data by WikiExtractor script
    :return: the transformed version as a JSON object
    """
    content_buf = StringIO(content)
    lines = content_buf.readlines()
    concatenated_lines = ",".join(lines)
    json_array_as_str = f'[{concatenated_lines}]'
    return json.loads(json_array_as_str)


def _derive_output_file(fn):
    """
    Given a filename representing the dump file, construct a corresponding filename for the output DataFrame.
    :param fn:
    :return: the name of the pickle file which will contain the DataFrame data
    """
    fn_output = str(Path(fn).stem + '.pickle')
    return Path.joinpath(Path(output_dir).absolute(), Path(fn_output))


def convert_to_pandas(src):
    """
    Convert a dump file of Wikimedia into Pandas DataFrame containing extracted text.
    :param src: the name of the dump file
    :return: the Pandas DataFrame.
    """
    proc_result = subprocess.run(['python', '-m', 'wikiextractor.WikiExtractor',
                                  '-o', '-', '-b', '2M', '--json',
                                  src],
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


if __name__ == '__main__':
    """
    This script wraps the functionality of WikiExtractor which extracts text from a Wikimedia dump file.
    The extracted texts will be stored in a DataFrame which is stored on filesystem as a pickle file.
    The script accepts arguments which are information where the script can locate the dump given and where 
    the converted output file is stored.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_file', help='the dump file containing texts from Wikipedia.', required=True)
    parser.add_argument('--output_dir', help='the output directory where extracted texts wil be saved in.',
                        required=True)
    args = parser.parse_args()
    src_file = args.src_file
    output_dir = args.output_dir
    dest_file = _derive_output_file(src_file)
    log.debug('Program parameters successfully processed.')
    df = convert_to_pandas(src_file)
    log.debug(f'Conversion to Pandas DateFrame succeeded. Writing dataframe to {dest_file}')
    df.to_pickle(dest_file)
    log.debug(f'File {dest_file} successfully written to filesystem.')
