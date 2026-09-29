import streamlit as st

st.set_page_config(page_title="A 股投顾助手", page_icon="📈", layout="wide")

st.title("A 股投顾助手")
st.caption("轻量版智能投顾助手：输入股票代码，查看趋势、风险与投资建议")

with st.sidebar:
    st.header("参数设置")
    symbol = st.text_input("股票代码", value="600519")
    risk_tolerance = st.selectbox("风险偏好", ["低风险", "中等", "高风险"])
    run_analysis = st.button("生成分析")

if run_analysis:
    if not symbol:
        st.warning("请先输入股票代码")
    else:
        # 这里直接使用本地模拟评分逻辑（离线版，可在 Codespaces / iPad 中运行）
        from src.analysis.scoring import analyze_symbol

        result = analyze_symbol(symbol, risk_tolerance=risk_tolerance)

        if result.get("error"):
            st.error(result["error"])
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("综合评分", f"{result['score']}/100")
            col2.metric("趋势评分", f"{result['trend_score']}/100")
            col3.metric("风险评分", f"{result['risk_score']}/100")
            col4.metric("当前价", f"¥{result['price']:.2f}")

            st.markdown(f"### 投资建议：{result['advice']}")
            st.info(result["summary"])

            tab1, tab2, tab3 = st.tabs(["投资结论", "关键理由", "风控提示"])

            with tab1:
                st.write(result["investment_thesis"])

            with tab2:
                for item in result["reasons"]:
                    st.markdown(f"- {item}")

            with tab3:
                for item in result["risk_notes"]:
                    st.markdown(f"- {item}")

            st.markdown("---")
            st.subheader("关键指标")
            metrics_cols = st.columns(len(result["metrics"]))
            for col, (key, value) in zip(metrics_cols, result["metrics"].items()):
                col.metric(key, value)
else:
    st.markdown("### 使用说明")
    st.markdown("- 输入一个股票代码，例如 600519、000001")
    st.markdown("- 选择你的风险偏好")
    st.markdown("- 点击“生成分析”查看趋势、价格和建议")
    st.markdown("- 当前版本使用离线模拟数据，便于在 iPad / Codespaces 里演示")
    st.markdown("---")
    st.markdown("### 免责声明")
    st.markdown("- 本项目仅用于学习和研究，不构成投资建议")
    st.markdown("- 不自动下单，也不承诺收益")
    st.markdown("- 真实投资应结合基本面、消息面和风险控制")
