import streamlit as st
import pandas as pd
import plotly.express as px


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Robot Market Intelligence Platform",
    layout="wide"
)


# =========================
# HEADER
# =========================

st.title("🤖 ROBOT MARKET INTELLIGENCE PLATFORM")
st.caption(
    "Raw Data Truth Layer - No Added Data - SI From Importer Only"
)


# =========================
# UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload Monthly Raw Data Excel",
    type=["xlsx"]
)


if uploaded_file:


    # =========================
    # READ RAW DATA
    # =========================

    try:

        df = pd.read_excel(
            uploaded_file,
            sheet_name=0
        )

    except Exception as e:

        st.error(
            f"Excel reading error: {e}"
        )

        st.stop()


    # =========================
    # DATA CLEAN BASIC
    # KHÔNG XOÁ DÒNG
    # =========================

    raw_records = len(df)


    st.success(
        f"Loaded {raw_records:,} records successfully"
    )


    st.info(
        f"Raw Data Integrity Check: {raw_records:,} rows preserved"
    )


    # =========================
    # REQUIRED COLUMN CHECK
    # =========================


    required_columns = [

        "Importer",
        "Quantity",
        "Value_USD",
        "Actual_Detailed_Product",
        "Month"

    ]


    missing = [

        col for col in required_columns
        if col not in df.columns

    ]


    if missing:

        st.error(
            "Missing columns: "
            + ", ".join(missing)
        )

        st.stop()



    # =========================
    # NUMERIC CLEAN
    # KHÔNG XOÁ RECORD
    # =========================


    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    ).fillna(0)


    df["Value_USD"] = pd.to_numeric(
        df["Value_USD"],
        errors="coerce"
    ).fillna(0)



    # =========================
    # KPI
    # =========================


    total_units = df["Quantity"].sum()

    total_value = df["Value_USD"].sum()


    avg_asp = (

        total_value / total_units

        if total_units > 0

        else 0

    )



    # =========================
    # TABS
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



    # ==================================================
    # TAB 1 MARKET SIZE
    # ==================================================

    with tab1:


        st.header(
            "Market Size & Landscape"
        )


        c1,c2,c3 = st.columns(3)


        c1.metric(
            "TOTAL UNITS",
            f"{total_units:,.0f}"
        )


        c2.metric(
            "TOTAL VALUE USD",
            f"${total_value:,.0f}"
        )


        c3.metric(
            "AVERAGE ASP",
            f"${avg_asp:,.0f}"
        )


        trend = pd.DataFrame(

            {

                "Metric":[
                    "Units",
                    "Value USD"
                ],

                "Value":[
                    total_units,
                    total_value
                ]

            }

        )


        fig = px.bar(

            trend,

            x="Metric",

            y="Value",

            title="Market Overview"

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    # ==================================================
    # TAB 2 BRAND
    # ==================================================

    with tab2:


        st.header(
            "Brand Analysis"
        )


        st.info(

            "Brand analysis only from uploaded raw data. "
            "No external data added."

        )


        st.dataframe(

            df.head(200),

            use_container_width=True

        )



    # ==================================================
    # TAB 3 CUSTOMER INTELLIGENCE
    # SI = IMPORTER
    # ==================================================

    with tab3:


        st.header(

            "SI / Customer Intelligence"

        )


        st.info(

            "SI is evaluated directly from Importer column"

        )


        si_table = (

            df.groupby("Importer")

            .agg(

                Units=(
                    "Quantity",
                    "sum"
                ),

                Revenue_USD=(

                    "Value_USD",

                    "sum"

                )

            )

            .reset_index()

            .sort_values(

                "Revenue_USD",

                ascending=False

            )

        )


        st.dataframe(

            si_table,

            use_container_width=True

        )


        fig = px.bar(

            si_table,

            x="Importer",

            y="Revenue_USD",

            title="Importer Ranking"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )



    # ==================================================
    # TAB 4 STRATEGIC
    # ==================================================

    with tab4:


        st.header(

            "Strategic Opportunity Mapping"

        )


        st.warning(

            "No SI guessing. No added mapping. "
            "Only uploaded data."

        )


        st.write(

            "Available Importer Count:",

            df["Importer"].nunique()

        )



    # ==================================================
    # TAB 5 EXECUTIVE
    # ==================================================

    with tab5:


        st.header(

            "Executive Summary"

        )


        summary = {


            "Raw Records":

            int(len(df)),


            "Total Units":

            float(total_units),


            "Total Value USD":

            float(total_value),


            "Importer Count":

            int(df["Importer"].nunique())


        }


        st.json(summary)



else:


    st.info(

        "Please upload Excel file"

    )
