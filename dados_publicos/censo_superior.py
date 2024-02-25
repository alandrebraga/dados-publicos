import requests
import zipfile
import os
import shutil
import argparse
from io import BytesIO


BASE_URL: str = (
    "https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_"
)

data_path = "./data"
extract_path = "./extracted_files"

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

def run(year: str):
    create_dirs()
    download_data_and_unzip(year)
    move_csv_to_data()
    rename_course_file(year)
    rename_university_file(year)
    remove_extracted_dir()


def run_backfill():
    for year in range(2010, 2022 + 1):
        run(year)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and extract INEP data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--year", type=int, help="Year of the data to be downloaded and extracted"
    )
    group.add_argument("--backfill", action="store_true", help="Run backfill for the range of years")
    args = parser.parse_args()

    if args.year:
        run(args.year)
    else:
        run_backfill()