"""Run with: streamlit run streamlit_app.py"""
from __future__ import annotations
import random
import time
import streamlit as st
from environment import DIRECTIONS, PHASES, TrafficEnv

st.set_page_config(page_title="Traffic RL Control Centre", page_icon="🚦", layout="wide")

def new_simulation(counts):
    env = TrafficEnv(service_rate=2, switch_penalty=1)
    env.reset(counts)
    st.session_state.env, st.session_state.running, st.session_state.history = env, False, []

if "env" not in st.session_state: new_simulation({d: 5 for d in DIRECTIONS})
if "running" not in st.session_state: st.session_state.running = False
if "history" not in st.session_state: st.session_state.history = []

st.title("🚦 Traffic Signal RL Simulator")
st.caption("A finite four-way intersection: configure vehicles, observe each decision, and clear every queue.")
with st.sidebar:
    st.header("Episode setup")
    st.caption("Counts remain fixed for the episode—no endless arrivals.")
    counts = {d: st.number_input(f"{d} approach", 0, 100, 5, key=f"count_{d}") for d in DIRECTIONS}
    left, right = st.columns(2)
    if left.button("Randomize", use_container_width=True):
        result = [0, 0, 0, 0]
        for _ in range(sum(counts.values())): result[random.randrange(4)] += 1
        for d, value in zip(DIRECTIONS, result): st.session_state[f"count_{d}"] = value
        st.rerun()
    if right.button("New episode", type="primary", use_container_width=True):
        new_simulation(counts); st.rerun()
    st.divider(); st.header("How the controller learns")
    st.write("The state is the four queue lengths. An action chooses **NS green** or **EW green**. Reward penalizes queue length and stopped time, so better actions reduce delay.")
    st.caption("This demo uses a transparent queue-aware policy; `choose_action()` can be replaced with the trained DQN action.")

env = st.session_state.env
def tick():
    if env.done:
        st.session_state.running = False; return
    action = env.choose_action()
    state, reward, metrics = env.step(action)
    st.session_state.history.append({"tick": env.step_number, "phase": PHASES[action], "reward": reward, **metrics, **dict(zip(DIRECTIONS, state))})

controls = st.columns([1, 1, 1, 5])
if controls[0].button("▶ Start" if not st.session_state.running else "❚❚ Pause", use_container_width=True, disabled=env.done): st.session_state.running = not st.session_state.running
if controls[1].button("Step once", use_container_width=True, disabled=env.done): tick()
if controls[2].button("Reset", use_container_width=True):
    new_simulation({d: st.session_state[f"count_{d}"] for d in DIRECTIONS}); st.rerun()

metrics = env.metrics()
phase = "No signal yet" if env.last_action is None else f"{PHASES[env.last_action]} green"
st.subheader(f"Signal: {phase}")
columns = st.columns(6)
for col, label, value in zip(columns, ("Queued", "Passed", "Moved now", "Stopped now", "Average wait", "Last reward"), (metrics["queued"], f"{metrics['passed']} / {metrics['total']}", metrics["moved_this_tick"], metrics["stopped_this_tick"], f"{metrics['average_wait']} ticks", metrics["reward"])): col.metric(label, value)

st.markdown("#### Vehicle tracking")
for card, direction in zip(st.columns(4), DIRECTIONS):
    queue = env.queues[direction]
    green = env.last_action is not None and direction in (("N", "S") if env.last_action == 0 else ("E", "W"))
    cars = " ".join(f"🚗 {v.vehicle_id} ({v.wait_time})" for v in queue[:8]) or "Clear"
    overflow = f" +{len(queue) - 8} more" if len(queue) > 8 else ""
    card.markdown(f"**{direction} approach {'🟢' if green else '🔴'}**\n\nQueue: **{len(queue)}**\n\n{cars}{overflow}\n\n*Each car displays its wait in ticks.*")

if env.last_moved or env.last_stopped:
    moved = ", ".join(v.vehicle_id for v in env.last_moved) or "None"
    stopped = ", ".join(v.vehicle_id for v in env.last_stopped[:12]) or "None"
    st.info(f"Last tick — passed: **{moved}**. Stopped and accrued one wait tick: **{stopped}**.")
if st.session_state.history:
    st.markdown("#### Live episode history")
    st.line_chart(st.session_state.history, x="tick", y=["queued", "average_wait"], color=["#ff4b4b", "#1f77b4"])
    st.dataframe(st.session_state.history[::-1], use_container_width=True, hide_index=True)
if env.done and metrics["total"]: st.success(f"Episode complete in {env.step_number} ticks. All {metrics['total']} vehicles passed; accumulated wait: {metrics['total_wait']} ticks.")
if st.session_state.running and not env.done:
    time.sleep(0.45); tick(); st.rerun()
