import streamlit as st 
from groq import Groq 
from dotenv import load_dotenv 
from reportlab.lib.pagesizes import A4 
from reportlab.pdfgen import canvas 
from reportlab.lib.utils import simpleSplit 
import os 
import io 
# ============================================================ 
# LOAD ENVIRONMENT VARIABLES 
# ============================================================ 
load_dotenv() 
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
 
 
# ============================================================ 
# PAGE CONFIGURATION 
# ============================================================ 
 
st.set_page_config( 
    page_title="Debate Partner Bot", 
    page_icon=" ", 
    layout="centered" 
) 
 
 
# ============================================================ 
# CUSTOM CSS 
# ============================================================ 
 
st.markdown(""" 
<style> 
 
.main-title { 
    text-align: center; 
    font-size: 42px; 
    font-weight: bold; 
} 
 
.subtitle { 
    text-align: center; 
    color: gray; 
    font-size: 18px; 
    margin-bottom: 30px; 
} 
 
.user-message { 
    background-color: #E3F2FD; 
    padding: 15px; 
    border-radius: 12px; 
    margin: 10px 0; 
} 
 
.ai-message { 
    background-color: #F1F1F1; 
    padding: 15px; 
    border-radius: 12px; 
    margin: 10px 0; 
} 
 
.summary-box { 
    background-color: #F8F9FA; 
    padding: 20px; 
    border-radius: 12px; 
    border: 1px solid #DDDDDD; 
} 
 
</style> 
""", unsafe_allow_html=True) 
 
 
# ============================================================ 
# CHECK API KEY 
# ============================================================ 
 
if not GROQ_API_KEY: 
 
    st.error( 
        " GROQ_API_KEY not found. " 
        "Please create a .env file and add your Groq API key." 
    ) 
 
    st.code( 
        "GROQ_API_KEY=your_groq_api_key_here" 
    ) 
 
    st.stop() 
 
 
# ============================================================ 
# GROQ CLIENT 
# ============================================================ 
 
client = Groq( 
    api_key=GROQ_API_KEY 
) 
 
 
# ============================================================ 
# SESSION STATE 
# ============================================================ 
 
if "debate_started" not in st.session_state: 
    st.session_state.debate_started = False 
 
if "conversation" not in st.session_state: 
    st.session_state.conversation = [] 
 
if "topic" not in st.session_state: 
    st.session_state.topic = "" 
 
if "style" not in st.session_state: 
    st.session_state.style = "Formal" 
 
if "summary" not in st.session_state: 
    st.session_state.summary = "" 
 
 
# ============================================================ 
# TITLE 
# ============================================================ 
 
st.markdown( 
    '<div class="main-title"> Debate Partner Bot</div>', 
    unsafe_allow_html=True 
) 
 
st.markdown( 
    '<div class="subtitle">' 
    'Practice arguments. Think critically. Improve communication.' 
    '</div>', 
    unsafe_allow_html=True 
) 
 
 
# ============================================================ 
# START SCREEN 
# ============================================================ 
 
if not st.session_state.debate_started: 
 
    st.subheader(" Start a Debate") 
 
    topic = st.text_input( 
        "Debate Topic", 
        placeholder="Example: Should AI replace human jobs?" 
    ) 
 
    style = st.selectbox( 
        "Choose Debate Style", 
        [ 
            "Formal", 
            "Casual", 
            "Academic", 
            "Friendly" 
        ] 
    ) 
 
    if st.button( 
        " Start Debate", 
        use_container_width=True 
    ): 
 
        if not topic.strip(): 
 
            st.warning( 
                "Please enter a debate topic." 
            ) 
 
        else: 
 
            st.session_state.topic = topic 
            st.session_state.style = style 
            st.session_state.debate_started = True 
            st.session_state.conversation = [] 
            st.session_state.summary = "" 
 
            st.rerun() 
 
 
# ============================================================ 
# DEBATE SCREEN 
# ============================================================ 
 
