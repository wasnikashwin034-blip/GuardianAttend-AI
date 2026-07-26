import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


DATABASE = "data/attendance.db"



# ==============================
# ADD FEES RECORD
# ==============================

def add_fee(student, total):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO fees
        (
        student_name,
        total_amount,
        paid_amount,
        pending_amount,
        payment_status
        )

        VALUES(?,?,?,?,?)

        """,

        (
            student,
            total,
            0,
            total,
            "Pending"
        )

    )


    conn.commit()

    conn.close()



# ==============================
# UPDATE PAYMENT
# ==============================

def make_payment(student, amount):


    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT total_amount,paid_amount
        FROM fees
        WHERE student_name=?

        """,

        (student,)

    )


    data = cursor.fetchone()



    if data:


        total = data[0]

        paid = data[1]


        new_paid = paid + amount


        pending = total - new_paid



        status = "Paid" if pending <= 0 else "Pending"



        cursor.execute(
            """
            UPDATE fees

            SET paid_amount=?,
            pending_amount=?,
            payment_status=?,
            last_payment_date=?

            WHERE student_name=?

            """,

            (

            new_paid,

            pending,

            status,

            datetime.now().strftime("%Y-%m-%d"),

            student

            )

        )



        cursor.execute(
            """
            INSERT INTO payments

            (
            student_name,
            amount,
            payment_date,
            status
            )

            VALUES(?,?,?,?)

            """,

            (

            student,

            amount,

            datetime.now().strftime("%Y-%m-%d"),

            "Success"

            )

        )



        conn.commit()



    conn.close()




# ==============================
# LOAD FEES
# ==============================

def get_fees():

    conn = sqlite3.connect(
        DATABASE
    )


    df = pd.read_sql_query(

        """
        SELECT *
        FROM fees

        """,

        conn

    )


    conn.close()


    return df




# ==============================
# ADMIN FEES PAGE
# ==============================

def show():


    st.title(
        "💰 Fees Management"
    )


    st.subheader(
        "GuardianAttend AI | Admin Panel"
    )


    st.divider()



    # ADD FEES

    st.header(
        "➕ Add Student Fees"
    )


    student = st.text_input(
        "Student Name"
    )


    total = st.number_input(
        "Total Fees (£)",
        min_value=0
    )



    if st.button(
        "Add Fees"
    ):

        add_fee(
            student,
            total
        )

        st.success(
            "Fees added successfully"
        )

        st.rerun()



    st.divider()



    # PAYMENT UPDATE

    st.header(
        "💳 Receive Payment"
    )


    pay_student = st.text_input(
        "Student Name",
        key="pay"
    )


    amount = st.number_input(
        "Payment Amount (£)",
        min_value=0,
        key="amount"
    )



    if st.button(
        "Update Payment"
    ):

        make_payment(
            pay_student,
            amount
        )

        st.success(
            "Payment updated"
        )

        st.rerun()



    st.divider()



    # DISPLAY DATA

    st.header(
        "📋 Fees Records"
    )


    df = get_fees()



    if not df.empty:

        st.dataframe(
            df,
            width="stretch"
        )


    else:

        st.info(
            "No fee records available"
        )