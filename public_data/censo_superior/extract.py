import requests
import zipfile
import os
import shutil
from io import BytesIO
from google.cloud import storage, bigquery
import argparse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets.json'

BASE_URL: str = (
    "https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_"
)

data_path = "dados_publicos/censo_superior/data"
extract_path = "dados_publicos/censo_superior/extracted_files"

def create_dirs():
    os.makedirs(extract_path, exist_ok=True)
    os.makedirs(data_path, exist_ok=True)


def remove_extracted_dir():
    shutil.rmtree(extract_path)


def download_data_and_unzip(year: int):
    url = f"{BASE_URL}{year}.zip"
    filebytes = BytesIO(requests.get(url, verify=False).content)
    zipfile.ZipFile(filebytes).extractall(extract_path)


def move_csv_to_data():
    for dirpath, _, files in os.walk(extract_path):
        for file in files:
            if file.endswith(".CSV"):
                shutil.move(f"{dirpath}/{file}", data_path)



def rename_course_file(year: int):
    for dirpath, _, files in os.walk(data_path):
        for file in files:
            if f"CURSOS_{str(year)}" in file:
                os.replace(f"{dirpath}/{file}", f"{dirpath}/cursos_{year}.csv")


def rename_university_file(year: int):
    for dirpath, _, files in os.walk(data_path):
        for file in files:
            if f"IES_{str(year)}" in file:
                os.replace(f"{dirpath}/{file}", f"{dirpath}/ies_{year}.csv")

def extract(year: str):
    create_dirs()
    download_data_and_unzip(year)
    move_csv_to_data()
    rename_course_file(year)
    rename_university_file(year)
    remove_extracted_dir()
    load_to_cloud_storage()


def load_to_cloud_storage():
    files = os.listdir(data_path)
    client = storage.Client()
    bucket = client.get_bucket("dl_educacao-superior-415319")
    for file in files:
        blob = bucket.blob(f"microdados_censo_superior/{file}")
        blob.upload_from_filename(f"{data_path}/{file}")

def table_exists(client, table_id):
    try:
        client.get_table(table_id)
        return True
    except:
        return False

def load_to_bigquery():
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True, field_delimiter=";"
    )
    uri_pattern = "dl_educacao-superior-415319"
    storage_client = storage.Client()
    bucket = storage_client.bucket(uri_pattern)
    blobs = bucket.list_blobs()

    for blob in blobs:
        formated_name = blob.name.split('/')[1][0:-4]
        table_name = f"raw_dados_publicos.{formated_name}"

        if not table_exists(client, table_name):
            uri = f"gs://dl_educacao-superior-415319/{blob.name}"
            load_job = client.load_table_from_uri(uri, table_name,job_config=job_config)
            load_job.result()
            print(f"Job finished for {blob.name}")
        else:
            print(f"Table {table_name} already exists")


def run_backfill():
    for year in range(2010, 2022 + 1):
        extract(year)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and extract INEP data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--year", type=int, help="Year of the data to be downloaded and extracted"
    )
    group.add_argument("--backfill", action="store_true", help="Run backfill for the range of years")
    args = parser.parse_args()

    if args.year:
        extract(args.year)
    else:
        run_backfill()

    load_to_bigquery()