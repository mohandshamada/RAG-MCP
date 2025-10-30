"""
Comparison Engine for RAG MCP Server
Compares documents against specifications and generates detailed reports
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status enumeration"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non-compliant"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


@dataclass
class ComplianceItem:
    """Single compliance item"""
    requirement_id: str
    requirement_text: str
    expected_value: Optional[str]
    found_value: Optional[str]
    status: ComplianceStatus
    evidence: List[str]
    notes: str = ""


@dataclass
class ComparisonResult:
    """Result of document comparison"""
    document_name: str
    spec_name: str
    comparison_timestamp: str
    total_requirements: int
    compliant_items: int
    partial_items: int
    non_compliant_items: int
    unknown_items: int
    compliance_percentage: float
    items: List[ComplianceItem]
    summary: str


class SpecificationParser:
    """Parse specifications from various formats"""
    
    @staticmethod
    def parse_json_spec(spec_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse JSON specification format"""
        requirements = []
        
        if isinstance(spec_data, dict):
            if "requirements" in spec_data:
                requirements = spec_data["requirements"]
            else:
                # Try to flatten the dict as requirements
                for key, value in spec_data.items():
                    requirements.append({
                        "id": key,
                        "text": str(value),
                        "expected": None
                    })
        
        return requirements
    
    @staticmethod
    def parse_list_spec(spec_list: List[str]) -> List[Dict[str, Any]]:
        """Parse list of specification strings"""
        requirements = []
        
        for idx, item in enumerate(spec_list):
            requirements.append({
                "id": f"REQ_{idx + 1:03d}",
                "text": item,
                "expected": None
            })
        
        return requirements