else: 
 
    st.success( 
        f"Debate Topic: {st.session_state.topic}" 
    ) 
 
    st.info( 
        f"Debate Style: {st.session_state.style}" 
    ) 
 
    st.markdown( 
        "** Rule:** The AI will always take the " 
        "opposite position from you." 
    ) 
 
 
    # ======================================================== 
    # DISPLAY CHAT HISTORY 
    # ======================================================== 
 
    for message in st.session_state.conversation: 
 
        if message["role"] == "user": 
 
            st.markdown( 
                f""" 
                <div class="user-message"> 
                <b> You:</b><br> 
                {message["content"]} 
                </div> 
                """, 
                unsafe_allow_html=True 
            ) 
 
        else: 
 
            st.markdown( 
                f""" 
                <div class="ai-message"> 
                <b> AI:</b><br> 
                {message["content"]} 
                </div> 
                """, 
                unsafe_allow_html=True 
            ) 
 
 
    # ======================================================== 
    # USER INPUT 
    # ======================================================== 
 
    user_message = st.chat_input( 
        "Enter your argument..." 
    ) 
 
 
    if user_message: 
 
        st.session_state.conversation.append({ 
            "role": "user", 
            "content": user_message 
        }) 
 
 
        # ==================================================== 
        # SYSTEM PROMPT 
        # ==================================================== 
 
        system_prompt = f""" 
 
You are an AI Debate Partner. 
 
You are debating with the user. 
 
Debate Topic: 
{st.session_state.topic} 
 
Debate Style: 
{st.session_state.style} 
 
 
YOUR MAIN ROLE: 
 
Always take the opposite position 
from the user's argument. 
 
 
RULES: 
 
1. Never blindly agree with the user. 
 
2. Analyze the user's argument carefully. 
 
3. Give a logical counterargument. 
 
4. Keep your response concise and engaging. 
 
5. Give examples when useful. 
 
6. Be respectful and professional. 
 
7. Never insult the user. 
 
8. If the user's argument is weak, 
   explain why it is weak. 
 
9. If the user's argument is strong, 
   briefly acknowledge its strength, 
   but still provide a counterargument. 
 
10. Avoid repeating previous arguments. 
 
11. Encourage critical thinking. 
 
12. Stay focused on the debate topic. 
 
13. Follow the selected debate style. 
 
""" 
 
 
        # ==================================================== 
        # PREPARE MESSAGES 
        # ==================================================== 
 
        messages = [ 
            { 
                "role": "system", 
                "content": system_prompt 
            } 
        ] 
 
        messages.extend( 
            st.session_state.conversation 
        ) 
 
 
        # ==================================================== 
        # CALL GROQ 
        # ==================================================== 
 
        try: 
 
            with st.spinner( 
                " AI is thinking..." 
            ): 
 
               response = client.chat.completions.create( 
 
                    model="openai/gpt-oss-120b", 
 
                    messages=messages, 
 
                    temperature=0.7, 
 
                    max_tokens=500
                 )
            ai_response = ( 
                response 
                .choices[0] 
                .message 
                .content 
            ) 
 
 
            st.session_state.conversation.append({ 
                "role": "assistant", 
                "content": ai_response 
            }) 
 
            st.rerun() 
 
 
        except Exception as e: 
 
            st.session_state.conversation.pop() 
 
            st.error( 
                f" Groq API Error: {e}" 
            ) 
 
 
    # ======================================================== 
    # END DEBATE 
    # ======================================================== 
 
    st.divider() 
 
    col1, col2 = st.columns(2) 
 
 
    with col1: 
 
        if st.button( 
            " End Debate", 
            use_container_width=True 
        ): 
 
            if len( 
                st.session_state.conversation 
            ) == 0: 
 
                st.warning( 
                    "Please have at least one argument " 
                    "before ending the debate." 
                ) 
 
            else: 
 
                debate_text = "" 
 
                for message in ( 
                    st.session_state.conversation 
                ): 
 
                    if message["role"] == "user": 
 
                        debate_text += ( 
                            "USER: " 
                            + message["content"] 
                            + "\n\n" 
                        ) 
 
                    else: 
 
                        debate_text += ( 
                            "AI: " 
                            + message["content"] 
                            + "\n\n" 
                        ) 
 
 
                summary_prompt = f""" 
 
You are a professional debate evaluator. 
 
Debate Topic: 
{st.session_state.topic} 
 
Debate Style: 
{st.session_state.style} 
 
 
Complete Debate: 
 
{debate_text} 
 
 
Create a neutral professional debate summary. 
 
Include these sections: 
 
1. Main Arguments by the User 
 
2. Main Counterarguments by the AI 
 
3. Strongest Point from the User 
 
4. Strongest Point from the AI 
 
5. Areas Where the User Could Improve 
 
6. Neutral Conclusion 
 
 
IMPORTANT: 
 
Do not declare a winner. 
 
Do not favor either side. 
 
Keep the evaluation balanced, 
professional, and useful for learning. 
 
""" 
 
 
                try: 
 
                    with st.spinner( 
                        " Generating neutral summary..." 
                    ): 
 
                        summary_response = ( 
                            client 
                            .chat 
                            .completions 
                            .create( 
 
                                model= 
                                "openai/gpt-oss-120b", 
 
                                messages=[ 
 
                                    { 
                                        "role": "system", 
 
                                        "content": 
                                        "You are a neutral professional debate evaluator." 
                                    }, 
 
                                    { 
                                        "role": "user", 
 
                                        "content": 
                                        summary_prompt 
                                    } 
 
                                ], 
 
                                temperature=0.4, 
 
                                max_tokens=1000 
 
                            ) 
                        ) 
 
 
                    st.session_state.summary = ( 
                        summary_response 
                        .choices[0] 
                        .message 
                        .content 
                    ) 
 
 
                except Exception as e: 
 
                    st.error( 
                        f" Summary generation failed: {e}" 
                    ) 
 
 
    with col2: 
 
        if st.button( 
            " New Debate", 
            use_container_width=True 
        ): 
 
            st.session_state.debate_started = False 
            st.session_state.conversation = [] 
            st.session_state.topic = "" 
            st.session_state.summary = "" 
 
            st.rerun() 
 
 
