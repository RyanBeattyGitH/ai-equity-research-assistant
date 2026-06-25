from app.db.base import Base
from app.db.session import engine

# IMPORTANT: ensure all models are imported so SQLAlchemy registers them
from app.models.document_chunk import DocumentChunk
from app.models.company import Company
from app.models.filing import Filing
from app.models.user import User

def init():
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done")

if __name__ == "__main__":
    init()
