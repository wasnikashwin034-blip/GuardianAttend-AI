import streamlit as st
import sqlite3
import pandas as pd


DATABASE = "data/attendance.db"



# ==============================
# GET STUDENT FEES
# ==============================

def get_fee_data(student_name):

    conn = sqlite3.connect(
        DATABASE
    )


    fee = pd.read_sql_query(

        """
        SELECT *
        FROM fees
        WHERE student_name=?

        """,

        conn,

        params=(student_name,)

    )


    conn.close()

    return fee




# ==============================
# PAYMENT HISTORY
# ==============================

def get_payment_history(student_name):

    conn = sqlite3.connect(
        DATABASE
    )


    payments = pd.read_sql_query(

        """
        SELECT *
        FROM payments
        WHERE student_name=?

        ORDER BY id DESC

        """,

        conn,

        params=(student_name,)

    )


    conn.close()

    return payments




# ==============================
# STUDENT FEES PAGE
# ==============================


def show():


    st.title(
        "💳 My Fees"
    )


    st.subheader(
        "🛡️ GuardianAttend AI | Student Fee Portal"
    )


    st.divider()



    username = st.session_state.username



    fees = get_fee_data(
        username
    )



    if fees.empty:


        st.warning(
            "No fee record found"
        )

        return



    data = fees.iloc[0]



    total = data["total_amount"]

    paid = data["paid_amount"]

    pending = data["pending_amount"]

    status = data["payment_status"]




    # ==============================
    # FEE CARDS
    # ==============================


    col1,col2,col3 = st.columns(3)



    with col1:

        st.metric(
            "💰 Total Fees",
            f"₹ {total}"
        )



    with col2:

        st.metric(
            "✅ Paid",
            f"₹ {paid}"
        )



    with col3:

        st.metric(
            "⏳ Pending",
            f"₹ {pending}"
        )



    st.divider()



    # ==============================
    # STATUS
    # ==============================


    if status=="Paid":

        st.success(
            "✅ All fees paid"
        )

    else:

        st.warning(
            f"Pending Amount: ₹ {pending}"
        )



        if st.button(
            "💳 Pay Now"
        ):

            st.info(
                "Online payment gateway will be connected in Phase 5.3"
            )



    st.divider()



    # ==============================
    # PAYMENT HISTORY
    # ==============================


    st.subheader(
        "📜 Payment History"
    )


    history = get_payment_history(
        username
    )



    if not history.empty:


        st.dataframe(

            history,

            width="stretch"

        )


    else:


        st.info(
            "No payments made yet"
        )