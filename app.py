import streamlit as st
import requests
import sqlite3
from datetime import datetime


# Database setup
def init_db():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS interactions 
                 (user_id TEXT, message TEXT, response TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

# Function to fetch AI-generated response using Hugging Face API
def get_ai_response(user_input):
    API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Use a public model
    headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_TOKEN"}  # Replace with your token
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": user_input})
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Store user interaction
def store_interaction(user_id, message, response):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO interactions (user_id, message, response, timestamp) VALUES (?, ?, ?, ?)", 
              (user_id, message, response, datetime.now()))
    conn.commit()
    conn.close()

# Streamlit UI with multiple pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Introduction", "Upstander Project", "Real Stories", "Strength Survey", "Personal Memories", "Scenario Generation", "Events & Resources"])

    # Page 0: Introduction
    if page == "Introduction":
        st.title("Welcome to the Upstander Program")
        st.image("images/banner.jpg", use_column_width=True)  # Add a banner image
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Learn how to respond to social situations with AI-driven stories and suggestions.")
        st.write("### Get Started:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Learn About Upstanders"):
                page = "Upstander Project"  # Navigate to Page 1
        with col2:
            if st.button("Take the Strength Survey"):
                page = "Strength Survey"  # Navigate to Page 3
        st.markdown('</div>', unsafe_allow_html=True)

    # Page 1: Upstander Project
    elif page == "Upstander Project":
        st.title("Upstander Project")
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Learn about the history and importance of upstanders.")
        
        with st.expander("What is an Upstander?"):
            st.write("An upstander is someone who takes action to support others in difficult situations.")
        
        with st.expander("Take the Upstander Quiz"):
            st.write("Test your knowledge of upstanders!")
            question = st.radio("What does it mean to be an upstander?", ["Someone who ignores problems", "Someone who takes action to help others", "Someone who causes problems"])
            if st.button("Submit Quiz"):
                if question == "Someone who takes action to help others":
                    st.success("Correct! An upstander takes action to help others.")
                else:
                    st.error("Incorrect. Try again!")
        st.markdown('</div>', unsafe_allow_html=True)

    # Page 2: Real Stories
    elif page == "Real Stories":
        st.title("Real Stories")
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Read real stories from the Human Rights Museum.")
        
        # Fetch stories from the database
        conn = sqlite3.connect("upstander_stories.db")
        c = conn.cursor()
        c.execute("SELECT title, story FROM upstander_stories")
        stories = c.fetchall()
        conn.close()
        
        for title, story in stories:
            with st.expander(title):
                st.write(story)
        st.markdown('</div>', unsafe_allow_html=True)

    # Page 3: Strength Survey
    elif page == "Strength Survey":
        st.title("Personal Strength Survey")
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Discover your strengths and how to use them.")
        
        with st.form("strength_survey"):
            st.write("How do you react in stressful situations?")
            reaction = st.radio("Choose one:", ["Calmly", "Anxiously", "With anger"])
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                st.write(f"Your reaction: {reaction}")
                st.write("**Your top strength:** Empathy")  # Example result
        st.markdown('</div>', unsafe_allow_html=True)

    # Page 4: Personal Memories
    elif page == "Personal Memories":
        st.title("Personal Memories")
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Reflect on your own experiences and share your stories.")
        
        with st.form("share_story"):
            user_id = st.text_input("Enter your User ID:")
            story = st.text_area("Share your story:")
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                conn = sqlite3.connect("user_data.db")
                c = conn.cursor()
                c.execute("INSERT INTO interactions (user_id, message, response, timestamp) VALUES (?, ?, ?, ?)", 
                          (user_id, story, "N/A", datetime.now()))
                conn.commit()
                conn.close()
                st.success("Thank you for sharing your story!")
        
        st.subheader("Community Stories")
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        c.execute("SELECT user_id, message FROM interactions WHERE response = 'N/A'")
        user_stories = c.fetchall()
        conn.close()
        
        for user_id, story in user_stories:
            st.write(f"**User {user_id}:** {story}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Page 5: Scenario Generation
    elif page == "Scenario Generation":
        st.title("Scenario Generation")
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Get actionable steps for specific situations.")
        
        scenario = st.selectbox("Choose a scenario:", ["Bullying", "Workplace Harassment", "Public Discrimination"])
        if st.button("Get Advice"):
            with st.spinner("Generating advice..."):
                advice = get_ai_response(f"How to handle {scenario}?")
                st.write("**AI Advice:**", advice)
        st.markdown('</div>', unsafe_allow_html=True)

    # Page 6: Events & Resources
    elif page == "Events & Resources":
        st.title("Events & Resources")
        st.markdown('<div class="text-container">', unsafe_allow_html=True)
        st.write("Find upcoming events and emotional support resources.")
        
        st.subheader("Upcoming Events")
        st.write("1. Upstander Workshop - October 15, 2023")
        st.write("2. Human Rights Seminar - November 1, 2023")
        
        st.subheader("Resources")
        st.write("[Mental Health Hotline](https://example.com)")
        st.write("[Anti-Bullying Organization](https://example.com)")
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        © 2023 Upstander Program. All rights reserved. | 
        <a href="mailto:info@upstanderprogram.com" style="color: white;">Contact Us</a> | 
        <a href="https://example.com" style="color: white;">Privacy Policy</a>
    </div>
    """, unsafe_allow_html=True)

# Initialize database
init_db()

if __name__ == "__main__":
    main()