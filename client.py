#!/usr/bin/env python3
"""
RAG MCP Server CLI Client
Interactive command-line interface for testing and managing the RAG MCP server
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import subprocess

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag_server import (
    ingest_document, rag_query, rag_batch_query, 
    extract_tables_from_document, get_document_summary,
    list_indexed_documents, delete_document_index,
    compare_document_to_specification,
    compare_multiple_documents_to_spec,
    generate_compliance_report
)


class RAGClient:
    """CLI client for RAG MCP Server"""
    
    def __init__(self):
        self.verbose = False
    
    def ingest(self, file_path: str, document_name: str = None) -> None:
        """Ingest a document"""
        if not document_name:
            document_name = Path(file_path).stem
        
        print(f"📄 Ingesting {file_path}...")
        result = ingest_document(file_path, document_name)
        
        if result.get("success"):
            print(f"✓ Successfully ingested: {document_name}")
            print(f"  Chunks created: {result['chunks_created']}")
            print(f"  Vector store: {result['vector_store_path']}")
        else:
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
    
    def query(self, document_name: str, query: str, top_k: int = 5) -> None:
        """Query a document"""
        print(f"🔍 Querying {document_name}...")
        print(f"   Question: {query}\n")
        
        result = rag_query(document_name, query, top_k)
        
        if "error" in result:
            print(f"✗ Error: {result['error']}")
            return
        
        results = result.get("results", [])
        print(f"Found {len(results)} relevant results:\n")
        
        for i, res in enumerate(results, 1):
            print(f"[{i}] Score: {res['similarity_score']:.3f}")
            print(f"    Chunk: {res['chunk_id']}")
            print(f"    Content: {res['content']}")
            print()
    
    def batch_query(self, documents: List[str], query: str, top_k: int = 3) -> None:
        """Query multiple documents"""
        print(f"🔍 Querying {len(documents)} documents...")
        print(f"   Question: {query}\n")
        
        result = rag_batch_query(documents, query, top_k)
        
        if "error" in result:
            print(f"✗ Error: {result['error']}")
            return
        
        findings = result.get("findings", {})
        for doc_name, doc_result in findings.items():
            if "error" in doc_result:
                print(f"⚠️  {doc_name}: {doc_result['error']}")
            else:
                num_results = doc_result.get("num_results", 0)
                print(f"✓ {doc_name}: {num_results} results found")
    
    def compare(self, document_name: str, spec_file: str, spec_name: str = "Specification") -> None:
        """Compare document to specification"""
        # Load specification
        try:
            with open(spec_file, 'r') as f:
                content = f.read()
                if spec_file.endswith('.json'):
                    spec = json.loads(content)
                else:
                    # Try as line-separated list
                    spec = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            print(f"✗ Error loading specification: {e}")
            return
        
        print(f"📋 Comparing {document_name} to {spec_name}...")
        result = compare_document_to_specification(
            document_name,
            spec,
            spec_name
        )
        
        if not result.get("success"):
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
            return
        
        print(f"\n✓ Comparison Complete")
        print(f"  Compliance: {result['compliance_percentage']:.1f}%")
        print(f"  Compliant: {result['statistics']['compliant']}")
        print(f"  Partial: {result['statistics']['partial']}")
        print(f"  Non-Compliant: {result['statistics']['non_compliant']}")
        print(f"  Unknown: {result['statistics']['unknown']}")
        print(f"\n{result['summary']}")
    
    def compare_multiple(self, spec_file: str, spec_name: str = "Specification") -> None:
        """Compare all indexed documents to specification"""
        # Get all documents
        docs_result = list_indexed_documents()
        documents = list(docs_result.get("documents", {}).keys())
        
        if not documents:
            print("✗ No documents indexed")
            return
        
        # Load specification
        try:
            with open(spec_file, 'r') as f:
                content = f.read()
                if spec_file.endswith('.json'):
                    spec = json.loads(content)
                else:
                    spec = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            print(f"✗ Error loading specification: {e}")
            return
        
        print(f"📋 Comparing {len(documents)} documents to {spec_name}...")
        result = compare_multiple_documents_to_spec(
            documents,
            spec,
            spec_name
        )
        
        if not result.get("success"):
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
            return
        
        results = result.get("results", {})
        for doc_name, doc_result in sorted(results.items(), 
                                          key=lambda x: x[1]['compliance_percentage'], 
                                          reverse=True):
            compliance = doc_result['compliance_percentage']
            print(f"\n{doc_name}: {compliance:.1f}%")
            stats = doc_result['statistics']
            print(f"  ✓ {stats['compliant']} | ⚠️  {stats['partial']} | ✗ {stats['non_compliant']}")
    
    def report(self, document_name: str, spec_file: str, 
               spec_name: str = "Specification", output_format: str = "text") -> None:
        """Generate compliance report"""
        # Load specification
        try:
            with open(spec_file, 'r') as f:
                content = f.read()
                if spec_file.endswith('.json'):
                    spec = json.loads(content)
                else:
                    spec = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e:
            print(f"✗ Error loading specification: {e}")
            return
        
        print(f"📊 Generating {output_format} report for {document_name}...")
        result = generate_compliance_report(
            document_name,
            spec,
            spec_name,
            output_format
        )
        
        if not result.get("success"):
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
            return
        
        report_text = result.get("report", "")
        
        # Save report
        if output_format == "json":
            ext = ".json"
        elif output_format == "html":
            ext = ".html"
        else:
            ext = ".txt"
        
        output_file = f"{document_name}_compliance_report{ext}"
        with open(output_file, 'w') as f:
            f.write(report_text)
        
        print(f"✓ Report saved to: {output_file}")
        
        if output_format != "json":
            print("\nFirst 50 lines of report:")
            print('\n'.join(report_text.split('\n')[:50]))
    
    def list_documents(self) -> None:
        """List all indexed documents"""
        result = list_indexed_documents()
        documents = result.get("documents", {})
        
        if not documents:
            print("No documents indexed yet")
            return
        
        print(f"\n📚 Indexed Documents ({result['total_documents']}):\n")
        for doc_name, doc_info in documents.items():
            print(f"  {doc_name}")
            print(f"    Type: {doc_info['file_type']}")
            print(f"    Chunks: {doc_info['chunks']}")
            print(f"    Size: {doc_info['content_length']} chars")
            print()
    
    def summary(self, document_name: str) -> None:
        """Get document summary"""
        result = get_document_summary(document_name)
        
        if "error" in result:
            print(f"✗ Error: {result['error']}")
            return
        
        metadata = result.get("metadata", {})
        print(f"\n📋 Document Summary: {document_name}\n")
        
        for key, value in metadata.items():
            if isinstance(value, (list, dict)):
                print(f"  {key}: {json.dumps(value, indent=4)}")
            else:
                print(f"  {key}: {value}")
    
    def delete(self, document_name: str) -> None:
        """Delete document index"""
        result = delete_document_index(document_name)
        
        if result.get("success"):
            print(f"✓ {result['message']}")
        else:
            print(f"✗ Error: {result.get('error', 'Unknown error')}")


def main():
    parser = argparse.ArgumentParser(
        description="RAG MCP Server CLI Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest a PDF
  python client.py ingest /path/to/document.pdf
  
  # Query a document
  python client.py query my_document "What is the main topic?"
  
  # Compare to specification
  python client.py compare my_document spec.txt
  
  # Generate report
  python client.py report my_document spec.txt --format html
  
  # List all documents
  python client.py list
        """
    )
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a document")
    ingest_parser.add_argument("file_path", help="Path to document")
    ingest_parser.add_argument("-n", "--name", help="Document name (default: filename)")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query a document")
    query_parser.add_argument("document", help="Document name")
    query_parser.add_argument("query", help="Query text")
    query_parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of results")
    
    # Batch query command
    batch_parser = subparsers.add_parser("batch", help="Query multiple documents")
    batch_parser.add_argument("documents", nargs="+", help="Document names")
    batch_parser.add_argument("query", help="Query text")
    batch_parser.add_argument("-k", "--top-k", type=int, default=3, help="Results per document")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare to specification")
    compare_parser.add_argument("document", help="Document name")
    compare_parser.add_argument("spec", help="Specification file (JSON or text)")
    compare_parser.add_argument("-n", "--name", default="Specification", help="Specification name")
    
    # Compare multiple command
    compare_all_parser = subparsers.add_parser("compare-all", help="Compare all documents")
    compare_all_parser.add_argument("spec", help="Specification file")
    compare_all_parser.add_argument("-n", "--name", default="Specification", help="Specification name")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate compliance report")
    report_parser.add_argument("document", help="Document name")
    report_parser.add_argument("spec", help="Specification file")
    report_parser.add_argument("-n", "--name", default="Specification", help="Specification name")
    report_parser.add_argument("-f", "--format", choices=["text", "json", "html"], 
                              default="text", help="Report format")
    
    # List command
    subparsers.add_parser("list", help="List indexed documents")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get document summary")
    summary_parser.add_argument("document", help="Document name")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete document index")
    delete_parser.add_argument("document", help="Document name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = RAGClient()
    client.verbose = args.verbose
    
    try:
        if args.command == "ingest":
            client.ingest(args.file_path, args.name)
        elif args.command == "query":
            client.query(args.document, args.query, args.top_k)
        elif args.command == "batch":
            client.batch_query(args.documents[:-1], args.query, args.top_k)
        elif args.command == "compare":
            client.compare(args.document, args.spec, args.name)
        elif args.command == "compare-all":
            client.compare_multiple(args.spec, args.name)
        elif args.command == "report":
            client.report(args.document, args.spec, args.name, args.format)
        elif args.command == "list":
            client.list_documents()
        elif args.command == "summary":
            client.summary(args.document)
        elif args.command == "delete":
            client.delete(args.document)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        if client.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