class ComparisonEngine:
    """Main comparison engine for RAG-based document comparison"""
    
    def __init__(self, rag_query_func):
        """
        Initialize comparison engine
        
        Args:
            rag_query_func: Function to perform RAG queries
        """
        self.rag_query_func = rag_query_func
        self.logger = logging.getLogger(__name__)
    
    def compare_document_to_spec(
        self,
        document_name: str,
        specifications: List[str] | Dict[str, Any],
        spec_name: str = "Specification",
        threshold: float = 0.7
    ) -> ComparisonResult:
        """
        Compare document against specifications using RAG
        
        Args:
            document_name: Name of indexed document
            specifications: List of spec strings or dict of specs
            spec_name: Name of specification
            threshold: Similarity threshold (0-1)
            
        Returns:
            ComparisonResult with compliance details
        """
        self.logger.info(f"Comparing {document_name} against {spec_name}")
        
        # Parse specifications
        if isinstance(specifications, list):
            requirements = SpecificationParser.parse_list_spec(specifications)
        else:
            requirements = SpecificationParser.parse_json_spec(specifications)
        
        if not requirements:
            self.logger.warning("No requirements found in specification")
            requirements = []
        
        compliance_items = []
        
        # Query RAG for each requirement
        for req in requirements:
            item = self._check_requirement(
                document_name,
                req,
                threshold
            )
            compliance_items.append(item)
        
        # Calculate statistics
        result = self._calculate_compliance_stats(
            document_name,
            spec_name,
            compliance_items
        )
        
        return result
    
    def _check_requirement(
        self,
        document_name: str,
        requirement: Dict[str, Any],
        threshold: float
    ) -> ComplianceItem:
        """Check single requirement against document"""
        
        req_id = requirement.get("id", "UNKNOWN")
        req_text = requirement.get("text", "")
        expected_value = requirement.get("expected", None)
        
        try:
            # Query document for this requirement
            rag_result = self.rag_query_func(
                document_name,
                req_text,
                top_k=5
            )
            
            if "error" in rag_result:
                status = ComplianceStatus.UNKNOWN
                found_value = None
                evidence = []
            else:
                results = rag_result.get("results", [])
                
                if not results:
                    status = ComplianceStatus.NON_COMPLIANT
                    found_value = None
                    evidence = []
                else:
                    # Check if best result meets threshold
                    best_score = float(results[0].get("similarity_score", 0))
                    
                    if best_score >= threshold:
                        status = ComplianceStatus.COMPLIANT
                        found_value = results[0].get("content", "Found")
                    elif best_score >= (threshold * 0.7):  # Partial match
                        status = ComplianceStatus.PARTIAL
                        found_value = results[0].get("content", "Partially found")
                    else:
                        status = ComplianceStatus.NON_COMPLIANT
                        found_value = results[0].get("content", "Not found")
                    
                    evidence = [
                        f"{r.get('content', '')[:100]}... (Score: {r.get('similarity_score', 0):.2f})"
                        for r in results[:3]
                    ]
            
            return ComplianceItem(
                requirement_id=req_id,
                requirement_text=req_text,
                expected_value=expected_value,
                found_value=found_value,
                status=status,
                evidence=evidence,
                notes=""
            )
        
        except Exception as e:
            self.logger.error(f"Error checking requirement {req_id}: {e}")
            return ComplianceItem(
                requirement_id=req_id,
                requirement_text=req_text,
                expected_value=expected_value,
                found_value=None,
                status=ComplianceStatus.UNKNOWN,
                evidence=[str(e)],
                notes=f"Error: {str(e)}"
            )
    
    def _calculate_compliance_stats(
        self,
        document_name: str,
        spec_name: str,
        items: List[ComplianceItem]
    ) -> ComparisonResult:
        """Calculate compliance statistics"""
        
        total = len(items)
        compliant = sum(1 for i in items if i.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for i in items if i.status == ComplianceStatus.PARTIAL)
        non_compliant = sum(1 for i in items if i.status == ComplianceStatus.NON_COMPLIANT)
        unknown = sum(1 for i in items if i.status == ComplianceStatus.UNKNOWN)
        
        # Calculate compliance percentage (unknowns count as failures)
        compliance_percentage = (compliant + partial * 0.5) / total * 100 if total > 0 else 0
        
        # Generate summary
        summary = f"Document: {document_name}\n"
        summary += f"Specification: {spec_name}\n"
        summary += f"Compliance: {compliance_percentage:.1f}%\n"
        summary += f"Compliant: {compliant}/{total} | "
        summary += f"Partial: {partial}/{total} | "
        summary += f"Non-Compliant: {non_compliant}/{total} | "
        summary += f"Unknown: {unknown}/{total}"
        
        return ComparisonResult(
            document_name=document_name,
            spec_name=spec_name,
            comparison_timestamp=datetime.now().isoformat(),
            total_requirements=total,
            compliant_items=compliant,
            partial_items=partial,
            non_compliant_items=non_compliant,
            unknown_items=unknown,
            compliance_percentage=compliance_percentage,
            items=items,
            summary=summary
        )
    
    def compare_multiple_documents(
        self,
        document_names: List[str],
        specifications: List[str] | Dict[str, Any],
        spec_name: str = "Specification"
    ) -> Dict[str, ComparisonResult]:
        """
        Compare multiple documents against same specification
        
        Args:
            document_names: List of document names
            specifications: Specification to compare against
            spec_name: Name of specification
            
        Returns:
            Dictionary of comparison results keyed by document name
        """
        results = {}
        
        for doc_name in document_names:
            result = self.compare_document_to_spec(
                doc_name,
                specifications,
                spec_name
            )
            results[doc_name] = result
        
        return results
    
    def generate_compliance_report(
        self,
        comparison_result: ComparisonResult,
        output_format: str = "json"
    ) -> str:
        """
        Generate compliance report in specified format
        
        Args:
            comparison_result: ComparisonResult object
            output_format: 'json', 'text', or 'html'
            
        Returns:
            Formatted report string
        """
        if output_format == "json":
            return self._format_json_report(comparison_result)
        elif output_format == "text":
            return self._format_text_report(comparison_result)
        elif output_format == "html":
            return self._format_html_report(comparison_result)
        else:
            raise ValueError(f"Unknown format: {output_format}")
    
    def _format_json_report(self, result: ComparisonResult) -> str:
        """Format as JSON"""
        result_dict = asdict(result)
        # Convert enum to string
        result_dict["items"] = [
            {
                **asdict(item),
                "status": item.status.value
            }
            for item in result.items
        ]
        return json.dumps(result_dict, indent=2)
    
    def _format_text_report(self, result: ComparisonResult) -> str:
        """Format as plain text"""
        report = f"""
{'='*70}
COMPLIANCE REPORT
{'='*70}

{result.summary}

{'='*70}
DETAILED FINDINGS
{'='*70}

"""
        for item in result.items:
            report += f"\n[{item.requirement_id}] {item.status.value.upper()}\n"
            report += f"Requirement: {item.requirement_text}\n"
            if item.expected_value:
                report += f"Expected: {item.expected_value}\n"
            if item.found_value:
                report += f"Found: {item.found_value}\n"
            if item.evidence:
                report += f"Evidence:\n"
                for i, ev in enumerate(item.evidence, 1):
                    report += f"  {i}. {ev}\n"
            if item.notes:
                report += f"Notes: {item.notes}\n"
            report += "\n"
        
        report += f"\n{'='*70}\nReport generated: {result.comparison_timestamp}\n"
        
        return report
    
    def _format_html_report(self, result: ComparisonResult) -> str:
        """Format as HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Compliance Report - {result.document_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2 {{ color: #333; }}
        .summary {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .compliant {{ color: green; font-weight: bold; }}
        .partial {{ color: orange; font-weight: bold; }}
        .non-compliant {{ color: red; font-weight: bold; }}
        .unknown {{ color: gray; font-weight: bold; }}
        .item {{ margin: 20px 0; padding: 10px; border-left: 4px solid #ddd; }}
        .item.compliant {{ border-left-color: green; }}
        .item.partial {{ border-left-color: orange; }}
        .item.non-compliant {{ border-left-color: red; }}
        .evidence {{ margin-left: 20px; font-size: 0.9em; color: #666; }}
    </style>
</head>
<body>
    <h1>Compliance Report</h1>
    <div class="summary">
        <h2>{result.document_name}</h2>
        <p><strong>Specification:</strong> {result.spec_name}</p>
        <p><strong>Compliance:</strong> <span style="font-size: 1.5em;">{result.compliance_percentage:.1f}%</span></p>
        <p>Compliant: {result.compliant_items} | Partial: {result.partial_items} | Non-Compliant: {result.non_compliant_items} | Unknown: {result.unknown_items}</p>
    </div>
    
    <h2>Detailed Findings</h2>
"""
        
        for item in result.items:
            html += f"""
    <div class="item {item.status.value}">
        <h3>[{item.requirement_id}] <span class="{item.status.value}">{item.status.value.upper()}</span></h3>
        <p><strong>Requirement:</strong> {item.requirement_text}</p>
"""
            if item.expected_value:
                html += f"        <p><strong>Expected:</strong> {item.expected_value}</p>\n"
            if item.found_value:
                html += f"        <p><strong>Found:</strong> {item.found_value}</p>\n"
            if item.evidence:
                html += "        <div class='evidence'><strong>Evidence:</strong><ul>\n"
                for ev in item.evidence:
                    html += f"            <li>{ev}</li>\n"
                html += "        </ul></div>\n"
            if item.notes:
                html += f"        <p><strong>Notes:</strong> {item.notes}</p>\n"
            html += "    </div>\n"
        
        html += f"""
    <p><em>Report generated: {result.comparison_timestamp}</em></p>
</body>
</html>
"""
        return html
