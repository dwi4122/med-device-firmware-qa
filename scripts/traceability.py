"""Traceability matrix for regulatory compliance."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Requirement:
    """Represents a regulatory requirement and associated test cases."""
    
    id: str
    description: str
    test_cases: List[str]


class TraceabilityMatrix:
    """Maps test cases to regulatory requirements."""

    def __init__(self):
        """Initialize the traceability matrix with predefined requirements."""
        self.requirements = {
            "IEC_62304_5.7": Requirement(
                id="IEC_62304_5.7",
                description="Software update reliability",
                test_cases=[
                    "firmware_update_test.robot::Valid Firmware Update",
                    "firmware_recovery_test.robot::Rollback After Failed Update"
                ]
            ),
            "ISO_80601_2_70_201.12": Requirement(
                id="ISO_80601_2_70_201.12",
                description="Pressure control accuracy",
                test_cases=[
                    "firmware_update_test.robot::Pressure Control Validation"
                ]
            )
        }

    def get_tests_for_requirement(self, requirement_id: str) -> List[str]:
        """Get test cases mapped to a specific requirement.
        
        Args:
            requirement_id (str): The ID of the regulatory requirement.

        Returns:
            List[str]: List of test cases associated with the requirement.
        """
        if requirement_id in self.requirements:
            return self.requirements[requirement_id].test_cases
        return []

    def generate_report(self) -> Dict:
        """Generate traceability report summarizing requirements and test cases.
        
        Returns:
            Dict: A dictionary containing the report with requirement details 
                  and total test count.
        """
        return {
            "requirements": [
                {
                    "id": req.id,
                    "description": req.description,
                    "test_count": len(req.test_cases)
                }
                for req in self.requirements.values()
            ],
            "total_tests": sum(
                len(req.test_cases)
                for req in self.requirements.values()
            )
        }
