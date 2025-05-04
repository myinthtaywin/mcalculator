import streamlit as st
import math

# Set page config
st.set_page_config(page_title="M-Calculator", page_icon="🧮")
st.title("🧮 M-Calculator")

# Dropdown selection
option = st.selectbox("Choose Calculator Type:", ["Simple Calculation", "Time Value of Money Calculation"])

# --- Simple Calculator ---
if option == "Simple Calculation":
    st.subheader("Simple Arithmetic Calculator")
    num1 = st.number_input("Enter First Number:", value=0.0)
    num2 = st.number_input("Enter Second Number:", value=0.0)
    operator = st.selectbox("Choose Operator:", ["+", "-", "*", "/"])

    if st.button("Calculate"):
        try:
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                result = num1 / num2
            st.success(f"Result: {result:,.2f}")
        except Exception as e:
            st.error(f"Error: {e}")

# --- TVM Calculator ---
elif option == "Time Value of Money Calculation":
    st.subheader("Time Value of Money Calculator")

    calc_type = st.radio("Select what to calculate:", ["Future Value", "Present Value", "Interest Rate", "Number of Payments", "Payment Amount"])

    # Inputs
    pv = st.number_input("Present Value (PV):", value=0.0, format="%f")
    fv = st.number_input("Future Value (FV):", value=0.0, format="%f")
    annual_rate = st.number_input("Annual Interest Rate (%):", value=7.0)
    pmt = st.number_input("Payment Amount (PMT):", value=0.0, format="%f")
    n = st.number_input("Number of Payments:", value=0, step=1)
    mode = st.selectbox("Payment Mode:", ["Year", "Month", "Day"])

    def get_rate():
        if mode == "Month": return annual_rate / 100 / 12
        if mode == "Day": return annual_rate / 100 / 365
        return annual_rate / 100

    def get_n():
        return int(n)

    if st.button("Calculate"):
        try:
            r = get_rate()
            total_n = get_n()

            if calc_type == "Future Value":
                result = pv * (1 + r) ** total_n + pmt * (((1 + r) ** total_n - 1) / r)
                st.success(f"Future Value: {result:,.2f}")

            elif calc_type == "Present Value":
                result = (fv - pmt * (((1 + r) ** total_n - 1) / r)) / ((1 + r) ** total_n)
                st.success(f"Present Value: {result:,.2f}")

            elif calc_type == "Payment Amount":
                result = (fv * r) / ((1 + r) ** total_n - 1)
                st.success(f"Payment Amount: {result:,.2f}")

            elif calc_type == "Interest Rate":
                r_est = (fv / pv) ** (1 / total_n) - 1
                if mode == "Month": r_est *= 12
                elif mode == "Day": r_est *= 365
                st.success(f"Estimated Annual Interest Rate: {r_est * 100:,.4f}%")

            elif calc_type == "Number of Payments":
                if pmt == 0:
                    result = math.log(fv / pv) / math.log(1 + r)
                else:
                    numerator = pmt + r * fv
                    denominator = pmt + r * pv
                    result = math.log(numerator / denominator) / math.log(1 + r)
                st.success(f"Number of Payments: {result:,.2f}")

        except Exception as e:
            st.error(f"Calculation error: {e}")
