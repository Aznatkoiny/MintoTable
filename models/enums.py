"""
Enum definitions for data validation
"""

from enum import Enum

class Stream(str, Enum):
    """Valid options for Stream field"""
    GOVERNANCE = "Governance"
    MARKETING = "Marketing and Communications"
    ONBOARDING = "Onboarding & Training"
    PRODUCT = "Product Development & Technology"

class Substream(str, Enum):
    """Valid options for Substream field"""
    GOVERNANCE = "Governance"
    COMMUNICATIONS = "Internal & External Communications"
    TRAINING = "Training Material Development"
    MODULE = "Module Enhancements & Testing"

class Initiative(str, Enum):
    """Valid options for Initiative field"""
    CTU = "CTU Approval"
    OTHER = "Other"
    GTM = "Go-to-Market"
    FUTURE = "Future State Process & Training"
    MVP1 = "MVP 1"
    MVP2 = "MVP 2"
    MVP3 = "MVP 3"
    TESTING = "Testing"
    ENDEAVOR = "Endeavor"
    IP_HUB = "IP Hub"

class ItemType(str, Enum):
    """Valid options for Type field"""
    TECHNICAL = "Technical"
    FUNCTIONAL = "Functional"

class Stage(str, Enum):
    """Valid options for Stage field"""
    BACKLOG = "Backlog"
    RESEARCH = "Research"
    IN_PROGRESS = "In-Progress"
    QA = "Q&A"
    DONE = "Done"