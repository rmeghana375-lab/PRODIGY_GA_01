import streamlit as st
from transformers import pipeline


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Text Generator",
    page_icon="✨",
    layout="wide"
)


# ---------------- STYLE ----------------

st.markdown(
"""
<style>

.stApp {
    background: #0f0f0f;
}


/* Hide default elements */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* Center title */

.main-title {

    text-align:center;
    font-size:42px;
    font-weight:600;
    margin-top:80px;
    color:white;

}


.sub-title {

    text-align:center;
    font-size:18px;
    color:#9ca3af;

}


/* Chat bubbles */


.user-box {

    background:#2f2f2f;
    color:white;

    padding:16px;
    border-radius:18px;

    margin-left:25%;
    margin-top:15px;

}


.ai-box {

    background:#171717;
    color:white;

    border:1px solid #333;

    padding:16px;
    border-radius:18px;

    margin-right:25%;
    margin-top:15px;

}


</style>
""",
unsafe_allow_html=True
)



# ---------------- SIDEBAR ----------------


with st.sidebar:


    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.messages=[]

        st.rerun()


    st.divider()

    st.caption(
        "Model"
    )

    st.write(
        "GPT-2 Transformer"
    )



# ---------------- MODEL ----------------


@st.cache_resource
def load_model():


    model=pipeline(

        "text-generation",

        model="gpt2-medium"

    )


    return model



generator=load_model()



# ---------------- SESSION ----------------


if "messages" not in st.session_state:


    st.session_state.messages=[]




# ---------------- EMPTY SCREEN ----------------


if len(st.session_state.messages)==0:


    st.markdown(

        """
        <div class='main-title'>
        How can I help you today?
        </div>

        <div class='sub-title'>
        Start typing below to generate intelligent text
        </div>

        """,

        unsafe_allow_html=True

    )



# ---------------- SHOW CHAT ----------------


for msg in st.session_state.messages:


    if msg["role"]=="user":


        st.markdown(

            f"""
            <div class='user-box'>
            {msg['content']}
            </div>
            """,

            unsafe_allow_html=True

        )



    else:


        st.markdown(

            f"""
            <div class='ai-box'>
            {msg['content']}
            </div>
            """,

            unsafe_allow_html=True

        )




# ---------------- INPUT ----------------


prompt=st.chat_input(

    "Ask anything..."

)



if prompt:


    st.session_state.messages.append(

        {
            "role":"user",
            "content":prompt
        }

    )


    with st.spinner(
        "Generating response..."
    ):


        output=generator(

            prompt,

            max_new_tokens=100,

            temperature=0.75,

            top_p=0.95,

            repetition_penalty=1.15,

            do_sample=True

        )


        answer=output[0]["generated_text"]



    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer
        }

    )


    st.rerun()