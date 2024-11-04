import pickle

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import dotenv_values

config = dotenv_values(".env")

from ._ import fnames, logger


def model(
    endpoint: str,
    key: str,
    input_fname: str,
    pkl_fname: str,
):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    path_to_input_document = f"in/{input_fname}"
    with open(path_to_input_document, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=f
        )

    result = poller.result()

    # Save the analysis result to a file
    with open(f"cache/{pkl_fname}", "wb") as file:
        pickle.dump(result, file)

    logger.info(f"Document analysis results have been saved to '{pkl_fname}'.")


def main():
    names = fnames(config["INPUT"])
    model(
        endpoint=config["ENDPOINT"],
        key=config["KEY"],
        input_fname=names["input_fname"],
        pkl_fname=names["pkl_fname"],
    )


if __name__ == "__main__":
    main()
