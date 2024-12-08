# Python Code Processor

A simple Flask web application that processes Python files by removing comments and replacing random words with underscores. This tool is useful for experimenting with code transformations or obfuscations.

## Features

-   Upload Python files to process them.
-   Automatically removes single-line and multi-line comments.
-   Replaces a specified number of random words in the code with underscores.
-   Download the processed file directly from the app.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or higher installed on your system. To check your Python version, run:
`python --version`


### Installation

1.  Clone the repository:

	```
	git clone https://github.com/yourusername/python-code-processor.git
	cd python-code-processor
	```

2. Create a virtual environment:

	`python -m venv venv`

3. Activate the virtual environment:

    Windows (Command Prompt):

		`venv\Scripts\activate`

> Windows (PowerShell):

		`.\venv\Scripts\Activate.ps1`

> Mac/Linux:

	    source venv/bin/activate

4. Install dependencies:

	`pip install -r requirements.txt`

### Running the Application
1. Start the Flask development server:
	`python app.py`

2. Open your browser and navigate to:
	`http://127.0.0.1:5000`

3. Upload a `.py` file, and the processed file will be ready for download.

