import streamlit as st
import requests
import random
import os

st.set_page_config(
    page_title="CineMatch · Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');
            
[data-testid="stSidebarCollapseButton"] {
        display: block !important;
        visibility: visible !important;
        z-index: 999999 !important;
        color: #E50914 !important; /* Netflix red to match your theme */
    }

    section[data-testid="stSidebar"][aria-expanded="false"] + div {
        display: block !important;
    } 

:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --card: #1c1c28;
    --accent: #e63946;
    --gold: #f4a261;
    --text: #f0eee8;
    --muted: #888899;
    --border: #2a2a3a;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* ── FIX: Do not hide the header, just make it transparent ── */
#MainMenu, footer { visibility: hidden; }
header { background-color: transparent !important; }

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Style the native Streamlit sidebar toggle so it's always visible ── */
[data-testid="collapsedControl"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important; /* Added z-index here too just in case */
}
[data-testid="collapsedControl"] svg {
    fill: var(--muted) !important;
}

/* ── Kill the "Press Enter to apply" tooltip/overlay on text inputs ── */
div[data-testid="stTextInput"] div[data-testid="InputInstructions"],
div[data-testid="stTextInput"] + div small,
div[data-baseweb="input"] ~ small,
small.st-emotion-cache-1gulkj5,
div[data-testid="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
}

/* ── Main content ── */
.main .block-container {
    max-width: 100% !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-top: 1.5rem !important;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    letter-spacing: 4px;
    color: var(--text);
    line-height: 1;
    margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    color: var(--muted);
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* ── Ready banner ── */
.ready-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(76, 175, 125, 0.08);
    border: 1px solid rgba(76, 175, 125, 0.25);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 2rem;
}
.rb-icon { font-size: 1.8rem; }
.rb-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 2px;
    color: #4caf7d;
    display: block;
    line-height: 1.3;
}
.rb-sub {
    font-size: 0.82rem;
    color: var(--muted);
    margin-top: 2px;
    display: block;
}

