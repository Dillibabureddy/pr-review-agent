# PR Review Agent by BANDI DILLI BABU REDDY

A multi-server Pull Request review agent that analyzes code quality, standards, and potential issues across GitHub, GitLab, and Bitbucket.

## Features

- **Multi-server Compatibility**: Supports GitHub, GitLab, and Bitbucket
- **Code Quality Analysis**: Integrates with Flake8, Pylint, and Radon for comprehensive code analysis
- **Structured Feedback**: Generates human-readable feedback with severity categorization
- **Quality Scoring**: Calculates a quality score based on identified issues
- **Web Interface**: Modern web application for easy access

## Installation

### For Local Development

```bash
cd pr-review-agent
pip install -r requirements.txt
pip install -r requirements-web.txt
pip install flake8 pylint radon
```

### For Production Deployment

```bash
pip install -r requirements-web.txt
```

## Usage

### Running Locally

```bash
uvicorn app:app --reload
```

Then visit `http://localhost:8000` in your browser.

### Using the Web Interface

1. Navigate to the web application
2. Select your Git server (GitHub, GitLab, or Bitbucket)
3. Enter repository owner/organization name
4. Enter repository name
5. Enter pull request number
6. Optionally enter a personal access token for private repositories
7. Click "Review Pull Request"

## Web Application Structure

- **Backend**: FastAPI application (`app.py`)
- **Frontend**: HTML templates with Tailwind CSS styling
- **Templates**: Jinja2 templates in `/templates/`
- **Static Files**: CSS, JS, and assets in `/static/`

## Deployment Options

### Deploy to Heroku

1. Create a `Procfile`:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

2. Create a `runtime.txt`:
```
python-3.10
```

3. Push to Heroku

### Deploy to GitHub Pages

For static hosting, you can deploy the frontend separately and connect it to your backend API.

### Deploy to PythonAnywhere

1. Upload all files to PythonAnywhere
2. Install dependencies: `pip install -r requirements-web.txt`
3. Run with: `uvicorn app:app --host 0.0.0.0 --port 8000`

## Architecture

### Components

1. **Fetcher Modules**: Handle PR/MR retrieval from different git servers
   - `github_fetcher.py`: GitHub PR fetching
   - `gitlab_fetcher.py`: GitLab MR fetching  
   - `bitbucket_fetcher.py`: Bitbucket PR fetching

2. **Analyzer Modules**: Perform code quality checks
   - `flake8_analyzer.py`: Style guide enforcement
   - `pylint_analyzer.py`: Code quality and error detection
   - `radon_analyzer.py`: Code complexity metrics

3. **Feedback Generator**: Create human-readable review feedback
   - `feedback_generator.py`: Structured feedback generation

4. **Web Application**: FastAPI backend with web interface
   - `app.py`: Main FastAPI application
   - `templates/`: HTML templates for web interface
   - `static/`: Static assets (CSS, JS, images)

## Requirements

- Python 3.7+
- FastAPI
- uvicorn
- requests
- GitPython
- flake8
- pylint
- radon
- PyYAML

## License

MIT

