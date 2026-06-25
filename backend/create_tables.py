from app.db.base import Base
from app.db.session import engine

# IMPORTANT: import every model so SQLAlchemy registers them
from app.models.document_chunk import DocumentChunk
from app.models.company import Company
from app.models.filing import Filing
from app.models.user import User
from app.models.watchlist import Watchlist
from app.models.portfolio import Portfolio

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
