# Application-Level Tenant Context Scoping

We evaluated enforcing PostgreSQL Row-Level Security (RLS) policies versus dependency-injected application-level query scoping in FastAPI. We decided to enforce multi-tenant isolation through application-level `Tenant Context` dependency injection across all database sessions and repository operations. This avoids RLS connection pool contamination issues in async SQLAlchemy/SQLModel environments, simplifies local testing, and guarantees explicit tenant filtering without complex database session initialization scripts.
