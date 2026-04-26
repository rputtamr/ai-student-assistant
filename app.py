import streamlit as st

st.set_page_config(page_title="AI Student Assistant", page_icon="🎓", layout="wide")

# ---------------- INIT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "analytics" not in st.session_state:
    st.session_state.analytics = {
        "AI Courses": 0,
        "Study Tips": 0,
        "Campus Advice": 0,
        "Other": 0
    }

# ---------------- AI ENGINE ----------------
def get_topic(query):
    query = query.lower()
    if "course" in query or "ai" in query or "machine learning" in query or "python" in query:
        return "AI Courses"
    elif "study" in query or "exam" in query or "pomodoro" in query:
        return "Study Tips"
    elif "campus" in query or "club" in query or "network" in query:
        return "Campus Advice"
    else:
        return "Other"

def get_response(query):
    topic = get_topic(query)

    if topic == "AI Courses":
        return """📘 **AI Learning Path:**
- Python fundamentals
- Data Structures & Algorithms
- Machine Learning
- Deep Learning
- Real-world Projects

💡 Tip: Build projects early, not just theory."""

    elif topic == "Study Tips":
        return """📚 **Study Strategy:**
- Pomodoro technique (25 min focus blocks)
- Weekly revision cycles
- Practice past exams
- Active recall > passive reading

💡 Consistency beats last-minute study."""

    elif topic == "Campus Advice":
        return """🏫 **Campus Strategy:**
- Join at least 1 technical club
- Attend hackathons & workshops
- Build peer + mentor network
- Use university resources actively

💡 Networking creates opportunities."""

    else:
        return """🤖 I can help you with:
- AI/CS course guidance
- Study strategies
- Campus success tips

Try asking something specific!"""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🎓 AI Assistant")
    st.caption("EdPlus-style student tool")

    st.divider()

    st.write("### 💡 Quick Prompts")

    if st.button("📘 AI Courses"):
        msg = "Suggest AI courses"
        st.session_state.messages.append({"role": "user", "content": msg})
        st.session_state.messages.append({"role": "assistant", "content": get_response(msg)})
        st.session_state.analytics["AI Courses"] += 1
        st.rerun()

    if st.button("📚 Study Tips"):
        msg = "Give study tips"
        st.session_state.messages.append({"role": "user", "content": msg})
        st.session_state.messages.append({"role": "assistant", "content": get_response(msg)})
        st.session_state.analytics["Study Tips"] += 1
        st.rerun()

    if st.button("🏫 Campus Advice"):
        msg = "Campus advice"
        st.session_state.messages.append({"role": "user", "content": msg})
        st.session_state.messages.append({"role": "assistant", "content": get_response(msg)})
        st.session_state.analytics["Campus Advice"] += 1
        st.rerun()

    st.divider()

    # ---------------- ANALYTICS PANEL ----------------
    st.write("### 📊 Query Analytics")
    st.caption("What students ask most")

    total = sum(st.session_state.analytics.values())

    if total == 0:
        st.info("No queries yet. Start chatting!")
    else:
        for topic, count in st.session_state.analytics.items():
            pct = int((count / total) * 100) if total > 0 else 0
            st.write(f"**{topic}** — {count} queries ({pct}%)")
            st.progress(pct / 100)

        st.divider()
        top_topic = max(st.session_state.analytics, key=st.session_state.analytics.get)
        st.success(f"🔥 Most asked: **{top_topic}**")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.analytics = {
            "AI Courses": 0,
            "Study Tips": 0,
            "Campus Advice": 0,
            "Other": 0
        }
        st.rerun()

# ---------------- MAIN ----------------
st.title("💬 AI Student Assistant")
st.caption("A student experience prototype — EdPlus style")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    topic = get_topic(user_input)
    st.session_state.analytics[topic] += 1

    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()