import pickle
from functools import reduce

import pandas as pd
from azure.ai.formrecognizer import AnalyzeResult, DocumentTable
from dotenv import dotenv_values

from ._ import fnames, logger

config = dotenv_values(".env")


def _to_pd(document_table: DocumentTable):

    table_data = [
        [None for _ in range(document_table.column_count)]
        for _ in range(document_table.row_count)
    ]

    for cell in document_table.cells:
        table_data[cell.row_index][cell.column_index] = cell.content

    df = pd.DataFrame(table_data)

    df.columns = df.iloc[0]
    df = df.drop(index=df.index[0])

    return df


def etl(pkl_fname: str, output_fname: str, table_target: str):
    with open(f"cache/{pkl_fname}", "rb") as file:
        result: AnalyzeResult = pickle.load(file)

    all_tables = []

    for table_idx, table in enumerate(result.tables):
        df = _to_pd(table)
        if df.iloc[0, 0] == table_target:
            all_tables.append(df)

    if all_tables:
        combined_df = reduce(
            lambda x, y: pd.concat([x, y], axis=0, join="inner"), all_tables
        )
        combined_df.to_csv(f"out/{output_fname}", index=False)
        logger.info(f"All valid tables have been saved to 'out/{output_fname}'.")
    else:
        logger.warning(
            f"No valid tables found with the first header value '{table_target}'."
        )


def main():
    names = fnames(config["INPUT"])
    etl(
        pkl_fname=names["pkl_fname"],
        output_fname=names["output_fname"],
        table_target="From/To Advisor",
    )


if __name__ == "__main__":
    main()
