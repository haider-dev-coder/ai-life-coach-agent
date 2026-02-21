import sys, os
import streamlit as st
from datetime import datetime, timedelta
from urllib.parse import quote

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent_setup import agent_executor
from utils.json_parser import parse_agent_output
from agent.memory_manager import load_habits, save_habit
from utils.time_extractor import extract_time_from_task, get_reminder_datetime

# Page config
st.set_page_config(
    page_title="AI Life Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .tip-card {
        background: #f0f2f6;
        padding: 15px;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        margin: 10px 0;
        color: #1f1f1f;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px;
        font-size: 18px;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/goal.png", width=80)
    st.title("⚙️ Settings")
    user_id = st.text_input("👤 Username", "guest")
    
    st.markdown("---")
    st.subheader("📊 Your Stats")
    habit_memory = load_habits(user_id)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Days Active", len(habit_memory))
    with col2:
        st.metric("Plans Created", len(habit_memory))
    
    # Show latest reminders
    if 'reminders' in st.session_state and st.session_state.reminders:
        st.markdown("---")
        st.subheader("⏰ Today's Reminders")
        for reminder in st.session_state.reminders:
            st.info(f"🔔 {reminder['time']} - {reminder['text'][:50]}...")
    
    st.markdown("---")
    st.subheader("🎯 Quick Actions")
    if st.button("🗑️ Clear History"):
        save_habit(user_id, {})
        st.success("History cleared!")
        st.rerun()

    if st.button("📜 View History"):
        st.session_state.show_history = not st.session_state.get('show_history', False)

# Main content
st.markdown('<h1 class="main-header">🎯 AI Life Coach & Habit Tracker</h1>', unsafe_allow_html=True)

# Welcome message
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.info(f"👋 Welcome back, **{user_id}**! Ready to plan your day?")

# Input section
st.markdown("### 💭 Tell me about your goals or habits")
user_input = st.text_area(
    "",
    placeholder="Example: I want to improve my diet, exercise more, or manage stress better...",
    height=150,
    key="user_input"
)

# Initialize session state
if 'current_plan' not in st.session_state:
    st.session_state.current_plan = None

# Generate button
col1, col2, col3 = st.columns([1,1,1])
with col2:
    generate_btn = st.button("✨ Generate My Plan", use_container_width=True)

if generate_btn:
    if user_input.strip():
        # Pre-check for off-topic requests
        off_topic_keywords = ['joke', 'funny', 'story', 'job', 'career', 'weather', 'news', 'code', 'program']
        user_lower = user_input.lower()
        
        if any(keyword in user_lower for keyword in off_topic_keywords):
            st.error("⚠️ I am an AI Life Coach focused exclusively on health and wellness. I cannot help with jokes, entertainment, career advice, or unrelated topics.")
            st.info("💡 Please ask me about:\n- Diet and nutrition\n- Exercise and fitness\n- Sleep improvement\n- Stress management\n- Building healthy habits")
        else:
            with st.spinner("🤖 AI is crafting your personalized plan..."):
                try:
                    response = agent_executor.invoke({"input": user_input})
                    parsed = parse_agent_output(response["output"])
                    
                    if parsed:
                        # Extract reminders from tasks
                        reminders = []
                        for task in parsed.daily_plan:
                            time_str = extract_time_from_task(task)
                            if time_str:
                                reminder_dt = get_reminder_datetime(time_str)
                                reminders.append({
                                    'text': task,
                                    'time': time_str,
                                    'datetime': reminder_dt,
                                    'task': task
                                })
                        
                        st.session_state.reminders = reminders
                        st.session_state.current_plan = parsed
                        
                        # Save to memory
                        habit_memory[datetime.now().strftime("%Y-%m-%d %H:%M")] = {
                            "input": user_input,
                            "plan": parsed.daily_plan,
                            "tips": parsed.tips,
                            "progress": parsed.progress,
                            "reminders": reminders
                        }
                        save_habit(user_id, habit_memory)
                        st.rerun()
                    else:
                        st.error("❌ Could not parse response")
                        with st.expander("🔍 Show Raw Response"):
                            st.code(response["output"])
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter your goals or habits first!")

# Display plan if it exists
if st.session_state.current_plan:
    parsed = st.session_state.current_plan
    
    st.success("✅ Your personalized plan is ready!")
    
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["📋 Daily Plan", "📈 Progress", "💡 Tips"])
    
    with tab1:
        st.markdown("### 🎯 Your Daily Action Plan")
        for i, item in enumerate(parsed.daily_plan, 1):
            st.markdown(f"""
            <div class="tip-card">
                <strong>{i}.</strong> {item}
            </div>
            """, unsafe_allow_html=True)
        
        # Add to Calendar button
        st.markdown("---")
        from urllib.parse import quote
        from datetime import datetime, timedelta
        
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        
        # Format for Google Calendar: YYYYMMDD
        start_date = tomorrow.strftime("%Y%m%d")
        
        # Create events for each task with time
        calendar_events = []
        for i, task in enumerate(parsed.daily_plan, 1):
            time_str = extract_time_from_task(task)
            if time_str:
                # Has time - create individual event
                hour, minute = map(int, time_str.split(':'))
                start_datetime = f"{start_date}T{hour:02d}{minute:02d}00"
                end_datetime = f"{start_date}T{(hour+1):02d}{minute:02d}00"
                
                event_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote(f'Task {i}: {task[:30]}...')}&dates={start_datetime}/{end_datetime}&details={quote(task)}"
                calendar_events.append((time_str, event_url, task))
        
        if calendar_events:
            st.markdown("**📅 Add Tasks to Calendar:**")
            for time_str, url, task in calendar_events:
                st.markdown(f'<a href="{url}" target="_blank" style="text-decoration: none;"><button style="background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; margin: 5px 0; width: 100%;">📅 {time_str} - {task[:40]}...</button></a>', unsafe_allow_html=True)
        else:
            # Fallback: Add all as one event
            tasks_text = "\n".join([f"{i}. {task}" for i, task in enumerate(parsed.daily_plan, 1)])
            calendar_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote('Daily Health Plan')}&dates={start_date}T090000/{start_date}T100000&details={quote(tasks_text)}"
            st.markdown(f'<a href="{calendar_url}" target="_blank" style="text-decoration: none;"><button style="background: linear-gradient(120deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%;">📅 Add All Tasks to Google Calendar</button></a>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Progress Tracking")
        for item in parsed.progress:
            st.info(f"📈 {item}")
    
    with tab3:
        st.markdown("### 💡 Expert Tips")
        for i, item in enumerate(parsed.tips, 1):
            with st.expander(f"Tip #{i}", expanded=True):
                st.write(item)

# History viewer
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

if st.session_state.show_history and habit_memory:
    st.markdown("---")
    st.markdown("## 📜 Your History")
    
    for timestamp, data in sorted(habit_memory.items(), reverse=True):
        with st.expander(f"📅 {timestamp}", expanded=False):
            st.markdown("**Your Input:**")
            st.write(data.get('input', 'N/A'))
            
            if 'plan' in data:
                st.markdown("**Daily Plan:**")
                for i, item in enumerate(data['plan'], 1):
                    st.write(f"{i}. {item}")
                
                # Add to Calendar button for history
                tomorrow = datetime.now() + timedelta(days=1)
                date_str = tomorrow.strftime("%Y%m%d")
                tasks_text = "\n".join([f"{i}. {task}" for i, task in enumerate(data['plan'], 1)])
                calendar_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote(f'Plan from {timestamp}')}&dates={date_str}T090000Z/{date_str}T100000Z&details={quote(tasks_text)}"
                
                st.markdown(f'<a href="{calendar_url}" target="_blank" style="text-decoration: none;"><button style="background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; margin-top: 10px;">📅 Add to Calendar</button></a>', unsafe_allow_html=True)
            
            if 'tips' in data:
                st.markdown("**Tips:**")
                for tip in data['tips']:
                    st.write(f"💡 {tip}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Agent is Created By Haider </p>",
    unsafe_allow_html=True
)