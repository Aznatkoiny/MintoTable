"""
Pydantic models for project items and meeting minutes
"""

from pydantic import BaseModel
from typing import List, Optional
from .enums import Stream, Substream, Initiative, ItemType, Stage

class ProjectItem(BaseModel):
    """
    Model for a project item extracted from meeting minutes.
    Contains all required fields for the project plan.
    """
    TaskID: Optional[str] = None
    Stream: Optional[Stream] = None
    Substream: Optional[Substream] = None
    Initiative: Optional[Initiative] = None
    Type: Optional[ItemType] = None
    WorkItem: Optional[str] = None
    Description: Optional[str] = None
    AssignedTo: Optional[str] = None
    Progress: Optional[str] = None
    Priority: Optional[str] = None
    StartDate: Optional[str] = None
    DueDate: Optional[str] = None
    FinishDate: Optional[str] = None
    Stage: Optional[Stage] = None
    Sprint: Optional[str] = None
    JiraID: Optional[str] = None
    KeyStakeholders: Optional[List[str]] = []
    RAIDTags: Optional[List[str]] = []
    Source: Optional[str] = None
    LinkToSource: Optional[str] = None
    GanttSwimlane: Optional[str] = None
    GanttItem: Optional[str] = None
    Screenshots: Optional[List[str]] = []

class Minutes(BaseModel):
    """
    Model for structured meeting minutes.
    Contains meeting metadata and extracted project items.
    """
    raw_text: str
    meeting_title: Optional[str] = None
    meeting_date: Optional[str] = None
    attendees: List[str] = []
    summary: Optional[str] = None
    items: List[ProjectItem] = []