"""
OpenAI API service for processing meeting minutes
"""

import json
from openai import OpenAI
from models.enums import Stream, Substream, Initiative, ItemType, Stage
from models.project_models import ProjectItem, Minutes
from config.app_config import OPENAI_MODEL

# Initialize the OpenAI client with None (will be set later)
client = None

def set_api_key(api_key):
    """
    Set the OpenAI API key
    
    Args:
        api_key (str): The OpenAI API key
    """
    global client
    client = OpenAI(api_key=api_key)

def _extract_meeting_info(text):
    """
    Extract basic meeting information like title, date, attendees, and summary
    
    Args:
        text (str): Raw meeting minutes text
        
    Returns:
        dict: Extracted meeting information
    """
    if client is None:
        raise ValueError("OpenAI API key not set. Please set your API key first.")
        
    meeting_info_prompt = """
    Extract the following information from the meeting minutes: 
    - meeting_title: The title or name of the meeting
    - meeting_date: The date when the meeting was held
    - attendees: List of people who attended the meeting
    - summary: A brief summary of what was discussed
    
    Return the information in JSON format.
    """
    
    meeting_info_completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": meeting_info_prompt},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(meeting_info_completion.choices[0].message.content)

def _extract_project_items(text):
    """
    Extract project items from the meeting minutes
    
    Args:
        text (str): Raw meeting minutes text
        
    Returns:
        list: List of project item dictionaries
    """
    if client is None:
        raise ValueError("OpenAI API key not set. Please set your API key first.")
        
    project_items_prompt = """
    Based on the meeting minutes, identify tasks, action items, decisions, or any work that needs to be done.
    For each item, extract as much of the following information as possible:
    
    - TaskID: Generate a unique identifier if not present
    - Stream: Categorize into one of the following: Governance, Marketing and Communications, Onboarding & Training, Product Development & Technology
    - Substream: Categorize into one of the following: Governance, Internal & External Communications, Training Material Development, Module Enhancements & Testing
    - Initiative: Categorize into one of the following: CTU Approval, Other, Go-to-Market, Future State Process & Training, MVP 1, MVP 2, MVP 3, Testing, Endeavor, IP Hub
    - Type: Categorize as either Technical or Functional
    - WorkItem: A short title for the task
    - Description: Detailed description of what needs to be done
    - AssignedTo: Person responsible for the task
    - Progress: Current progress (percentage or status)
    - Priority: Task priority (High, Medium, Low)
    - StartDate: When the task should start or started
    - DueDate: When the task is due
    - FinishDate: When the task was actually completed
    - Stage: Current stage from: Backlog, Research, In-Progress, Q&A, Done
    - Sprint: Associated sprint if applicable
    - JiraID: Associated Jira ticket if mentioned
    - KeyStakeholders: List of people who have a stake in this item
    - RAIDTags: Any risks, assumptions, issues, or dependencies mentioned
    - Source: Where this item originated (e.g., "Weekly Team Meeting")
    - LinkToSource: Any URL or reference to the source
    - GanttSwimlane: Associated Gantt chart swimlane if mentioned
    - GanttItem: Associated Gantt chart item if mentioned
    - Screenshots: Any references to screenshots or images

    Provide the output as a JSON object with an "items" key containing an array of objects, with each object containing the fields above where information is available.
    If a field requires specific values (Stream, Substream, Initiative, Type, Stage), use only the provided options or leave empty.
    """
    
    project_items_completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": project_items_prompt},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(project_items_completion.choices[0].message.content)
    return result.get('items', [])

def _validate_project_item(item_data):
    """
    Validate and clean up project item data
    
    Args:
        item_data (dict): Raw project item data
        
    Returns:
        dict: Validated project item data
    """
    # Handle enum fields by checking if they match valid options
    if 'Stream' in item_data and item_data['Stream']:
        try:
            item_data['Stream'] = Stream(item_data['Stream'])
        except ValueError:
            item_data['Stream'] = None
            
    if 'Substream' in item_data and item_data['Substream']:
        try:
            item_data['Substream'] = Substream(item_data['Substream'])
        except ValueError:
            item_data['Substream'] = None
            
    if 'Initiative' in item_data and item_data['Initiative']:
        try:
            item_data['Initiative'] = Initiative(item_data['Initiative'])
        except ValueError:
            item_data['Initiative'] = None
            
    if 'Type' in item_data and item_data['Type']:
        try:
            item_data['Type'] = ItemType(item_data['Type'])
        except ValueError:
            item_data['Type'] = None
            
    if 'Stage' in item_data and item_data['Stage']:
        try:
            item_data['Stage'] = Stage(item_data['Stage'])
        except ValueError:
            item_data['Stage'] = None
    
    return item_data

def process_minutes(text):
    """
    Process the minutes using OpenAI's API and return structured data
    
    Args:
        text (str): Raw meeting minutes text
        
    Returns:
        Minutes: Structured minutes data
    """
    if client is None:
        raise ValueError("OpenAI API key not set. Please set your API key first.")
        
    try:
        # Extract basic meeting information
        meeting_info = _extract_meeting_info(text)
        
        # Extract project items
        project_items_data = _extract_project_items(text)
        
        # Create the Minutes object
        minutes = Minutes(
            raw_text=text,
            meeting_title=meeting_info.get('meeting_title', ''),
            meeting_date=meeting_info.get('meeting_date', ''),
            attendees=meeting_info.get('attendees', []),
            summary=meeting_info.get('summary', ''),
            items=[]
        )
        
        # Parse and validate project items
        for item_data in project_items_data:
            # Validate the item data
            validated_item_data = _validate_project_item(item_data)
            
            # Create and add the project item
            project_item = ProjectItem(**validated_item_data)
            minutes.items.append(project_item)
        
        return minutes
    
    except Exception as e:
        print(f"Error processing minutes: {e}")
        raise