# Meeting Minutes to Project Plan Processor

This application processes meeting minutes and converts them into structured project plan items. It uses OpenAI's API to extract relevant information and generates Excel and JSON outputs with the extracted data.

## Features

- Extract project items from meeting minutes text
- Categorize items according to predefined streams, substreams, initiatives, etc.
- Generate Excel files with data validation for specific fields
- Save extracted data as JSON
- Simple GUI interface

## Setup

1. Clone this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment:
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Alternatively, you can set it in your environment:
     ```
     export OPENAI_API_KEY='your-api-key'
     ```

## Usage

Run the application:
```
python main.py
```

1. Copy and paste your meeting minutes into the text area
2. Click "Process Minutes"
3. The application will process the minutes and generate:
   - An Excel file with extracted project items
   - A JSON file with the same data
   - A summary of extracted items in the UI

## Project Structure

- `main.py`: Main entry point
- `models/`: Data models using Pydantic
- `services/`: Core functionality services
- `ui/`: User interface components
- `config/`: Application configuration
- `.env`: Environment variables (create from .env.example)
- `.gitignore`: Git ignore patterns

## Customization

### Field Options
To modify the available options for fields like Stream, Substream, etc., edit the enum definitions in `models/enums.py`.

### Environment Variables
You can customize the application by setting the following environment variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: The OpenAI model to use (default: "gpt-4o-2024-08-06")
- `APP_OUTPUT_DIR`: Directory to save output files (default: current directory)
- `APP_PREFIX`: Prefix for output filenames (default: "Project_Items")
- `TIMESTAMP_FORMAT`: Format for timestamps in filenames (default: "%Y%m%d_%H%M%S")
- `APP_TITLE`: Application window title
- `APP_SIZE`: Application window size (default: "900x800")
- `APP_INPUT_HEIGHT`: Height of the input text area (default: 15)
- `APP_RESULT_HEIGHT`: Height of the result text area (default: 20)
- `VALIDATE_FIELDS`: Whether to validate field values (default: true)