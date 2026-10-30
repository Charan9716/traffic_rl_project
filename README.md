# Traffic Signal RL Simulator

An interactive Streamlit dashboard for demonstrating four-way traffic-signal control. Users set the number of vehicles on the north, south, east, and west approaches, then observe a queue-aware controller choose the green phase and track every vehicle's delay.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app** and select that repository and branch.
3. Set the main file path to `streamlit_app.py`.
4. Deploy. The platform installs dependencies from `requirements.txt` automatically.

No secrets or external services are required. Keep any future `.streamlit/secrets.toml` or `.env` files out of Git; they are already ignored.

## Simulation rules

- The episode has a finite, user-selected vehicle count; it does not add traffic indefinitely.
- Each controller action opens either North/South or East/West.
- Cars that are not served stop and gain one waiting-time tick.
- Reward is the negative of the remaining queue plus current stopped-vehicle delay; reducing queues and delay improves it.
