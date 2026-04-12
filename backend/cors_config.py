from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    """
    Configure CORS middleware for the FastAPI app.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://rag-ai-assistant-c6f9.vercel.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )