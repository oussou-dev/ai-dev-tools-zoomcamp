# Phase 10: Frontend (Streamlit consuming API)

This phase builds the UI, strictly decoupled from the backend logic via HTTP requests.

---

Prompt_30

```
# Task_1    
Generate `app/frontend/main.py`.

# Goal
Create a dashboard to view AI News and trigger the collection pipeline.

# Tech
- Streamlit
- Requests
- Pandas (for data handling)

# Requirements
1.  **Configuration**:
    - Load `API_URL` from env (default: `http://localhost:8000`).
    - Set page config to "wide" layout with a robot emoji 🤖.

2.  **Sidebar (Control Center)**:
    - Title: "⚙️ Pipeline Controls".
    - **Backend Status**: Call `GET /health`. Display a green badge "Online" if 200 OK, else red "Offline".
    - **Trigger Button**: "🚀 Run Pipeline".
        - Action: Call `POST /pipeline/run`.
        - UX: Show `st.spinner("Agents are working...")` while request is sending.
        - Result: Show success/error toast or message based on API response.

3.  **Main Area (The Feed)**:
    - Title: "🧠 AI News Aggregator".
    - **Data Fetching**:
        - Call `GET /digests?limit=20`.
        - If error, show `st.error`.
    - **Display Logic**:
        - Iterate through the list of digests.
        - Use `st.container(border=True)` for each item.
        - **Inside the container**:
            - Header: Title + Source Icon (use `article_type` to choose emoji: 🎥 for youtube, 📝 for others).
            - Body: Summary.
            - Footer: "Published: {date}" | [Read Original]({url}).

4.  **Refinement**:
    - Add a "Refresh Feed" button in the top right (using `st.rerun()`).

# Instructions
- **Crucial**: Do NOT import any backend code. Use `requests` only.
- Handle `requests.exceptions.ConnectionError` gracefully (API might be starting up).
```