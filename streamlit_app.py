from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

st.set_page_config(page_title="지피터스 전자책 스터디", page_icon="🎈", layout="wide")

st.title("🎈 지피터스 전자책 스터디")
st.markdown(
    """
    이번 생에 꼭 하겠다던 전자책을 끝까지 완성하는 지피터스 스터디에 오신 것을 환영합니다.
    하루의 목표와 목차를 정리하고, 진척도를 꾸준히 기록하며 함께 완성해 봐요! ✍️
    """
)


def _init_session_state() -> None:
    """Ensure lists used in the UI are initialised only once."""

    st.session_state.setdefault("chapter_plan", [])


_init_session_state()

with st.sidebar:
    st.header("📌 스터디 설정")
    today = date.today()
    start_date = st.date_input("시작일", value=today)
    end_date = st.date_input("완성 목표일", value=today + timedelta(days=13))

    if end_date <= start_date:
        st.warning("완성 목표일은 시작일 이후로 설정해 주세요.")
        duration = 1
    else:
        duration = (end_date - start_date).days + 1

    target_pages = int(
        st.number_input("목표 분량 (페이지)", min_value=1, step=1, value=30)
    )
    words_per_page = int(
        st.number_input("페이지 당 예상 단어 수", min_value=50, step=50, value=300)
    )
    completed_pages = int(
        st.number_input(
            "현재까지 작성한 페이지",
            min_value=0,
            max_value=max(target_pages, 1),
            step=1,
            value=0,
        )
    )

daily_pages = target_pages / duration
remaining_pages = max(target_pages - completed_pages, 0)
required_daily_pages = (
    0 if remaining_pages == 0 else remaining_pages / max((end_date - date.today()).days + 1, 1)
)

tab_overview, tab_outline, tab_checkins = st.tabs(["진척 현황", "목차 설계", "체크인 노트"])

with tab_overview:
    st.subheader("📈 프로젝트 현황")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 목표 페이지", f"{target_pages}p")
    col2.metric("예상 총 단어 수", f"{target_pages * words_per_page:,} 단어")
    col3.metric("필요한 하루 분량", f"{daily_pages:.1f}p")

    st.divider()
    st.subheader("⏱️ 남은 일정")
    remaining_days = max((end_date - date.today()).days + 1, 0)
    st.write(
        f"오늘 기준 남은 일정은 **{remaining_days}일**, 남은 분량은 **{remaining_pages} 페이지**입니다."
    )
    if remaining_pages == 0:
        st.success("목표 분량을 모두 달성했어요! 다음 챕터를 준비해 볼까요?")
    else:
        st.info(
            f"남은 기간 동안 매일 약 **{required_daily_pages:.1f} 페이지**를 작성하면 목표를 달성할 수 있어요."
        )

    st.divider()
    st.subheader("🗓️ 작성 일정표")
    schedule = []
    for offset in range(duration):
        current_day = start_date + timedelta(days=offset)
        cumulative_goal = min(round(daily_pages * (offset + 1), 1), target_pages)
        schedule.append(
            {
                "날짜": current_day.strftime("%Y-%m-%d"),
                "누적 목표 페이지": cumulative_goal,
                "남은 페이지": max(target_pages - cumulative_goal, 0),
            }
        )

    st.dataframe(schedule, hide_index=True, use_container_width=True)

with tab_outline:
    st.subheader("🧭 목차 설계")
    st.write(
        "아이디어가 떠오를 때마다 챕터를 추가하세요. 저장된 항목은 세션이 유지되는 동안에만 보관됩니다."
    )

    with st.form("chapter_form", clear_on_submit=True):
        chapter_title = st.text_input("챕터 제목", placeholder="예: 1장 - 전자책 기획하기")
        key_takeaway = st.text_area("핵심 메시지", placeholder="이 챕터에서 독자가 얻어갈 내용을 정리해 보세요.")
        submitted = st.form_submit_button("추가하기", use_container_width=True)

        if submitted and chapter_title:
            st.session_state.chapter_plan.append(
                {"챕터": chapter_title, "핵심 메시지": key_takeaway.strip()}
            )

    if st.session_state.chapter_plan:
        st.table(st.session_state.chapter_plan)
        if st.button("목차 초기화", type="secondary"):
            st.session_state.chapter_plan.clear()
    else:
        st.caption("아직 추가된 챕터가 없어요. 위 폼을 사용해 목차를 만들어 보세요.")

with tab_checkins:
    st.subheader("📝 데일리 체크인")
    st.write("오늘의 하이라이트와 배운 점을 기록하며 모멘텀을 유지하세요.")
    st.text_area(
        "오늘의 기록",
        placeholder="예: 오늘은 5페이지를 작성했고, 독자의 주요 고민을 더 구체화했습니다.",
        height=200,
    )

st.toast("집중력을 유지하고 원하는 책을 완성해 봅시다!", icon="📚")
