import streamlit as st
import pandas as pd
import datetime
import calendar

# ==========================================
# 1. 페이지 설정 및 초기화
# ==========================================
st.set_page_config(page_title="태리의 캘린더", page_icon="🐾", layout="wide")

# 현재 날짜 기준 초기화
today = datetime.date.today()

# 세션 상태(더미 데이터 및 캘린더 네비게이션) 초기화
if 'records' not in st.session_state:
    st.session_state.records = {
        (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"): {
            "height": 85.2, "weight": 11.5, "breakfast": "소고기 미역국 진밥", 
            "lunch": "닭고기 브로콜리 덮밥", "dinner": "두부 버섯 리조또", "snack": "사과 퓨레"
        },
        today.strftime("%Y-%m-%d"): {
            "height": 85.5, "weight": 11.6, "breakfast": "오트밀 바나나 포리지", 
            "lunch": "", "dinner": "", "snack": "치즈 1장"
        }
    }

if 'view_year' not in st.session_state:
    st.session_state.view_year = today.year

if 'view_month' not in st.session_state:
    st.session_state.view_month = today.month

# ==========================================
# 2. Custom CSS 주입 (테마, 색상 고정, 폰트 적용)
# ==========================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    /* 전체 폰트 및 배경 하얀색 강제 설정 */
    html, body, [class*="css"], .stApp {
        font-family: 'Jua', sans-serif !important;
        background-color: #FFFFFF !important;
    }
    
    /* Streamlit 기본 UI 요소 텍스트 색상 강제 지정 (다크모드 대비) */
    p, span, label, div[data-testid="stRadio"] label p, div[data-testid="stSidebar"] * {
        color: #333333 !important;
    }
    
    /* 제목 네이비색 고정 */
    .main-title {
        color: #000080 !important;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }

    /* 캘린더 네비게이션 영역 */
    .nav-header {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    .month-title {
        font-size: 1.8rem;
        color: #333333;
        font-weight: bold;
        margin: 0;
    }
    
    /* 캘린더 그리드 스타일 */
    .calendar-container {
        margin-top: 10px;
    }
    .week-header {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 15px;
        text-align: center;
        font-size: 1.2rem;
        color: #666 !important;
        margin-bottom: 10px;
    }
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 15px;
    }
    
    /* 개별 날짜 카드 스타일 */
    .day-card {
        background-color: #ffffff;
        border-radius: 16px;
        min-height: 140px;
        padding: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 2px solid #F3F4F6;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .day-card.empty {
        background-color: transparent;
        box-shadow: none;
        border: none;
    }
    .day-card.today {
        border: 2px solid #FFB6C1;
        background-color: #FFF5F7;
    }
    .day-number {
        font-size: 1.2rem;
        color: #333 !important;
    }
    
    /* 뱃지 스타일 */
    .badge-container {
        display: flex;
        gap: 5px;
        flex-wrap: wrap;
    }
    .badge-height {
        background-color: #D1FAE5;
        color: #065F46 !important;
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.85rem;
    }
    .badge-weight {
        background-color: #FCE7F3;
        color: #9D174D !important;
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.85rem;
    }
    .diet-emoji {
        font-size: 1.3rem;
        margin-top: auto;
        text-align: right;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. 사이드바: 데이터 입력 폼
# ==========================================
with st.sidebar:
    st.markdown("## 기록하기 ✏️")
    
    # 날짜 선택
    selected_date = st.date_input("날짜를 선택하세요", today)
    date_str = selected_date.strftime("%Y-%m-%d")
    
    # 기존 데이터 불러오기
    existing_data = st.session_state.records.get(date_str, {
        "height": 0.0, "weight": 0.0, 
        "breakfast": "", "lunch": "", "dinner": "", "snack": ""
    })
    
    st.markdown("### 📏 쑥쑥 자라요")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("키 (cm)", value=float(existing_data["height"]), step=0.1)
    with col2:
        weight = st.number_input("몸무게 (kg)", value=float(existing_data["weight"]), step=0.1)
        
    st.markdown("### 🍽️ 냠냠 먹어요")
    breakfast = st.text_input("아침", value=existing_data["breakfast"], placeholder="예: 오트밀 퓨레")
    lunch = st.text_input("점심", value=existing_data["lunch"], placeholder="예: 소고기 무국")
    dinner = st.text_input("저녁", value=existing_data["dinner"], placeholder="예: 닭고기 리조또")
    snack = st.text_input("간식", value=existing_data["snack"], placeholder="예: 사과 반 개")
    
    if st.button("저장하기 💖", use_container_width=True):
        st.session_state.records[date_str] = {
            "height": height, "weight": weight,
            "breakfast": breakfast, "lunch": lunch,
            "dinner": dinner, "snack": snack
        }
        st.success(f"{date_str} 기록이 저장되었어요!")

# ==========================================
# 4. 메인 화면 상단 (제목 및 보기 옵션)
# ==========================================
col_title, col_toggle = st.columns([3, 1])
with col_title:
    st.markdown('<h1 class="main-title">태리의 캘린더 🐾</h1>', unsafe_allow_html=True)
with col_toggle:
    view_mode = st.radio("보기 모드", ["Month (월별)", "Week (주별)"], horizontal=True, label_visibility="collapsed")

# ==========================================
# 5. 캘린더 네비게이션 (이전 달 / 다음 달)
# ==========================================
# 네비게이션 로직 구현을 위해 컬럼 배치
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([2, 1, 2, 1, 2])

with nav_col2:
    if st.button("◀ 이전 달", use_container_width=True):
        if st.session_state.view_month == 1:
            st.session_state.view_month = 12
            st.session_state.view_year -= 1
        else:
            st.session_state.view_month -= 1
        st.rerun()

with nav_col3:
    st.markdown(f"<div style='text-align: center;'><h2 class='month-title'>{st.session_state.view_year}년 {st.session_state.view_month}월</h2></div>", unsafe_allow_html=True)

with nav_col4:
    if st.button("다음 달 ▶", use_container_width=True):
        if st.session_state.view_month == 12:
            st.session_state.view_month = 1
            st.session_state.view_year += 1
        else:
            st.session_state.view_month += 1
        st.rerun()

# ==========================================
# 6. 달력 렌더링 로직
# ==========================================
def generate_calendar_html(year, month, mode="Month (월별)", selected_date=None):
    cal = calendar.Calendar(firstweekday=6) # 일요일부터 시작
    
    html = '<div class="calendar-container">'
    html += '<div class="week-header"><div>일</div><div>월</div><div>화</div><div>수</div><div>목</div><div>금</div><div>토</div></div>'
    html += '<div class="calendar-grid">'
    
    all_weeks = cal.monthdatescalendar(year, month)
    
    if mode == "Month (월별)":
        weeks_to_show = all_weeks
    else:
        # 주별 모드: 사이드바에서 선택한 날짜가 포함된 주만 필터링
        weeks_to_show = [week for week in all_weeks if selected_date in week]
        if not weeks_to_show: 
            # 만약 선택한 날짜가 현재 보고 있는 달력 화면(연/월)과 아예 다르면 첫 번째 주를 보여줌
            weeks_to_show = [all_weeks[0]]

    for week in weeks_to_show:
        for day in week:
            # 월별 보기에서 이전/다음 달 날짜 처리 (빈 칸 처리)
            if mode == "Month (월별)" and day.month != month:
                html += '<div class="day-card empty"></div>'
                continue
                
            date_str = day.strftime("%Y-%m-%d")
            record = st.session_state.records.get(date_str, {})
            
            # 선택한 날짜 하이라이트
            today_class = "today" if day == selected_date else ""
            
            html += f'<div class="day-card {today_class}">'
            html += f'<div class="day-number">{day.day}</div>'
            
            # 키/몸무게 뱃지
            html += '<div class="badge-container">'
            if record.get("height", 0) > 0:
                html += f'<div class="badge-height">키 {record["height"]}</div>'
            if record.get("weight", 0) > 0:
                html += f'<div class="badge-weight">몸 {record["weight"]}</div>'
            html += '</div>'
            
            # 식단 이모지 표시 로직
            diet_icons = ""
            if record.get("breakfast"): diet_icons += "🍼"
            if record.get("lunch") or record.get("dinner"): diet_icons += "🍚"
            if record.get("snack"): diet_icons += "🍎"
            
            if diet_icons:
                html += f'<div class="diet-emoji">{diet_icons}</div>'
                
            html += '</div>'
            
    html += '</div></div>'
    return html

# HTML 생성 및 출력
calendar_html = generate_calendar_html(st.session_state.view_year, st.session_state.view_month, view_mode, selected_date)
st.markdown(calendar_html, unsafe_allow_html=True)