from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
import os

# Import your existing modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import PRReviewAgent

app = FastAPI(title="PR Review Agent", description="Web interface for reviewing pull requests from GitHub, GitLab, and Bitbucket")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/review", response_class=HTMLResponse)
async def review_pr(
    request: Request,
    server: str = Form(...),
    owner: str = Form(...),
    repo: str = Form(...),
    pr_number: int = Form(...),
    token: str = Form(None),
    base_url: str = Form(None)
):
    try:
        # Initialize the agent
        agent = PRReviewAgent()
        
        # Perform the review
        result = agent.review_pr(
            server_type=server,
            repo_owner=owner,
            repo_name=repo,
            pr_number=pr_number,
            token=token,
            base_url=base_url
        )
        
        # Return the results
        return templates.TemplateResponse("results.html", {
            "request": request,
            "result": result,
            "server": server,
            "owner": owner,
            "repo": repo,
            "pr_number": pr_number
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during PR review: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
