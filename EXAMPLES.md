"""
RAG MCP Server - Usage Examples
Demonstrates all major features and workflows
"""

# ==============================================================================
# EXAMPLE 1: Basic Document Ingestion and Query
# ==============================================================================

from src.rag_server import ingest_document, rag_query

# Ingest a PDF document
result = ingest_document(
    file_path="/path/to/document.pdf",
    document_name="my_document"
)

print(f"Ingestion result: {result}")
# Output:
# {
#     "success": True,
#     "document_name": "my_document",
#     "file_type": "pdf",
#     "chunks_created": 45,
#     ...
# }

# Query the ingested document
query_result = rag_query(
    document_name="my_document",
    query="What are the main points discussed?",
    top_k=5
)

print(f"Found {query_result['num_results']} relevant results")
for result in query_result['results']:
    print(f"- Score: {result['similarity_score']:.3f}")
    print(f"  Content: {result['content'][:100]}...")


# ==============================================================================
# EXAMPLE 2: Multi-Document Query
# ==============================================================================

from src.rag_server import rag_batch_query

# Query multiple documents at once
batch_result = rag_batch_query(
    document_names=["doc1", "doc2", "doc3"],
    query="What is the budget allocation?",
    top_k=3
)

# Results are organized by document
for doc_name, findings in batch_result['findings'].items():
    if 'results' in findings:
        print(f"\n{doc_name}: {findings['num_results']} results found")


# ==============================================================================
# EXAMPLE 3: Simple Compliance Check
# ==============================================================================

from src.rag_server import compare_document_to_specification

# Define requirements as a simple list
specifications = [
    "Document must include executive summary",
    "Must contain financial projections",
    "Must list risk factors",
    "Must include management team details"
]

# Run comparison
compliance_result = compare_document_to_specification(
    document_name="business_plan",
    specifications=specifications,
    spec_name="Business Plan Requirements"
)

print(f"\nCompliance Score: {compliance_result['compliance_percentage']:.1f}%")
print(f"Compliant: {compliance_result['statistics']['compliant']}")
print(f"Partial: {compliance_result['statistics']['partial']}")
print(f"Non-Compliant: {compliance_result['statistics']['non_compliant']}")


# ==============================================================================
# EXAMPLE 4: Complex Specification Check
# ==============================================================================

import json

# Load specification from JSON file
with open('examples/sample_specification.json', 'r') as f:
    spec_data = json.load(f)

# Extract requirements list
specifications = [req['text'] for req in spec_data['requirements']]

# Compare with higher threshold for strict compliance
compliance_result = compare_document_to_specification(
    document_name="technical_proposal",
    specifications=specifications,
    spec_name="Technical Requirements",
    threshold=0.8  # Stricter matching
)

# Review non-compliant items
if compliance_result['success']:
    non_compliant = [
        item for item in compliance_result['items']
        if item['status'] == 'non-compliant'
    ]
    
    if non_compliant:
        print("⚠️  Non-Compliant Items:")
        for item in non_compliant:
            print(f"- {item['requirement_id']}: {item['requirement_text']}")


# ==============================================================================
# EXAMPLE 5: Multi-Document Comparison (Vendor Proposals)
# ==============================================================================

from src.rag_server import compare_multiple_documents_to_spec

# Vendor proposals already indexed as: vendor_a, vendor_b, vendor_c
vendor_names = ["vendor_a", "vendor_b", "vendor_c"]

# RFP requirements
rfp_specs = [
    "Deliver project within 6 months",
    "Total cost not to exceed $500,000",
    "Provide 24/7 support",
    "Quarterly reporting required",
    "Must maintain 99.9% uptime SLA"
]

# Compare all vendors
comparison_results = compare_multiple_documents_to_spec(
    document_names=vendor_names,
    specifications=rfp_specs,
    spec_name="RFP Requirements"
)

# Rank vendors by compliance score
ranked = sorted(
    comparison_results['results'].items(),
    key=lambda x: x[1]['compliance_percentage'],
    reverse=True
)

print("\n📊 Vendor Ranking:")
for rank, (vendor, result) in enumerate(ranked, 1):
    compliance = result['compliance_percentage']
    print(f"{rank}. {vendor}: {compliance:.1f}% compliant")


# ==============================================================================
# EXAMPLE 6: Generate Compliance Reports
# ==============================================================================

from src.rag_server import generate_compliance_report

# Generate different report formats
for format in ["text", "json", "html"]:
    report_result = generate_compliance_report(
        document_name="contract",
        specifications=["Clause 1", "Clause 2", "Clause 3"],
        spec_name="Legal Requirements",
        format=format
    )
    
    if report_result['success']:
        # Save report
        filename = f"contract_compliance_report.{format if format != 'text' else 'txt'}"
        with open(filename, 'w') as f:
            f.write(report_result['report'])
        print(f"✓ Saved {format} report to {filename}")


