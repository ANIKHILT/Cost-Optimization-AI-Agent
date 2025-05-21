# Cost-Optimization-AI-Agent
Multi-Cloud Cost Optimization Agent

### Local Setup Instructions (GCP Only for Now)

1. **Install CLI tools**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Authenticate GCP**:
   ```bash
   gcloud auth application-default login
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
   ```

3. **Permissions Needed (GCP)**:
   - Compute Viewer
   - Compute Admin (for delete)
   - Storage Admin (optional if using GCS for reports)

4. **Run locally**:
   ```bash
   streamlit run app/main.py
   ```
