import os
import logging
import json

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

def crack_invoice(invoice: bytes) -> dict:
    # create a doc intelligence client
    # https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python-preview

    """
    This code sample shows Prebuilt Invoice operations with the Azure Form Recognizer client library. 
    The async versions of the samples require Python 3.6 or later.

    To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
    https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
    """
    endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENT_INTELLIGENCE_KEY"]

    document_intelligence_client  = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
        
    poller = document_intelligence_client.begin_analyze_document("prebuilt-invoice", analyze_request=invoice, content_type="application/octet-stream")
    invoice_data: AnalyzeResult = poller.result()

    # TODO: validation and error handling
    if invoice_data.documents:
        return invoice_data.as_dict().get("documents")[0].get("fields")
    
    return {}