# ==============================================================================
# EXAMPLE 7: Table and Image Extraction
# ==============================================================================

from src.rag_server import extract_tables_from_document, extract_images_from_document

# Extract tables
tables_result = extract_tables_from_document("financial_report")
if tables_result['total_tables'] > 0:
    print(f"\nFound {tables_result['total_tables']} tables")
    for table in tables_result['tables']:
        print(f"- {table['sheet']}: {len(table['data'])} rows")

# Extract images/OCR data
images_result = extract_images_from_document("scanned_document")
if images_result['ocr_available']:
    print("✓ OCR data available for this document")


# ==============================================================================
# EXAMPLE 8: Document Summary and Metadata
# ==============================================================================

from src.rag_server import get_document_summary, list_indexed_documents

# Get summary for specific document
summary = get_document_summary("my_document")
print(f"\nDocument Summary: {summary['document_name']}")
print(f"File Type: {summary['metadata']['file_type']}")
print(f"Chunks: {summary['vector_store_chunks']}")

# List all indexed documents
all_docs = list_indexed_documents()
print(f"\nTotal Indexed Documents: {all_docs['total_documents']}")
for doc_name, doc_info in all_docs['documents'].items():
    print(f"- {doc_name}: {doc_info['chunks']} chunks")


# ==============================================================================
# EXAMPLE 9: Using with Claude Desktop
# ==============================================================================

"""
To use with Claude Desktop:

1. Add to claude_desktop_config.json:
{
  "mcpServers": {
    "rag-server": {
      "command": "python",
      "args": ["C:\\path\\to\\pdf_rag_mcp_server\\src\\rag_server.py"]
    }
  }
}

2. In Claude, you can:
   - Say: "Analyze this proposal document"
   - Claude ingests it using ingest_document
   - Ask: "What are the payment terms?"
   - Claude queries using rag_query
   - Request: "Compare this to our requirements"
   - Claude uses compare_document_to_specification
   - Get: "Generate compliance report"
   - Claude creates report using generate_compliance_report

Example Claude conversation:
---
User: I have several vendor proposals. Can you help me compare them?
Claude: I'll help you analyze and compare the vendor proposals. 
- First, ingest the proposals into the system
- Compare them against your RFP requirements
- Generate a compliance matrix
- Provide a recommendation based on compliance scores

(Claude uses the MCP tools behind the scenes)
---
"""


# ==============================================================================
# EXAMPLE 10: Workflow - RFP Response Evaluation
# ==============================================================================

def evaluate_rfp_responses(rfp_file, proposal_files):
    """Complete workflow for evaluating RFP responses"""
    
    import os
    
    # Step 1: Load RFP requirements
    with open(rfp_file, 'r') as f:
        rfp_specs = [line.strip() for line in f if line.strip()]
    
    # Step 2: Ingest all proposals
    vendor_names = []
    for proposal_file in proposal_files:
        doc_name = os.path.splitext(os.path.basename(proposal_file))[0]
        vendor_names.append(doc_name)
        
        print(f"Ingesting {doc_name}...")
        result = ingest_document(proposal_file, doc_name)
        if not result.get('success'):
            print(f"  Error: {result.get('error')}")
            continue
        print(f"  ✓ {result['chunks_created']} chunks created")
    
    # Step 3: Compare all proposals to RFP
    print(f"\nComparing {len(vendor_names)} proposals to RFP...")
    comparison = compare_multiple_documents_to_spec(
        document_names=vendor_names,
        specifications=rfp_specs,
        spec_name="RFP Requirements"
    )
    
    # Step 4: Generate individual reports
    print("\nGenerating compliance reports...")
    for vendor in vendor_names:
        generate_compliance_report(
            document_name=vendor,
            specifications=rfp_specs,
            spec_name="RFP Requirements",
            format="html"
        )
        print(f"  ✓ Report generated: {vendor}_compliance_report.html")
    
    # Step 5: Rank and summarize
    print("\n" + "="*50)
    print("EVALUATION SUMMARY")
    print("="*50)
    
    ranked = sorted(
        comparison['results'].items(),
        key=lambda x: x[1]['compliance_percentage'],
        reverse=True
    )
    
    for rank, (vendor, result) in enumerate(ranked, 1):
        compliance = result['compliance_percentage']
        status = "✓" if compliance >= 85 else "⚠" if compliance >= 70 else "✗"
        print(f"{status} {rank}. {vendor}: {compliance:.1f}%")


# Usage
if __name__ == "__main__":
    # Uncomment to run the complete workflow:
    # evaluate_rfp_responses(
    #     'requirements.txt',
    #     ['vendor_a_proposal.pdf', 'vendor_b_proposal.pdf']
    # )
    pass
