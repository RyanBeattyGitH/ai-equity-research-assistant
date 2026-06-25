from app.services.ingest import ingest_document

sample_text = """
Nvidia reported strong AI demand growth.
The company expects continued expansion in data center revenue.
Management highlighted GPU shortages and supply chain risks.
"""

ingest_document(sample_text)
