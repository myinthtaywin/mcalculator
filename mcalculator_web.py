import streamlit as st
import math
import datetime
from dateutil.relativedelta import relativedelta

# Set page config
st.set_page_config(page_title="M-Calculator", page_icon="🧮")
st.title("🧮 M-Calculator")

# Dropdown selection
option = st.selectbox("Choose Calculator Type:", ["Simple Calculation", "Time Value of Money Calculation", "Savings Goal Tracker"])

# --- Simple Calculator ---
if option == "Simple Calculation":
    st.subheader("Simple Arithmetic Calculator")
    num1 = st.text_input("Enter First Number:", value="")
    num2 = st.text_input("Enter Second Number:", value="")
    operator = st.selectbox("Choose Operator:", ["+", "-", "*", "/"])

    if st.button("Calculate"):
        try:
            num1 = float(num1.replace(",", ""))
            num2 = float(num2.replace(",", ""))
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
    pv = st.text_input("Present Value (PV):", value="")
    fv = st.text_input("Future Value (FV):", value="")
    annual_rate = st.text_input("Annual Interest Rate (%):", value="")
    pmt = st.text_input("Payment Amount (PMT):", value="")
    n = st.text_input("Number of Payments:", value="")
    mode = st.selectbox("Payment Mode:", ["Year", "Month", "Day"])

    def get_rate():
        rate = float(annual_rate.replace(",", "")) / 100
        if mode == "Month": return rate / 12
        if mode == "Day": return rate / 365
        return rate

    def get_n():
        return int(n.replace(",", ""))

    if st.button("Calculate"):
        try:
            r = get_rate()
            total_n = get_n()
            pv_val = float(pv.replace(",", ""))
            fv_val = float(fv.replace(",", ""))
            pmt_val = float(pmt.replace(",", ""))

            if calc_type == "Future Value":
                result = pv_val * (1 + r) ** total_n + pmt_val * (((1 + r) ** total_n - 1) / r)
                st.success(f"Future Value: {result:,.2f}")

            elif calc_type == "Present Value":
                result = (fv_val - pmt_val * (((1 + r) ** total_n - 1) / r)) / ((1 + r) ** total_n)
                st.success(f"Present Value: {result:,.2f}")

            elif calc_type == "Payment Amount":
                result = (fv_val * r) / ((1 + r) ** total_n - 1)
                st.success(f"Payment Amount: {result:,.2f}")

            elif calc_type == "Interest Rate":
                r_est = (fv_val / pv_val) ** (1 / total_n) - 1
                if mode == "Month": r_est *= 12
                elif mode == "Day": r_est *= 365
                st.success(f"Estimated Annual Interest Rate: {r_est * 100:,.4f}%")

            elif calc_type == "Number of Payments":
                if pmt_val == 0:
                    result = math.log(fv_val / pv_val) / math.log(1 + r)
                else:
                    numerator = pmt_val + r * fv_val
                    denominator = pmt_val + r * pv_val
                    result = math.log(numerator / denominator) / math.log(1 + r)
                st.success(f"Number of Payments: {result:,.2f}")

        except Exception as e:
            st.error(f"Calculation error: {e}")

# --- Savings Goal Tracker ---
elif option == "Savings Goal Tracker":
    st.subheader("💰 Savings Goal Tracker")

    goal_name = st.text_input("Goal Name", "Emergency Fund")
    target_amount = st.text_input("Target Amount:", value="")
    current_savings = st.text_input("Current Savings:", value="")
    savings_frequency = st.selectbox("Savings Frequency:", ["Day", "Week", "Month", "Year"])
    contribution = st.text_input("Contribution per Period:", value="")
    savings_rate = st.text_input("Estimated Annual Interest Rate (%):", value="")
    months = st.text_input("Target Timeline (in months):", value="")

    try:
        t_amt = float(target_amount.replace(",", ""))
        c_sav = float(current_savings.replace(",", ""))
        contrib = float(contribution.replace(",", ""))
        rate = float(savings_rate.replace(",", "")) / 100
        period_months = {"Day": 1/30, "Week": 12/52, "Month": 1, "Year": 12}[savings_frequency]
        r = rate / 12
        n_months = int(months.replace(",", "")) if months else 0

        total_contrib = contrib * (n_months / period_months)
        future_value = c_sav * (1 + r) ** n_months + contrib * (((1 + r) ** n_months - 1) / r) if r > 0 else c_sav + total_contrib

        progress = min(c_sav / t_amt, 1.0)
        st.progress(progress)
        st.write(f"**Progress:** {progress*100:.1f}% toward your {goal_name}")
        st.write(f"**Projected Value After {n_months:,} Months:** {future_value:,.2f}")

        # Estimate completion date with interest using logarithmic formula
        if contrib > 0:
            if r > 0:
                A = t_amt
                B = contrib
                P = c_sav
                n_calc = math.log((B + r * A) / (B + r * P)) / math.log(1 + r)
                n_calc = int(round(n_calc))
            else:
                n_calc = math.ceil((t_amt - c_sav) / contrib * period_months)

            today = datetime.date.today()
            completion_date = today + relativedelta(months=n_calc)
            years = n_calc // 12
            months_remain = n_calc % 12
            st.info(f"Estimated Completion: {completion_date.strftime('%B %Y')} → {years} year(s) and {months_remain} month(s)")
        else:
            st.warning("Contribution must be greater than 0 to estimate completion date.")

    except Exception as e:
        st.warning("Fill in all numeric fields to see results.")
