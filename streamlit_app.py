import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit_oauth import OAuth2Component
import os
import base64
import json

def app_logic():
    with st.sidebar:
        selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home","Warehouse","Query Optimization and Processing","Storage","Contact Us"],
        icons = ["house","gear","activity","snowflake","envelope"],
        menu_icon = "cast",
        default_index = 0,
        #orientation = "horizontal",
    )
    if selected == "Home":
        st.header('Snowflake Healthcare App')
        # Create a row layout
        c1, c2= st.columns(2)
        c3, c4= st.columns(2)

        with st.container():
            c1.write("c1")
            c2.write("c2")

        with st.container():
            c3.write("c3")
            c4.write("c4")

        with c1:
            chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
            st.area_chart(chart_data)
            
        with c2:
            chart_data = pd.DataFrame(np.random.randn(20, 3),columns=["a", "b", "c"])
            st.bar_chart(chart_data)

        with c3:
            chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
            st.line_chart(chart_data)

        with c4:
            chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
            st.line_chart(chart_data)
            
        
    if selected == "Warehouse":
        st.subheader(f"**You Have selected {selected}**")
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        my_cur = my_cnx.cursor()
        # run a snowflake query and put it all in a var called my_catalog
        my_cur.execute("select * from SWEATSUITS")
        my_catalog = my_cur.fetchall()
        st.dataframe(my_catalog)
        q1 = st.text_input('Write your query','')
        st.button('Run Query')
        if not q1:
            st.error('Please write a query')
        else:
            my_cur.execute(q1)
            my_catalog = my_cur.fetchall()
            st.dataframe(my_catalog)

        
    if selected == "Contact":
        st.subheader(f"**You Have selected {selected}**")


def main():

    # import logging
    # logging.basicConfig(level=logging.INFO)

    st.title("Google OIDC Example")
    st.write("This example shows how to use the raw OAuth2 component to authenticate with a Google OAuth2 and get email from id_token.")

    # create an OAuth2Component instance
    CLIENT_ID = "49158794855-p6f9i8dnq4m4a07ul2misue910a531a1.apps.googleusercontent.com"
    CLIENT_SECRET = "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"
    AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"


    if "auth" not in st.session_state:
        # create a button to start the OAuth2 flow
        oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
        result = oauth2.authorize_button(
            name="Continue with Google",
            icon="https://www.google.com.hk/favicon.ico",
            redirect_uri="https://cn-ops-asia-cloudscada.uc.r.appspot.com/",
            scope="openid email profile",
            key="google",
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=True,
            pkce='S256',
        )
        
        if result:
            st.write(result)
            # decode the id_token jwt and get the user's email address
            id_token = result["token"]["id_token"]
            # verify the signature is an optional step for security
            payload = id_token.split(".")[1]
            # add padding to the payload if needed
            payload += "=" * (-len(payload) % 4)
            payload = json.loads(base64.b64decode(payload))
            email = payload["email"]
            st.session_state["auth"] = email
            st.session_state["token"] = result["token"]
            st.rerun()
    else:
        #st.write("You are logged in!")
        app_logic()
        #st.write(st.session_state["auth"])
        #st.write(st.session_state["token"])
        if st.button("Logout"):
            del st.session_state["auth"]
            del st.session_state["token"]

if __name__ == "__main__":
    main()