/* ── Movie cards ── */
.movie-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(230,57,70,0.15);
}
.movie-poster {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    background: #1a1a28;
}
.movie-info { padding: 0.85rem 1rem; }
.movie-title-card {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 1px;
    color: var(--text);
    margin: 0 0 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.movie-meta {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex-wrap: wrap;
}
.badge {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 7px;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.5px;
}
.badge-accent {
    background: rgba(230,57,70,0.15);
    border-color: var(--accent);
    color: var(--accent);
}
.star { color: var(--gold); font-size: 0.8rem; }
.overview {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.5rem;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 2px;
    border-left: 4px solid var(--accent);
    padding-left: 0.75rem;
    margin-bottom: 1.2rem;
}

/* ── Sidebar widget labels ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: var(--muted) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    padding: 0.5rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
    margin-top: 0.3rem !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Text inputs ── */
div[data-testid="stTextInput"] input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

.api-status-ok  { font-size: 0.78rem; color: #4caf7d; margin-top: 0.5rem; }
.api-status-bad { font-size: 0.78rem; color: var(--accent); margin-top: 0.5rem; }

/* ── Empty / error states ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--muted);
}
.empty-icon { font-size: 4rem; margin-bottom: 1rem; }
.empty-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 2px;
}
.empty-sub { font-size: 0.85rem; margin-top: 0.5rem; }

.poster-placeholder {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1a28 0%, #13131a 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}

.fetch-warn {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 4px solid var(--gold);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    font-size: 0.88rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
}
.fetch-warn strong { color: var(--text); }
</style>
""", unsafe_allow_html=True)

TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE  = "https://image.tmdb.org/t/p/w500"

GENRE_MAP = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
    "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402,
    "Mystery": 9648, "Romance": 10749, "Science Fiction": 878,
    "Thriller": 53, "War": 10752, "Western": 37,
}

SORT_OPTIONS = {
    "Popularity ↓": "popularity.desc",
    "Rating ↓": "vote_average.desc",
    "Release Date ↓": "release_date.desc",
    "Release Date ↑": "release_date.asc",
}

if "api_key" not in st.session_state:
    st.session_state["api_key"] = os.environ.get("TMDB_API_KEY", "")

def fetch(endpoint, params={}):
    key = st.session_state.get("api_key", "")
    if not key:
        return None
    try:
        r = requests.get(
            f"{TMDB_BASE}/{endpoint}",
            params={"api_key": key, "language": "en-US", **params},
            timeout=8,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def poster_url(path):
    return f"{IMG_BASE}{path}" if path else None

def stars(rating):
    filled = round(rating / 2)
    return "★" * filled + "☆" * (5 - filled)

def movie_card_html(m):
    title    = m.get("title", "Unknown")
    overview = m.get("overview", "No overview available.")
    year     = (m.get("release_date") or "")[:4] or "N/A"
    rating   = m.get("vote_average", 0)
    poster   = poster_url(m.get("poster_path"))
    img_html = (
        f'<img class="movie-poster" src="{poster}" alt="{title}">'
        if poster else
        '<div class="poster-placeholder">🎬</div>'
    )
    return f"""
    <div class="movie-card">
        {img_html}
        <div class="movie-info">
            <div class="movie-title-card" title="{title}">{title}</div>
            <div class="movie-meta">
                <span class="badge">{year}</span>
                <span class="star">{stars(rating)}</span>
                <span class="badge badge-accent">{rating:.1f}</span>
            </div>
            <div class="overview">{overview}</div>
        </div>
    </div>"""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("##### 🔑 TMDB API KEY")

    typed_key = st.text_input(
        "Paste your TMDB v3 API key",
        type="password",
        placeholder="e.g. a1b2c3d4e5f6...",
    )

    if st.button("💾 Save Key"):
        if typed_key.strip():
            st.session_state["api_key"] = typed_key.strip()
            st.success("✔ Key saved! You're good to go.")
        else:
            st.warning("Please paste a key first.")

    if st.session_state.get("api_key"):
        st.markdown('<p class="api-status-ok">✔ API key active</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="api-status-bad">✘ No key yet</p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 🎛️ Filters")

    genres_selected = st.multiselect(
        "Genres",
        options=list(GENRE_MAP.keys()),
        default=["Action", "Drama"],
    )

    col1, col2 = st.columns(2)
    with col1:
        year_from = st.number_input("From", min_value=1900, max_value=2025, value=2000, step=1)
    with col2:
        year_to = st.number_input("To", min_value=1900, max_value=2025, value=2025, step=1)

    min_rating = st.slider("Min Rating", 0.0, 10.0, 6.0, 0.5)
    sort_by    = st.selectbox("Sort By", list(SORT_OPTIONS.keys()))

    st.markdown("---")
    st.markdown("##### 🔍 Search")

    search_query = st.text_input(
        "Movie title",
        placeholder="e.g. Inception…",
    )

    get_recs = st.button("🎬 Get Recommendations")

    st.markdown("---")
    st.markdown(
        '<div style="color:#444;font-size:0.72rem;text-align:center;">'
        'Data by <a href="https://www.themoviedb.org" target="_blank" '
        'style="color:#e63946;text-decoration:none;">TMDB</a></div>',
        unsafe_allow_html=True,
    )

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1 class="hero-title">Cine<span>Match</span></h1>
  <p class="hero-sub">Discover your next favourite film</p>
</div>
""", unsafe_allow_html=True)

# ── No key ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("api_key"):
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🔑</div>
        <div class="empty-text">One Step Away</div>
        <div class="empty-sub">
            Paste your TMDB API key in the sidebar and click <strong>Save Key</strong> to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Ready banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ready-banner">
    <div class="rb-icon">🎉</div>
    <div>
        <span class="rb-title">You're all set — search freely!</span>
        <span class="rb-sub">Pick genres & filters in the sidebar, search by title, or just hit Get Recommendations.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Fetch ──────────────────────────────────────────────────────────────────────
movies = []
fetch_failed = False

if search_query:
    data = fetch("search/movie", {"query": search_query, "page": 1})
    if data:
        movies = data.get("results", [])
        st.session_state["movies"] = movies
        st.session_state["mode_label"] = f'SEARCH · "{search_query.upper()}"'
    else:
        fetch_failed = True

elif get_recs or "movies" not in st.session_state:
    genre_ids = ",".join(str(GENRE_MAP[g]) for g in genres_selected) if genres_selected else ""
    params = {
        "sort_by": SORT_OPTIONS[sort_by],
        "vote_average.gte": min_rating,
        "primary_release_date.gte": f"{year_from}-01-01",
        "primary_release_date.lte": f"{year_to}-12-31",
        "vote_count.gte": 100,
        "page": random.randint(1, 5),
    }
    if genre_ids:
        params["with_genres"] = genre_ids

    data = fetch("discover/movie", params)
    if data:
        movies = data.get("results", [])
        st.session_state["movies"] = movies
        st.session_state["mode_label"] = "RECOMMENDED FOR YOU"
    else:
        fetch_failed = True

else:
    movies = st.session_state.get("movies", [])

if fetch_failed:
    st.markdown("""
    <div class="fetch-warn">
        ⚠️ <strong>Could not load movies.</strong>
        Make sure you're using the <strong>v3 API Key</strong> from TMDB (32 characters).
        Re-paste it in the sidebar and click <strong>Save Key</strong>.
    </div>
    """, unsafe_allow_html=True)

# ── Grid ───────────────────────────────────────────────────────────────────────
mode_label = st.session_state.get("mode_label", "RECOMMENDED FOR YOU")

if movies:
    st.markdown(f'<div class="section-label">{mode_label}</div>', unsafe_allow_html=True)
    cols = st.columns(5, gap="medium")
    for i, movie in enumerate(movies[:20]):
        with cols[i % 5]:
            st.markdown(movie_card_html(movie), unsafe_allow_html=True)
elif not fetch_failed:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎞️</div>
        <div class="empty-text">No movies found</div>
        <div class="empty-sub">Adjust your filters or hit "Get Recommendations"</div>
    </div>
    """, unsafe_allow_html=True)