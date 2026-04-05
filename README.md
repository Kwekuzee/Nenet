# NENet Northpreneurs Dashboard

An interactive analytics dashboard for the Northern Ghana Entrepreneurs Network (NENet) baseline assessment.

## Quick Start

### Option A — Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

### Option B — Deploy to Streamlit Cloud (free, shareable link)

1. Push this folder to a **GitHub repository** (public or private)
2. Go to https://share.streamlit.io
3. Click **"New app"** → select your repo → set `app.py` as the main file
4. Click **Deploy** — you get a public link like `https://yourapp.streamlit.app`

That's it. Anyone with the link can view the dashboard without installing anything.

---

### Option C — Deploy to Hugging Face Spaces (also free)

1. Create a Space at https://huggingface.co/new-space
2. Choose **Streamlit** as the SDK
3. Upload `app.py` and `requirements.txt`
4. Your app goes live at `https://huggingface.co/spaces/your-username/nenet-dashboard`

---

## Features

- 📊 **Overview** — Gender, business type, regional spread, revenue, business age
- 🏛 **Formalization** — GEPA, GEA, District Permit registration status + composite score
- 🌐 **Market & Export** — Export status, destinations, market reach, revenue vs export
- 🤝 **Support & Outreach** — Ranked support needs, discovery channels, gender disaggregation
- 🏭 **Sectors** — Industry distribution, activity categories, sector-revenue heatmap