# ============================================================ 
# SHOW SUMMARY 
# ============================================================ 
 
if st.session_state.summary: 
 
    st.divider() 
 
    st.subheader( 
        " Neutral Debate Summary" 
    ) 
 
    st.markdown( 
        f""" 
        <div class="summary-box"> 
        {st.session_state.summary} 
        </div> 
        """, 
        unsafe_allow_html=True 
    ) 
 
 
    # ======================================================== 
    # CREATE PDF 
    # ======================================================== 
 
    def create_pdf(): 
 
        buffer = io.BytesIO() 
 
        pdf = canvas.Canvas( 
            buffer, 
            pagesize=A4 
        ) 
 
        width, height = A4 
 
        y = height - 50 
 
 
        pdf.setFont( 
            "Helvetica-Bold", 
            20 
        ) 
 
        pdf.drawString( 
            50, 
            y, 
            "Debate Partner Bot" 
        ) 
 
        y -= 35 
 
 
        pdf.setFont( 
            "Helvetica", 
            11 
        ) 
 
        pdf.drawString( 
            50, 
            y, 
            f"Topic: {st.session_state.topic}" 
        ) 
 
        y -= 20 
 
        pdf.drawString( 
            50, 
            y, 
            f"Style: {st.session_state.style}" 
        ) 
 
        y -= 35 
 
 
        pdf.setFont( 
            "Helvetica-Bold", 
            14 
        ) 
 
        pdf.drawString( 
            50, 
            y, 
            "Debate Transcript" 
        ) 
 
        y -= 25 
 
 
        pdf.setFont( 
            "Helvetica", 
            10 
        ) 
 
 
        for message in ( 
            st.session_state.conversation 
        ): 
 
            if message["role"] == "user": 
 
                text = ( 
                    "You: " 
                    + message["content"] 
                ) 
 
            else: 
 
                text = ( 
                    "AI: " 
                    + message["content"] 
                ) 
 
 
            lines = simpleSplit( 
                text, 
                "Helvetica", 
                10, 
                width - 100 
            ) 
 
 
            for line in lines: 
 
                if y < 50: 
 
                    pdf.showPage() 
 
                    y = height - 50 
 
                    pdf.setFont( 
                        "Helvetica", 
                        10 
                    ) 
 
 
                pdf.drawString( 
                    50, 
                    y, 
                    line 
                ) 
 
                y -= 15 
 
 
            y -= 10 
 
 
        if y < 150: 
 
            pdf.showPage() 
 
            y = height - 50 
 
 
        pdf.setFont( 
            "Helvetica-Bold", 
            14 
        ) 
 
        pdf.drawString( 
            50, 
            y, 
            "Neutral Summary" 
        ) 
 
        y -= 25 
 
 
        pdf.setFont( 
            "Helvetica", 
            10 
        ) 
 
 
        summary_lines = simpleSplit( 
            st.session_state.summary, 
            "Helvetica", 
            10, 
            width - 100 
        ) 
 
 
        for line in summary_lines: 
 
            if y < 50: 
 
                pdf.showPage() 
 
                y = height - 50 
 
                pdf.setFont( 
                    "Helvetica", 
                    10 
                ) 
 
 
            pdf.drawString( 
                50, 
                y, 
                line 
            ) 
 
            y -= 15 
 
 
        pdf.save() 
 
        buffer.seek(0) 
 
        return buffer 
 
 
    # ======================================================== 
    # DOWNLOAD BUTTON 
    # ======================================================== 
 
    pdf_file = create_pdf() 
 
 
    st.download_button( 
        label=" Download Debate as PDF", 
        data=pdf_file, 
        file_name="debate_partner_transcript.pdf", 
        mime="application/pdf", 
        use_container_width=True 
    )