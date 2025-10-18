#import os, webbrowser, threading
#
#if not os.environ.get("STREAMLIT_BROWSER_OPENED"):
#    os.environ["STREAMLIT_BROWSER_OPENED"] = "1"
#    threading.Timer(1.0, lambda: webbrowser.open_new("http://localhost:8501")).start()

import streamlit as st
import pandas as pd
import plotly.express as px
import ssl
import datetime

# 忽略 SSL 憑證驗證錯誤
ssl._create_default_https_context = ssl._create_unverified_context

# ===== 頁面設定 =====
st.set_page_config(page_title="醫工室儀表板", layout="wide")

# ===== Session 狀態（頁面切換） =====
if "page" not in st.session_state:
    st.session_state.page = "main"

# ===== 自訂按鈕樣式設定 =====
BUTTON_STYLE = {
    "repair": {
        "text": "🧰 維修保養資訊",
        "color": "#1E3A8A",
        "hover": "#2563EB",
        "text_color": "#FFFFFF",
        "font_size": "20px",
        "radius": "14px",
        "width": "420px",
        "height": "70px",
        "margin_top": "10px",
        "margin_bottom": "10px"
    },
    "contract": {
        "text": "📘 合約資訊",
        "color": "#155E75",
        "hover": "#0E7490",
        "text_color": "#FFFFFF",
        "font_size": "18px",
        "radius": "12px",
        "width": "360px",
        "height": "60px",
        "margin_top": "10px",
        "margin_bottom": "10px"
    }
}

維修保養資訊顏色 = "#8FA9FF"

