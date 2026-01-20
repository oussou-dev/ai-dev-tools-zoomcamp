from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.main import app, get_db
from app.database.repository import Repository


@pytest.fixture
def override_get_db(test_db):
    """Override the get_db dependency to use the test database."""
    def _get_test_db():
        yield test_db

    return _get_test_db


@pytest.fixture
def client(override_get_db):
    """Create a test client with overridden dependencies."""
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test GET /health returns 200 with status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestPipeline:
    """Test pipeline execution endpoint."""

    def test_trigger_pipeline(self, client):
        """Test POST /pipeline/run returns 200 and accepts the request."""
        response = client.post("/pipeline/run")
        assert response.status_code in [200, 202]
        assert "message" in response.json()
        assert "Pipeline started in background" in response.json()["message"]

    def test_trigger_pipeline_with_params(self, client):
        """Test POST /pipeline/run with custom parameters."""
        response = client.post("/pipeline/run", params={"hours": 48, "top_n": 5})
        assert response.status_code in [200, 202]
        assert "message" in response.json()
        assert "Pipeline started in background" in response.json()["message"]


class TestDigests:
    """Test digests retrieval endpoint."""

    def test_fetch_digests_empty(self, client):
        """Test GET /digests returns empty list when no digests exist."""
        response = client.get("/digests")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    def test_fetch_digests_with_data(self, client, test_db):
        """Test GET /digests returns digests after inserting test data."""
        # Insert test digest into database
        repo = Repository(session=test_db)
        repo.create_digest(
            article_type="test",
            article_id="test_article_1",
            url="https://example.com/article1",
            title="Test Article Title",
            summary="This is a test summary of the article.",
            published_at=datetime.now(timezone.utc),
        )

        # Fetch digests via API
        response = client.get("/digests")
        assert response.status_code == 200
        digests = response.json()
        assert len(digests) > 0

        # Verify structure of first digest
        first_digest = digests[0]
        assert "id" in first_digest
        assert "title" in first_digest
        assert "summary" in first_digest
        assert "article_type" in first_digest
        assert "url" in first_digest
        assert "published_at" in first_digest
        assert "created_at" in first_digest

        # Verify content
        assert first_digest["title"] == "Test Article Title"
        assert first_digest["summary"] == "This is a test summary of the article."
        assert first_digest["article_type"] == "test"

    def test_fetch_digests_with_limit(self, client, test_db):
        """Test GET /digests respects limit parameter."""
        # Insert multiple test digests
        repo = Repository(session=test_db)
        for i in range(5):
            repo.create_digest(
                article_type="test",
                article_id=f"test_article_{i}",
                url=f"https://example.com/article{i}",
                title=f"Test Article {i}",
                summary=f"Summary {i}",
                published_at=datetime.now(timezone.utc),
            )

        # Fetch with limit
        response = client.get("/digests", params={"limit": 2})
        assert response.status_code == 200
        digests = response.json()
        assert len(digests) == 2

    def test_fetch_digests_default_limit(self, client, test_db):
        """Test GET /digests uses default limit of 50."""
        # Insert 100 test digests
        repo = Repository(session=test_db)
        for i in range(100):
            repo.create_digest(
                article_type="test",
                article_id=f"test_article_{i}",
                url=f"https://example.com/article{i}",
                title=f"Test Article {i}",
                summary=f"Summary {i}",
                published_at=datetime.now(timezone.utc),
            )

        # Fetch without limit parameter (should default to 50)
        response = client.get("/digests")
        assert response.status_code == 200
        digests = response.json()
        assert len(digests) == 50  # Default limit

    def test_digests_response_structure(self, client, test_db):
        """Test that digest response matches the expected schema."""
        # Insert test digest
        repo = Repository(session=test_db)
        repo.create_digest(
            article_type="youtube",
            article_id="test_video_123",
            url="https://youtube.com/watch?v=test",
            title="YouTube Video Title",
            summary="This is a video summary.",
            published_at=datetime.now(timezone.utc),
        )

        # Fetch digests
        response = client.get("/digests")
        assert response.status_code == 200
        digests = response.json()
        assert len(digests) == 1

        digest = digests[0]

        # Verify all required fields are present
        required_fields = ["id", "title", "url", "summary", "article_type", "published_at", "created_at"]
        for field in required_fields:
            assert field in digest, f"Missing field: {field}"

        # Verify field types
        assert isinstance(digest["id"], str)
        assert isinstance(digest["title"], str)
        assert isinstance(digest["url"], str)
        assert isinstance(digest["summary"], str)
        assert isinstance(digest["article_type"], str)
        assert isinstance(digest["published_at"], str)  # ISO format datetime
        assert isinstance(digest["created_at"], str)  # ISO format datetime
