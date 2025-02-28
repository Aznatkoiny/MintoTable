"""
GUI implementation for the meeting minutes processor
"""

import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from config.app_config import UI_WINDOW_TITLE, UI_WINDOW_SIZE, UI_INPUT_HEIGHT, UI_RESULT_HEIGHT
from services.openai_service import process_minutes, set_api_key
from services.excel_service import create_excel
from services.json_service import save_json

def _display_results(result_text, minutes_data):
    """
    Display the extracted data in the result text area
    
    Args:
        result_text: Tkinter text widget
        minutes_data: Minutes object
    """
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Meeting: {minutes_data.meeting_title or 'Untitled'}\n")
    result_text.insert(tk.END, f"Date: {minutes_data.meeting_date or 'Not specified'}\n")
    result_text.insert(tk.END, f"Attendees: {', '.join(minutes_data.attendees) or 'None specified'}\n\n")
    
    result_text.insert(tk.END, f"Extracted Project Items ({len(minutes_data.items)}):\n\n")
    
    for i, item in enumerate(minutes_data.items, start=1):
        item_dict = item.model_dump()
        result_text.insert(tk.END, f"Item {i}:\n")
        
        for key, value in item_dict.items():
            if value and value != [] and value != {}:
                # Format lists nicely
                if isinstance(value, list):
                    value_str = ", ".join(value)
                # Format enum values
                elif hasattr(value, 'value'):
                    value_str = value.value
                else:
                    value_str = str(value)
                    
                result_text.insert(tk.END, f"  {key}: {value_str}\n")
        
        result_text.insert(tk.END, "\n")

def create_gui():
    """Create a simple GUI for inputting meeting minutes"""
    
    def on_submit():
        """Handle submit button click"""
        # Get API key
        api_key = api_key_entry.get()
        if not api_key:
            messagebox.showerror("Error", "Please enter your OpenAI API key")
            return
        
        # Set API key
        set_api_key(api_key)
        
        # Get minutes text
        minutes_text = text_input.get("1.0", tk.END)
        if not minutes_text.strip():
            messagebox.showerror("Error", "Please enter meeting minutes")
            return
        
        status_label.config(text="Processing minutes... This may take a moment.")
        progress_bar.start(10)
        root.update()
        
        try:
            # Process the minutes
            minutes_data = process_minutes(minutes_text)
            
            # Save as JSON
            json_path = save_json(minutes_data)
            
            # Create Excel file
            excel_path = create_excel(minutes_data)
            
            status_label.config(text=f"Success! Files created:\n{json_path}\n{excel_path}")
            progress_bar.stop()
            
            # Show the extracted items in the result area
            _display_results(result_text, minutes_data)
            
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            progress_bar.stop()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    # Create the main window
    root = tk.Tk()
    root.title(UI_WINDOW_TITLE)
    root.geometry(UI_WINDOW_SIZE)
    
    # Create main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # API Key entry
    api_key_frame = ttk.LabelFrame(main_frame, text="OpenAI API Key")
    api_key_frame.pack(padx=10, pady=5, fill=tk.X)
    
    api_key_entry = ttk.Entry(api_key_frame, width=70, show="*")
    api_key_entry.pack(padx=5, pady=5, fill=tk.X)
    
    # API Key instructions
    api_key_info = ttk.Label(
        api_key_frame, 
        text="Enter your OpenAI API key above. Your key is required to process the minutes.",
        wraplength=800
    )
    api_key_info.pack(padx=5, pady=2)
    
    # Check if API key is in environment and use it
    if os.environ.get("OPENAI_API_KEY"):
        api_key_entry.insert(0, os.environ.get("OPENAI_API_KEY"))
    
    # Instructions
    instructions = ttk.Label(main_frame, text="Copy and paste your meeting minutes below:")
    instructions.pack(pady=10)
    
    # Text input area with frame
    input_frame = ttk.LabelFrame(main_frame, text="Meeting Minutes")
    input_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    text_input = scrolledtext.ScrolledText(input_frame, height=UI_INPUT_HEIGHT)
    text_input.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
    
    # Control frame
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill=tk.X, pady=5)
    
    # Submit button
    submit_button = ttk.Button(control_frame, text="Process Minutes", command=on_submit)
    submit_button.pack(side=tk.LEFT, padx=10)
    
    # Progress bar
    progress_bar = ttk.Progressbar(control_frame, orient="horizontal", length=300, mode="indeterminate")
    progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    # Status label
    status_label = ttk.Label(main_frame, text="")
    status_label.pack(pady=5)
    
    # Result area with frame
    result_frame = ttk.LabelFrame(main_frame, text="Extracted Project Items")
    result_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    result_text = scrolledtext.ScrolledText(result_frame, height=UI_RESULT_HEIGHT)
    result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
    
    # Start the main loop
    root.mainloop()