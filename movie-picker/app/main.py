import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.components import create_mood_selector, display_recommendations
from src.mood_classifier import classify_mood
from src.recommend import get_recommendations

# Configure page
st.set_page_config(
    page_title="ReelFeel - Movie Picker",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1em;
    }
    .subtitle {
        font-size: 1.2em;
        text-align: center;
        color: #666;
        margin-bottom: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎬 ReelFeel</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the perfect movie for your mood</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    num_recommendations = st.slider("Number of recommendations", 1, 10, 5)
    st.divider()
    st.info("💡 Describe your mood or current situation, and ReelFeel will recommend movies for you!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("How are you feeling?")
    user_mood = st.text_area(
        "Describe your mood or what you're in the mood for:",
        placeholder="e.g., I'm feeling adventurous and want something exciting...",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Quick Options")
    quick_moods = st.selectbox(
        "Or choose a mood:",
        ["Custom", "Happy", "Sad", "Thrilled", "Relaxed", "Thoughtful"],
        label_visibility="collapsed"
    )

# Get recommendations
if user_mood or quick_moods != "Custom":
    if st.button("🔍 Get Recommendations", use_container_width=True):
        with st.spinner("Finding perfect movies for you..."):
            # Use quick mood if selected, otherwise use custom input
            mood_input = quick_moods if quick_moods != "Custom" else user_mood
            
            # Placeholder for recommendations (integrate your actual logic)
            st.success(f"Found {num_recommendations} recommendations for: {mood_input}")
            
            # Display recommendations
            st.subheader("📽️ Recommended Movies")
            for i in range(num_recommendations):
                with st.expander(f"Recommendation {i+1}", expanded=i==0):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("**Title:** Movie Title Here")
                        st.write("**Genre:** Action, Adventure")
                        st.write("**Why:** This matches your mood because...")
                    with col2:
                        st.metric("Rating", "8.5/10")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; padding: 2em 0;'>
    <small>Made with 🎬 by ReelFeel | Discover movies that match your mood</small>
    </div>
""", unsafe_allow_html=True)
