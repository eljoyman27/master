import html
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "maintenance.db"

st.set_page_config(
    page_title="Upkeep — Maintenance Manager",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def database_path() -> Path:
    return DB_PATH


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(database_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                year TEXT,
                make_model TEXT,
                notes TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                last_done TEXT,
                due_date TEXT,
                mileage INTEGER,
                due_mileage INTEGER,
                cost REAL DEFAULT 0,
                status TEXT DEFAULT 'Upcoming',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(asset_id) REFERENCES assets(id)
            )
            """
        )


def query(sql: str, params: tuple = ()) -> list[dict]:
    with get_db() as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def execute(sql: str, params: tuple = ()) -> None:
    with get_db() as conn:
        conn.execute(sql, params)
        conn.commit()


def days_until(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return (datetime.strptime(value, "%Y-%m-%d").date() - date.today()).days
    except ValueError:
        return None


def computed_status(value: str | None) -> str:
    days = days_until(value)
    if days is None:
        return "Upcoming"
    if days < 0:
        return "Overdue"
    if days <= 14:
        return "Due Soon"
    return "Upcoming"


def maintenance_rows() -> list[dict]:
    rows = query(
        """
        SELECT m.*, a.name AS asset_name, a.category
        FROM maintenance m
        JOIN assets a ON a.id = m.asset_id
        ORDER BY COALESCE(m.due_date, '9999-12-31'), m.created_at DESC
        """
    )
    for row in rows:
        row["status"] = computed_status(row.get("due_date"))
        row["days_until"] = days_until(row.get("due_date"))
    return rows


def money(value: float | int | None) -> str:
    return f"${float(value or 0):,.2f}"


def display_date(value: str | None) -> str:
    if not value:
        return "Not scheduled"
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%b %-d, %Y")
    except ValueError:
        return value


def status_badge(status: str) -> str:
    css_class = status.lower().replace(" ", "-")
    return f'<span class="status {css_class}">{status}</span>'


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');
    :root { --ink:#17221d; --muted:#6c756f; --line:#dfe3df; --paper:#f7f7f3; --sage:#5d7565; --orange:#c9623d; }
    .stApp { background: var(--paper); color: var(--ink); font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { background: #17241e; border-right: 0; }
    [data-testid="stSidebar"] * { color: #eef2ee; }
    [data-testid="stSidebar"] .stRadio label { padding: .45rem .5rem; border-radius: 8px; }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,.07); }
    [data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.1rem; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    h1, h2 { font-family: 'DM Serif Display', Georgia, serif !important; font-weight: 400 !important; color: var(--ink) !important; }
    h1 { font-size: 2.4rem !important; letter-spacing: -.03em; margin-bottom: .2rem !important; }
    h2 { font-size: 1.65rem !important; }
    h3 { color: var(--ink) !important; }
    .lede { color: var(--muted); font-size: 1.02rem; margin: -.35rem 0 1.8rem; }
    .section-title { font-family: 'DM Serif Display', Georgia, serif; font-size: 1.55rem; margin: 1.4rem 0 .7rem; }
    .task-row { background:#fff; border:1px solid var(--line); border-radius:12px; padding:1rem 1.1rem; margin:.55rem 0; }
    .task-top { display:flex; align-items:center; justify-content:space-between; gap:1rem; }
    .task-name { font-weight:700; color:var(--ink); }
    .task-meta { color:var(--muted); font-size:.88rem; margin-top:.28rem; }
    .status { display:inline-block; padding:.28rem .55rem; border-radius:999px; font-size:.72rem; font-weight:700; white-space:nowrap; }
    .status.overdue { color:#982f24; background:#fae3de; }
    .status.due-soon { color:#8a5a13; background:#f8edcf; }
    .status.upcoming { color:#386049; background:#e3eee6; }
    .asset-row { border-bottom:1px solid var(--line); padding:.78rem 0; }
    .asset-row:last-child { border-bottom:0; }
    .asset-name { font-weight:700; }
    .asset-meta { color:var(--muted); font-size:.84rem; }
    .empty { border:1px dashed #c9cec9; border-radius:12px; padding:2rem; text-align:center; color:var(--muted); background:#fff; }
    .brand { font-family:'DM Serif Display', Georgia, serif; font-size:1.65rem; margin:.35rem 0 .1rem; }
    .brand-sub { color:#aab7ae !important; font-size:.79rem; margin-bottom:1.5rem; }
    div.stButton > button, div.stFormSubmitButton > button { border-radius:9px; font-weight:700; }
    div.stFormSubmitButton > button[kind="primary"], div.stButton > button[kind="primary"] { background:var(--orange); border-color:var(--orange); }
    [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
    @media (max-width: 700px) { h1 { font-size:2rem !important; } .task-top { align-items:flex-start; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def page_header(title: str, subtitle: str) -> None:
    st.title(title)
    st.markdown(f'<p class="lede">{subtitle}</p>', unsafe_allow_html=True)


def dashboard() -> None:
    page_header("Good morning, Reinaldo", "Here’s what needs your attention around home.")
    rows = maintenance_rows()
    overdue = [row for row in rows if row["status"] == "Overdue"]
    due_soon = [row for row in rows if row["status"] == "Due Soon"]

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Due soon", len(due_soon))
    metric_2.metric("Overdue", len(overdue))
    metric_3.metric("Total spent", money(sum(float(row.get("cost") or 0) for row in rows)))

    schedule, assets_panel = st.columns([1.9, 1], gap="large")
    with schedule:
        st.markdown('<div class="section-title">Maintenance schedule</div>', unsafe_allow_html=True)
        filter_name = st.segmented_control("Schedule filter", ["All", "Due Soon", "Overdue"], default="All", label_visibility="collapsed")
        visible = rows if filter_name == "All" else [row for row in rows if row["status"] == filter_name]
        if not visible:
            st.markdown('<div class="empty">No maintenance tasks in this view.<br>Log a task to start your schedule.</div>', unsafe_allow_html=True)
        for row in visible[:8]:
            due = display_date(row.get("due_date"))
            detail = f"{row['asset_name']} · Due {due} · {money(row.get('cost'))}"
            st.markdown(
                f'<div class="task-row"><div class="task-top"><span class="task-name">{html.escape(row["task"])}</span>{status_badge(row["status"])}</div><div class="task-meta">{html.escape(detail)}</div></div>',
                unsafe_allow_html=True,
            )

    with assets_panel:
        st.markdown('<div class="section-title">Your assets</div>', unsafe_allow_html=True)
        assets = query("SELECT * FROM assets ORDER BY category, name")
        for asset in assets[:7]:
            descriptor = " · ".join(part for part in [asset.get("category"), asset.get("year"), asset.get("make_model")] if part)
            st.markdown(f'<div class="asset-row"><div class="asset-name">{html.escape(asset["name"])}</div><div class="asset-meta">{html.escape(descriptor)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Recent activity</div>', unsafe_allow_html=True)
    recent = sorted(rows, key=lambda item: item.get("created_at") or "", reverse=True)[:5]
    if recent:
        data = [{"Task": r["task"], "Asset": r["asset_name"], "Last done": display_date(r.get("last_done")), "Cost": money(r.get("cost"))} for r in recent]
        st.dataframe(pd.DataFrame(data), hide_index=True, width="stretch")
    else:
        st.markdown('<div class="empty">Your logged maintenance activity will appear here.</div>', unsafe_allow_html=True)


def assets_page() -> None:
    page_header("Assets", "Everything you maintain, all in one place.")
    tab_list, tab_add = st.tabs(["All assets", "Add asset"])
    with tab_list:
        assets = query("SELECT * FROM assets ORDER BY category, name")
        search = st.text_input("Search assets", placeholder="Search by name, category, or model")
        filtered = [a for a in assets if search.lower() in " ".join(str(v or "") for v in a.values()).lower()]
        if filtered:
            frame = pd.DataFrame(filtered)[["name", "category", "year", "make_model", "notes"]]
            frame.columns = ["Name", "Category", "Year", "Make / model", "Notes"]
            st.dataframe(frame, hide_index=True, width="stretch")
        else:
            st.info("No assets match your search.")

        with st.expander("Edit or remove an asset"):
            if not assets:
                st.caption("Add an asset first.")
            else:
                selected = st.selectbox("Choose asset", assets, format_func=lambda a: a["name"])
                with st.form("edit_asset"):
                    name = st.text_input("Name", selected["name"])
                    category = st.text_input("Category", selected["category"])
                    year = st.text_input("Year", selected.get("year") or "")
                    model = st.text_input("Make / model", selected.get("make_model") or "")
                    notes = st.text_area("Notes", selected.get("notes") or "")
                    save, remove = st.columns(2)
                    if save.form_submit_button("Save changes", type="primary", width="stretch"):
                        execute("UPDATE assets SET name=?, category=?, year=?, make_model=?, notes=? WHERE id=?", (name, category, year, model, notes, selected["id"]))
                        st.success("Asset updated.")
                        st.rerun()
                    if remove.form_submit_button("Delete asset", width="stretch"):
                        linked = query("SELECT COUNT(*) AS count FROM maintenance WHERE asset_id=?", (selected["id"],))[0]["count"]
                        if linked:
                            st.error("Delete this asset’s maintenance records first.")
                        else:
                            execute("DELETE FROM assets WHERE id=?", (selected["id"],))
                            st.success("Asset deleted.")
                            st.rerun()

    with tab_add:
        with st.form("add_asset", clear_on_submit=True):
            left, right = st.columns(2)
            name = left.text_input("Name *", placeholder="Nissan Frontier")
            category = right.selectbox("Category *", ["Vehicle", "Appliance", "Home System", "Tool", "Bike", "Home Project", "Other"])
            year = left.text_input("Year", placeholder="2010")
            model = right.text_input("Make / model", placeholder="Frontier V6 King Cab SE")
            notes = st.text_area("Notes", placeholder="Anything useful to remember…")
            if st.form_submit_button("Add asset", type="primary"):
                if not name.strip():
                    st.error("Name is required.")
                else:
                    execute("INSERT INTO assets (name, category, year, make_model, notes) VALUES (?, ?, ?, ?, ?)", (name.strip(), category, year, model, notes))
                    st.success(f"Added {name}.")


def maintenance_page() -> None:
    page_header("Maintenance log", "Plan upcoming work and keep a clear service history.")
    assets = query("SELECT * FROM assets ORDER BY name")
    tab_schedule, tab_log = st.tabs(["Schedule & history", "Log maintenance"])

    with tab_schedule:
        rows = maintenance_rows()
        filter_col, asset_col = st.columns(2)
        status_filter = filter_col.multiselect("Status", ["Overdue", "Due Soon", "Upcoming"], default=["Overdue", "Due Soon", "Upcoming"])
        asset_filter = asset_col.selectbox("Asset", ["All assets"] + [a["name"] for a in assets])
        visible = [r for r in rows if r["status"] in status_filter and (asset_filter == "All assets" or r["asset_name"] == asset_filter)]
        if visible:
            data = [{"ID": r["id"], "Asset": r["asset_name"], "Task": r["task"], "Due": display_date(r.get("due_date")), "Status": r["status"], "Mileage / hours": r.get("due_mileage"), "Cost": money(r.get("cost")), "Notes": r.get("notes") or ""} for r in visible]
            st.dataframe(pd.DataFrame(data), hide_index=True, width="stretch")
        else:
            st.info("No maintenance records match these filters.")

        if rows:
            with st.expander("Update or delete a record"):
                selected = st.selectbox("Choose record", rows, format_func=lambda r: f"{r['task']} — {r['asset_name']}")
                action = st.radio("Action", ["Mark completed", "Delete"], horizontal=True)
                if action == "Mark completed":
                    completed_on = st.date_input("Completed on", date.today())
                    cost = st.number_input("Final cost", min_value=0.0, value=float(selected.get("cost") or 0), step=10.0)
                    if st.button("Mark completed", type="primary"):
                        execute("UPDATE maintenance SET last_done=?, due_date=NULL, cost=?, status='Upcoming' WHERE id=?", (completed_on.isoformat(), cost, selected["id"]))
                        st.success("Maintenance marked completed.")
                        st.rerun()
                elif st.button("Delete record", type="primary"):
                    execute("DELETE FROM maintenance WHERE id=?", (selected["id"],))
                    st.success("Record deleted.")
                    st.rerun()

    with tab_log:
        if not assets:
            st.warning("Add an asset before logging maintenance.")
            return
        with st.form("log_maintenance", clear_on_submit=True):
            asset = st.selectbox("Asset *", assets, format_func=lambda a: a["name"])
            task = st.text_input("Task *", placeholder="Oil and filter change")
            left, right = st.columns(2)
            last_done = left.date_input("Last completed", value=None)
            due_date = right.date_input("Next due date", value=None)
            mileage = left.number_input("Current mileage / hours", min_value=0, value=None, step=100)
            due_mileage = right.number_input("Due mileage / hours", min_value=0, value=None, step=100)
            cost = left.number_input("Cost", min_value=0.0, value=0.0, step=10.0)
            notes = st.text_area("Notes")
            if st.form_submit_button("Save maintenance", type="primary"):
                if not task.strip():
                    st.error("Task is required.")
                else:
                    due_value = due_date.isoformat() if due_date else None
                    execute(
                        """INSERT INTO maintenance (asset_id, task, last_done, due_date, mileage, due_mileage, cost, status, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (asset["id"], task.strip(), last_done.isoformat() if last_done else None, due_value, mileage, due_mileage, cost, computed_status(due_value), notes),
                    )
                    st.success("Maintenance saved.")


init_db()
with st.sidebar:
    st.markdown('<div class="brand">Upkeep</div><div class="brand-sub">HOME & VEHICLE CARE</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", ["Overview", "Assets", "Maintenance Log"], label_visibility="collapsed")
    st.markdown("---")
    st.caption(f"Database: {DB_PATH.name}")

if page == "Overview":
    dashboard()
elif page == "Assets":
    assets_page()
else:
    maintenance_page()
