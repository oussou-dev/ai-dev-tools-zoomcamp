import os
from datetime import datetime

import streamlit as st
import requests
from requests.exceptions import ConnectionError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration - Dynamic API URL with trailing slash removal
API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

# Page config
st.set_page_config(
    page_title="AI News Aggregator",
    page_icon="🤖",
    layout="wide",
)


def check_backend_status() -> bool:
    """Check if the backend API is online.

    Returns:
        True if online, False otherwise
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except ConnectionError:
        return False
    except Exception:
        return False


def run_pipeline():
    """Trigger the pipeline to run in the background."""
    try:
        with st.spinner("🔄 Agents are working..."):
            response = requests.post(
                f"{API_URL}/pipeline/run",
                params={"hours": 24, "top_n": 10},
                timeout=30,
            )

        if response.status_code == 200:
            st.success("✅ Pipeline started! Agents are working in the background.")
        else:
            st.error(f"❌ Failed to start pipeline: {response.status_code}")
    except ConnectionError:
        st.error("❌ Cannot connect to backend API. Is it running?")
    except Exception as e:
        st.error(f"❌ Error starting pipeline: {str(e)}")


def fetch_digests(limit: int = 20) -> list:
    """Fetch recent digests from the backend API.

    Args:
        limit: Maximum number of digests to fetch

    Returns:
        List of digest objects, or empty list on error
    """
    try:
        response = requests.get(
            f"{API_URL}/digests",
            params={"limit": limit},
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Failed to fetch digests: {response.status_code}")
            return []
    except ConnectionError:
        st.error("❌ Cannot connect to backend API. Is it running?")
        return []
    except Exception as e:
        st.error(f"❌ Error fetching digests: {str(e)}")
        return []


def format_date(date_str: str) -> str:
    """Format ISO datetime string to readable format.

    Args:
        date_str: ISO format datetime string

    Returns:
        Formatted date string
    """
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except Exception:
        return date_str


def get_source_emoji(article_type: str) -> str:
    """Get emoji for article type.

    Args:
        article_type: Type of article (youtube, openai, anthropic, etc.)

    Returns:
        Appropriate emoji for the article type
    """
    emoji_map = {
        "youtube": "🎥",
        "openai": "🤖",
        "anthropic": "🧠",
    }
    return emoji_map.get(article_type.lower(), "📝")


# ============================================================================
# MAIN LAYOUT
# ============================================================================

# Sidebar: Pipeline Controls
with st.sidebar:
    st.title("⚙️ Pipeline Controls")

    # Backend Status
    st.subheader("Backend Status")
    is_online = check_backend_status()
    if is_online:
        st.success("🟢 Online")
    else:
        st.error("🔴 Offline")

    st.divider()

    # Run Pipeline Button
    st.subheader("Actions")
    if st.button("🚀 Run Pipeline", use_container_width=True):
        run_pipeline()

    st.divider()

    # Configuration Info
    st.subheader("Configuration")
    st.caption(f"**API URL:** {API_URL}")


# Main Area: News Feed
st.title("🧠 AI News Aggregator")

# Top controls
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown("Stay updated with the latest AI news, research, and trends.")
with col2:
    if st.button("🔄 Refresh Feed", use_container_width=True):
        st.rerun()

st.divider()

# Fetch and display digests
digests = fetch_digests(limit=20)

if not digests:
    st.info("📭 No digests available yet. Run the pipeline to get started!")
else:
    st.markdown(f"**Found {len(digests)} articles**")
    st.divider()

    for idx, digest in enumerate(digests, 1):
        with st.container(border=True):
            # Header: Title + Source
            source_emoji = get_source_emoji(digest.get("article_type", ""))
            st.markdown(
                f"### {source_emoji} {digest.get('title', 'Untitled')}"
            )

            # Body: Summary
            st.markdown(digest.get("summary", "No summary available"))

            # Footer: Published date and link
            published = format_date(digest.get("published_at", ""))
            url = digest.get("url", "#")

            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.caption(f"📅 Published: {published}")
            with col2:
                st.markdown(f"[Read Original →]({url})")

            # Article type label
            article_type = digest.get("article_type", "unknown").upper()
            st.caption(f"Source: {article_type}")
