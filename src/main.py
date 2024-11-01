import logging
from functools import reduce

import pandas as pd
from azure.ai.formrecognizer import DocumentAnalysisClient, DocumentTable
from azure.core.credentials import AzureKeyCredential
from dotenv import dotenv_values

config = dotenv_values(".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def to_pd(document_table: DocumentTable):
    table_data = [
        [
            (
                cell.content
                if (cell.row_index == row and cell.column_index == col)
                else None
            )
            for col in range(document_table.column_count)
        ]
        for row in range(document_table.row_count)
        for cell in document_table.cells
        if cell.row_index == row
    ]
    df = pd.DataFrame(table_data)
    df.columns = df.iloc[0]
    df = df.loc[:, df.columns.notna()]
    return df


def save_and_filter_table(table: DocumentTable):
    df = to_pd(table)
    return df if df.iloc[0, 0] == "From/To Advisor" else None


def main():
    document_analysis_client = DocumentAnalysisClient(
        endpoint=config["ENDPOINT"], credential=AzureKeyCredential(config["KEY"])
    )

    path_to_sample_document = "in/sample.pdf"
    with open(path_to_sample_document, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=f
        )

    result = poller.result()

    list(
        map(
            lambda style: logging.info(
                "Document contains {} content".format(
                    "handwritten" if style.is_handwritten else "no handwritten"
                )
            ),
            result.styles,
        )
    )

    all_tables = list(filter(None, map(save_and_filter_table, result.tables)))

    if all_tables:
        combined_df = reduce(
            lambda x, y: pd.concat([x, y], axis=0, join="inner"), all_tables
        )
        combined_df.reset_index(drop=True, inplace=True)
        combined_df.to_csv("combined_tables.csv", index=False)
        logging.info("All valid tables have been saved to 'combined_tables.csv'.")
    else:
        logging.warning(
            "No valid tables found with the first header value 'From/To Advisor'."
        )


if __name__ == "__main__":
    main()