# ===== 自訂 CSS =====
st.markdown("""
    <style>
        body { background-color: #0e1117; color: #e8e8e8; }
        h1, h2, h3 { color: #d0d8ff; text-align: center; }

        .kpi-card {
            background-color: #1c1f26;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.25);
            border: 1px solid #333;
            text-align: center;
            transition: transform 0.2s ease;
            margin-bottom: 12px;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.35);
        }
        .kpi-label {
            color: #ccc;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# ===== KPI 顯示函數 =====
def colored_metric(label, value, color):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{color};">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def rate_color(rate):
    if rate < 0.8:
        return "#FF6347"
    elif rate < 0.9:
        return "#FFD700"
    else:
        return "#32CD32"

# ===== Google Sheet 設定 =====
SHEET_ID = "1-_9tP9j7yDdbcgQHSCycxDzaPCOHYSrCoQ2mZjPLI3I"
SHEET_GIDS = {
    "各同仁維修保養": "0",
    "維修": "221547120",
    "合約清單": "1945804832",
    "合約內容": "1994309175",
    "未完工": "662979561",
    "未完成保養": "1848891402",
}
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid="

@st.cache_data(ttl=600)
def load_data_from_gsheets():
    def safe_read(name, gid):
        url = BASE_URL + gid
        try:
            return pd.read_csv(url)
        except Exception as e:
            st.error(f"❌ 無法讀取【{name}】(GID:{gid})，錯誤：{e}")
            return pd.DataFrame()
    return (
        safe_read("各同仁維修保養", SHEET_GIDS["各同仁維修保養"]),
        safe_read("維修", SHEET_GIDS["維修"]),
        safe_read("合約清單", SHEET_GIDS["合約清單"]),
        safe_read("合約內容", SHEET_GIDS["合約內容"]),
        safe_read("未完工", SHEET_GIDS["未完工"]),
        safe_read("未完成保養", SHEET_GIDS["未完成保養"])
    )

# ===== 主頁面 =====
if st.session_state.page == "main":
    各同仁維修保養, 維修, 合約清單, 合約內容, 未完工, 未完成保養 = load_data_from_gsheets()

    st.markdown("<h1>🏥 醫工室儀表板</h1>", unsafe_allow_html=True)

    # ===== 按鈕區 =====
    col_btn1, col_space, col_btn2 = st.columns([0.9, 0.1, 0.9])

    # 維修保養按鈕
    with col_btn1:
        st.markdown(f"""
            <style>
                div[data-testid="stButton"] button:first-child {{
                    background-color: {BUTTON_STYLE['repair']['color']};
                    color: {BUTTON_STYLE['repair']['text_color']};
                    font-size: {BUTTON_STYLE['repair']['font_size']};
                    border-radius: {BUTTON_STYLE['repair']['radius']};
                    width: {BUTTON_STYLE['repair']['width']};
                    height: {BUTTON_STYLE['repair']['height']};
                    margin-top: {BUTTON_STYLE['repair']['margin_top']};
                    margin-bottom: {BUTTON_STYLE['repair']['margin_bottom']};
                    transition: 0.3s;
                }}
                div[data-testid="stButton"] button:first-child:hover {{
                    background-color: {BUTTON_STYLE['repair']['hover']};
                }}
            </style>
        """, unsafe_allow_html=True)
        if st.button(BUTTON_STYLE["repair"]["text"]):
            st.session_state.page = "repair"
            st.rerun()

    # 合約資訊按鈕
    with col_btn2:
        st.markdown(f"""
            <style>
                div[data-testid="stButton"]:nth-of-type(2) button:first-child {{
                    background-color: {BUTTON_STYLE['contract']['color']};
                    color: {BUTTON_STYLE['contract']['text_color']};
                    font-size: {BUTTON_STYLE['contract']['font_size']};
                    border-radius: {BUTTON_STYLE['contract']['radius']};
                    width: {BUTTON_STYLE['contract']['width']};
                    height: {BUTTON_STYLE['contract']['height']};
                    margin-top: {BUTTON_STYLE['contract']['margin_top']};
                    margin-bottom: {BUTTON_STYLE['contract']['margin_bottom']};
                    transition: 0.3s;
                }}
                div[data-testid="stButton"]:nth-of-type(2) button:first-child:hover {{
                    background-color: {BUTTON_STYLE['contract']['hover']};
                }}
            </style>
        """, unsafe_allow_html=True)
        if st.button(BUTTON_STYLE["contract"]["text"]):
            st.session_state.page = "contract"
            st.rerun()

    st.markdown("---")

    # ===== KPI =====
    if not 各同仁維修保養.empty:
        維修總件數 = 各同仁維修保養["維修總件數"].sum()
        已完成維修件數 = 各同仁維修保養["已完成維修件數"].sum()
        三十天內完成件數 = 各同仁維修保養["三十天內完成件數"].sum()
        未完成維修件數 = 維修總件數 - 已完成維修件數
        維修完成率 = 三十天內完成件數 / 維修總件數 if 維修總件數 else 0

        保養總件數 = 各同仁維修保養["保養總件數"].sum()
        已完成保養件數 = 各同仁維修保養["已完成保養件數"].sum()
        未保養件數 = 保養總件數 - 已完成保養件數
        保養完成率 = 已完成保養件數 / 保養總件數 if 保養總件數 else 0

        五日內內修完成件數 = 各同仁維修保養.get("五日內內修完成件數", pd.Series([0])).sum()
        自修件數 = 各同仁維修保養.get("自修件數", pd.Series([0])).sum()
        五日完修率 = 五日內內修完成件數 / 自修件數 if 自修件數 else 0
    else:
        維修總件數 = 保養總件數 = 已完成維修件數 = 已完成保養件數 = 未完成維修件數 = 未保養件數 = 五日完修率 = 0
    
    # ===== 合約統計 =====
    fig_contract = None
    合約總筆數 = 合約總台數 = 0
    if not 合約清單.empty and not 合約內容.empty:
        if "ContractNo" in 合約清單.columns and "ContractNo" in 合約內容.columns:
            合約清單["ContractNo"] = 合約清單["ContractNo"].astype(str).str.strip()
            合約內容["ContractNo"] = 合約內容["ContractNo"].astype(str).str.strip()
            合約交集 = sorted(set(合約清單["ContractNo"]) & set(合約內容["ContractNo"]))
            合約總筆數 = len(合約交集)

    if not 合約內容.empty and "CLASS" in 合約內容.columns and "Date_T" in 合約內容.columns:
        未結束合約 = 合約內容[合約內容["Date_T"].isna()]
        class_count = 未結束合約["CLASS"].value_counts().reset_index()
        class_count.columns = ["合約類型", "台數"]
        if not class_count.empty:
            fig_contract = px.bar(
                class_count, x="合約類型", y="台數", text="台數",
                title="📊 合約類型分佈圖", color="合約類型"
            )
            fig_contract.update_traces(textposition="outside")
            fig_contract.update_layout(title_x=0.5, plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
            合約總台數 = class_count["台數"].sum()

    col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
    with col1:
        c1, c2 = st.columns(2)
        with c1: colored_metric("維修總件數", f"{維修總件數:,}", "#00BFFF")
        with c2: colored_metric("未完成維修件數", f"{未完成維修件數:,}", "#EE5959")
        c3, c4 = st.columns(2)
        with c3: colored_metric("維修完成率", f"{維修完成率*100:.2f}%", rate_color(維修完成率))
        with c4: colored_metric("五日完修率", f"{五日完修率*100:.2f}%", rate_color(五日完修率))
    with col2:
        c1, c2 = st.columns(2)
        with c1: colored_metric("保養總件數", f"{保養總件數:,}", "#1E90FF")
        with c2: colored_metric("未保養件數", f"{未保養件數:,}", "#EE5959")
        c3, c4 = st.columns(2)
        with c3: colored_metric("保養完成率", f"{保養完成率*100:.2f}%", rate_color(保養完成率))
        with c4: st.empty()
    with col3:
        colored_metric("合約總筆數", f"{len(合約清單):,}", "#BA55D3")
        colored_metric("合約內容筆數", f"{len(合約內容):,}", "#00CED1")

    st.markdown("---")

    # ===== 圖表展示區 =====
    col10, col11, col12 = st.columns(3)
    fig_units = fig_reasons  = None

    if not 維修.empty:
        try:
            if "成本中心名稱" in 維修.columns:
                top_units = (
                    維修["成本中心名稱"]
                    .value_counts()
                    .head(10)
                    .rename_axis("成本中心名稱")
                    .reset_index(name="件數")
                )
                fig_units = px.pie(top_units, names="成本中心名稱", values="件數",
                                title="維修件數前10名單位", hole=0.4)
                fig_units.update_layout(title_x=0.5, plot_bgcolor="rgba(0,0,0,0)")

            if "故障原因" in 維修.columns:
                top_reasons = (
                    維修["故障原因"]
                    .value_counts()
                    .head(10)
                    .rename_axis("故障原因")
                    .reset_index(name="件數")
                )
                fig_reasons = px.pie(top_reasons, names="故障原因", values="件數",
                                    title="故障原因前10名", hole=0.4)
                fig_reasons.update_layout(title_x=0.5, plot_bgcolor="rgba(0,0,0,0)")
        except Exception as e:
            st.error(f"❌ 圖表產生錯誤：{e}")

    if fig_units is not None: col10.plotly_chart(fig_units, use_container_width=True)
    if fig_reasons is not None: col11.plotly_chart(fig_reasons, use_container_width=True)
    if fig_contract is not None: col12.plotly_chart(fig_contract, use_container_width=True)


# ===== 第二頁：維修保養資訊 =====
if st.session_state.page == "repair":
    # 🔹 左上角返回儀表板按鈕
    col_top_left, col_top_right = st.columns([1, 6])
    with col_top_left:
        if st.button("⬅️ 返回儀表板"):
            st.session_state.page = "main"
            st.rerun()
    # 變更處 4：呼叫新的函數
    各同仁維修保養, 維修, 合約清單, 合約內容, 未完工, 未完成保養 = load_data_from_gsheets()

    st.markdown(f"<h2 style='text-align:center; color:{維修保養資訊顏色};'>🧰 維修保養資訊</h2>", unsafe_allow_html=True)

    # 預設年月為當前年月 (格式: 202510 → 11410 需視資料格式調整)
    now = datetime.datetime.now()
    current_yyyymm = (now.year - 1911) * 100 + now.month  # 假設資料年月格式是民國年+月份，例如11410
    年月清單 = sorted(各同仁維修保養["年月"].dropna().unique())
    年月字串清單 = [str(y) for y in 年月清單]

    工程師清單 = sorted(各同仁維修保養["工程師"].dropna().unique())

    col_filter1, col_filter2 = st.columns([0.5, 0.5])
    with col_filter1:
        選工程師 = st.selectbox("選擇工程師", ["全部"] + 工程師清單)
    with col_filter2:
        預設年月字串 = str(current_yyyymm) if str(current_yyyymm) in 年月字串清單 else (年月字串清單[-1] if 年月字串清單 else "整年度")
        
        # 處理 index，避免在清單為空時出錯
        try:
             # 如果清單不為空，且預設字串在清單內，則將預設選項設為選單開頭 (預設選單開頭是 "整年度")
            default_index = 年月字串清單.index(預設年月字串) + 1 if 預設年月字串 != "整年度" and 預設年月字串 in 年月字串清單 else 0
        except ValueError:
             default_index = 0 # 找不到時預設選 "整年度"
        
        選年月 = st.selectbox("查詢年月（或選整年度）", ["整年度"] + 年月字串清單, index=default_index)

    # === 篩選 ===
    df_filtered = 各同仁維修保養.copy()

    if 選工程師 != "全部":
        df_filtered = df_filtered[df_filtered["工程師"] == 選工程師]

    if 選年月 != "整年度":
        選年月_int = int(選年月)    # 字串轉 int
        df_filtered = df_filtered[df_filtered["年月"] == 選年月_int]

    # === KPI ===
    維修總件數 = df_filtered["維修總件數"].sum()
    保養總件數 = df_filtered["保養總件數"].sum()
    維修完成率 = (df_filtered["三十天內完成件數"].sum() / 維修總件數) if 維修總件數 else 0
    保養完成率 = (df_filtered["已完成保養件數"].sum() / 保養總件數) if 保養總件數 else 0

    st.markdown("---")
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1: colored_metric("維修總件數", f"{維修總件數:,}", "#00BFFF")
    with col_k2: colored_metric("保養總件數", f"{保養總件數:,}", "#1E90FF")
    with col_k3: colored_metric("維修完成率", f"{維修完成率*100:.2f}%", rate_color(維修完成率))
    with col_k4: colored_metric("保養完成率", f"{保養完成率*100:.2f}%", rate_color(保養完成率))

    st.markdown("---")

    # === 折線圖 ===
    if not df_filtered.empty:
        # 折線圖用的資料依篩選過後資料做聚合 (依工程師彙總)
        df_line = df_filtered.groupby("工程師").agg({
            "維修總件數": "sum",
            "三十天內完成件數": "sum",
            "保養總件數": "sum",
            "已完成保養件數": "sum"
        }).reset_index()

        # 計算完成率
        df_line["維修完成率"] = df_line["三十天內完成件數"] / df_line["維修總件數"].replace(0, 1)
        df_line["保養完成率"] = df_line["已完成保養件數"] / df_line["保養總件數"].replace(0, 1)

        # 繪製折線圖（百分比顯示 + 固定顏色）
        fig_line = px.line(
            df_line,
            x="工程師",
            y=["維修完成率", "保養完成率"],
            markers=True,
            title="各工程師維修與保養完成率",
            labels={"value": "完成率 (%)", "variable": ""},
            hover_data={"value": ':.0%'},
            color_discrete_map={
                "維修完成率": "#1f77b4",  # 藍色
                "保養完成率": "#ff7f0e"   # 橘色
            }
        )

        fig_line.update_layout(
            title_x=0.5,
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text="",
            yaxis=dict(
                title="完成率 (%)",
                tickformat=".0%",
                range=[0, 1],
                dtick=0.2
            )
        )

        st.plotly_chart(fig_line, use_container_width=True)

    else:
        st.info("查無符合篩選條件的資料")

    # === 長條圖 ===
    if not df_filtered.empty:
        df_bar = df_filtered[["工程師", "維修總件數", "保養總件數"]].melt(
            id_vars="工程師", var_name="項目", value_name="件數"
        )

        # 固定顏色
        color_map = {
            "維修總件數": "#1f77b4",  # 藍色
            "保養總件數": "#ff7f0e"   # 橘色
        }

        fig_bar = px.bar(
            df_bar,
            x="工程師",
            y="件數",
            color="項目",
            barmode="group",
            title="各工程師維修與保養總件數",
            color_discrete_map=color_map
        )

        fig_bar.update_layout(
            title_x=0.5,
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text=""
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # === 故障原因圓餅圖（篩選後維修資料）===
    if not 維修.empty:
        df_維修_filtered = 維修.copy()

        # 篩選維修資料中工程師
        if 選工程師 != "全部" and "工程師" in df_維修_filtered.columns:
            df_維修_filtered = df_維修_filtered[df_維修_filtered["工程師"] == 選工程師]

        # 篩選年月
        if 選年月 != "整年度" and "請修單年月" in df_維修_filtered.columns:
            df_維修_filtered = df_維修_filtered[df_維修_filtered["請修單年月"] == 選年月_int]

        if not df_維修_filtered.empty and "故障原因" in df_維修_filtered.columns:
            top_reasons = df_維修_filtered["故障原因"].value_counts().head(8).reset_index()
            top_reasons.columns = ["故障原因", "件數"]
            fig_pie = px.pie(
                top_reasons,
                names="故障原因",
                values="件數",
                hole=0.4,
                title="故障原因分佈"
            )
            fig_pie.update_layout(title_x=0.5, plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("查無符合篩選條件的維修故障原因資料")

    # === 未完成維修清單與未完成保養清單 ===
    st.markdown("---")
    st.markdown("### 🧾 未完成維修清單")
    if not 未完工.empty:
        df_unfinished_maintain = 未完工.copy()
        if 選工程師 != "全部" and "工程師" in df_unfinished_maintain.columns:
            df_unfinished_maintain = df_unfinished_maintain[df_unfinished_maintain["工程師"] == 選工程師]
        if 選年月 != "整年度" and "請修單年月" in df_unfinished_maintain.columns:
            df_unfinished_maintain = df_unfinished_maintain[df_unfinished_maintain["請修單年月"] == 選年月_int]
        st.dataframe(df_unfinished_maintain, use_container_width=True)
    else:
        st.info("無未完成維修清單資料")

    st.markdown("### 🧾 未完成保養清單")
    if not 未完成保養.empty:
        df_unfinished_service = 未完成保養.copy()
        if 選工程師 != "全部" and "工程師" in df_unfinished_service.columns:
            df_unfinished_service = df_unfinished_service[df_unfinished_service["工程師"] == 選工程師]
        if 選年月 != "整年度" and "保養單年月" in df_unfinished_service.columns:
            df_unfinished_service = df_unfinished_service[df_unfinished_service["保養單年月"] == 選年月_int]
        st.dataframe(df_unfinished_service, use_container_width=True)
    else:
        st.info("無未完成保養清單資料")

    st.markdown("---")

#    if st.button("⬅️ 返回儀表板"):
#        st.session_state.page = "main"
#        st.rerun()

# ===== 第三頁：合約資訊 =====
if st.session_state.page == "contract":    # 🔹 左上角返回儀表板按鈕
    col_top_left, col_top_right = st.columns([1, 6])
    with col_top_left:
        if st.button("⬅️ 返回儀表板"):
            st.session_state.page = "main"
            st.rerun()

    # 重新載入資料
    各同仁維修保養, 維修, 合約清單, 合約內容, 未完工, 未完成保養 = load_data_from_gsheets()

    st.markdown("<h2 style='text-align:center; color:#6EC6FF;'>📘 合約資訊</h2>", unsafe_allow_html=True)

    # ===== KPI 資料計算（以你的合約內容表為例） =====
    # 總合約數與總金額仍算全部
    total_contracts = len(合約內容["ContractNo"].unique())
    total_amount = 合約內容["Cost"].sum()

    # === 只統計未結束合約 (Date_T 為空者) ===
    有效合約 = 合約內容[合約內容["Date_T"].isna()]

    # 未結束合約的設備總台數
    total_assets = len(有效合約["AssetNo"].unique())

    # 各類型合約台數（僅未結束合約）
    full_contracts = 有效合約[有效合約["CLASS"].str.contains("全責", na=False)].shape[0]
    half_contracts = 有效合約[有效合約["CLASS"].str.contains("半責", na=False)].shape[0]
    labor_contracts = 有效合約[有效合約["CLASS"].str.contains("勞務", na=False)].shape[0]
    mix_contracts = 有效合約[有效合約["CLASS"].str.contains("複合", na=False)].shape[0]

    # ===== KPI 方塊樣式 =====
    st.markdown("""
        <style>
        .kpi-box {
            background-color: #11131a;
            border: 2px solid #2a2d36;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin: 5px;
        }
        .kpi-title {
            font-size: 20px;
            color: #d4d4d4;
        }
        .kpi-value {
            font-size: 50px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # ===== KPI 區塊排列（分兩列） =====
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

    with row1_col1:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">維護合約總件數</div>
                <div class="kpi-value" style="color:#99ccff;">{total_contracts}</div>
            </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">維護合約金額</div>
                <div class="kpi-value" style="color:#ffb6c1;">{total_amount:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with row1_col3:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">合約設備總台數</div>
                <div class="kpi-value" style="color:#a4d8ff;">{total_assets}</div>
            </div>
        """, unsafe_allow_html=True)

    with row2_col1:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">全責合約台數</div>
                <div class="kpi-value" style="color:#fff8a3;">{full_contracts}</div>
            </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">半責合約台數</div>
                <div class="kpi-value" style="color:#c7b5ff;">{half_contracts}</div>
            </div>
        """, unsafe_allow_html=True)

    with row2_col3:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">勞務台數</div>
                <div class="kpi-value" style="color:#e5f8cc;">{labor_contracts}</div>
            </div>
        """, unsafe_allow_html=True)

    with row2_col4:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="kpi-title">複合型合約台數</div>
                <div class="kpi-value" style="color:#ffb3b3;">{mix_contracts}</div>
            </div>
        """, unsafe_allow_html=True)

    # ===== 清單區塊 =====
    st.markdown("<br><h2 style='color:white;'>合約清單</h2>", unsafe_allow_html=True)
    st.dataframe(合約清單, use_container_width=True, hide_index=True)

    # ===== 返回首頁按鈕 =====
#    st.markdown("<br>", unsafe_allow_html=True)
#    if st.button("🔙 返回首頁"):
#        st.session_state.page = "main"