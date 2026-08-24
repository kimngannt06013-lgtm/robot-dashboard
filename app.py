import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Robot Market Intelligence Platform",
    layout="wide"
)


st.title("🤖 ROBOT MARKET INTELLIGENCE PLATFORM")
st.caption("Raw Data Only - No Added Data")


# =========================
# UPLOAD FILE
# =========================

uploaded_file = st.file_uploader(
    "Upload Monthly Raw Data Excel",
    type=["xlsx"]
)


if uploaded_file:


    df = pd.read_excel(uploaded_file, sheet_name=0)


    st.success(
        f"Loaded {len(df)} records successfully"
    )


    # =========================
    # KIỂM TRA CỘT
    # =========================

    required = [
        "Importer",
        "Quantity",
        "Value_USD",
        "Actual_Detailed_Product",
        "Month"
    ]


    missing = []

    for c in required:
        if c not in df.columns:
            missing.append(c)


    if missing:

        st.error(
            "Missing columns: "
            + ", ".join(missing)
        )

        st.stop()



    # =========================
    # TAB
    # =========================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "TAB 1 Market Size",
            "TAB 2 Brand",
            "TAB 3 Customer Intelligence",
            "TAB 4 Strategic",
            "TAB 5 Executive Summary"
        ]
    )


    # =========================
    # TAB 1
    # =========================

    with tab1:

        st.header("Market Size")


        total_units = df["Quantity"].sum()

        total_value = df["Value_USD"].sum()

        asp = (
            total_value / total_units
            if total_units != 0
            else 0
        )


        c1,c2,c3 = st.columns(3)


        c1.metric(
            "Total Units",
            f"{total_units:,.0f}"
        )


        c2.metric(
            "Total Value USD",
            f"${total_value:,.0f}"
        )


        c3.metric(
            "Average ASP",
            f"${asp:,.0f}"
        )



    # =========================
    # TAB 2
    # =========================

    with tab2:

        st.header("Brand Opportunity")

        st.info(
            "Brand sẽ lấy trực tiếp từ dữ liệu Excel"
        )


        st.dataframe(df.head(100))



    # =========================
    # TAB 3
    # =========================

    with tab3:

        st.header(
            "Customer Intelligence"
        )


        importer = (
            df.groupby("Importer")
            .agg(
                Units=("Quantity","sum"),
                Value_USD=("Value_USD","sum")
            )
            .reset_index()
            .sort_values(
                "Value_USD",
                ascending=False
            )
        )


        st.dataframe(
            importer
        )


        fig = px.bar(
            importer,
            x="Importer",
            y="Value_USD",
            title="Importer Ranking"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # =========================
    # TAB 4
    # =========================

    with tab4:

        st.header(
            "Strategic Opportunity Mapping"
        )


        st.warning(
            "Chỉ hiển thị dữ liệu có trong file upload"
        )

        st.write(
            "No additional SI mapping applied."
        )



    # =========================
    # TAB 5
    # =========================

    with tab5:

        st.header(
            "Executive Summary"
        )


        st.write(
            "Dashboard Summary"
        )


        st.write(
            {
                "Records":len(df),
                "Units":int(total_units),
                "Value_USD":float(total_value)
            }
        )


else:

    st.info(
        "Please upload Excel file"
    )
