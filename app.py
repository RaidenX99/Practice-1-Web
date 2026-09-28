# -*- coding: utf-8 -*-
import streamlit as st
import json
import base64
import io
import math
from PIL import Image
from datetime import datetime
import plotly.graph_objects as go
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from core import PracticeEngine

st.set_page_config(page_title="Практическая работа №4", layout="centered", page_icon="📉")

def upload_to_google_drive(file_content, filename):
    try:
        folder_id = st.secrets["GOOGLE_DRIVE_FOLDER_ID"]
        creds_dict = dict(st.secrets["google_credentials"])
        
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=['https://www.googleapis.com/auth/drive.file']
        )
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        
        media = MediaIoBaseUpload(
            io.BytesIO(file_content.encode('utf-8')), 
            mimetype='application/json',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return True
    except Exception as e:
        st.error(f"Ошибка автовыгрузки в облако: {e}")
        return False

def parse_float(val_str):
    try:
        return float(val_str.strip().replace(',', '.'))
    except:
        return None

def draw_uniform_simulation(ans_str, task_data):
    a = task_data.get('a', 10)
    b = task_data.get('b', 50)
    val = parse_float(ans_str)
    
    height = 1 / (b - a) if b > a else 1
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[a, b, b, a, a], y=[0, 0, height, height, 0], fill='toself', mode='lines', line_color='rgba(150,150,150,0.5)', name='Плотность f(x)'))
    
    if val is not None and 0 <= val <= 1:
        x_calc = a + val * (b - a)
        fig.add_trace(go.Scatter(x=[a, x_calc, x_calc, a, a], y=[0, 0, height, height, 0], fill='toself', mode='lines', fillcolor='rgba(0, 200, 100, 0.6)', line_color='green', name='Доля вероятности'))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Равномерное распределение")
    st.plotly_chart(fig, use_container_width=True)

def draw_exponential_simulation(ans_str, task_data):
    lam = task_data.get('lam', 0.02)
    val = parse_float(ans_str)
    
    t_max = int(5 / lam)
    t_vals = list(range(0, t_max, max(1, t_max//50)))
    r_vals = [math.exp(-lam * t) for t in t_vals]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=r_vals, mode='lines', line=dict(color='blue', width=3), name='R(t) / F(t)'))
    
    if val is not None and 0 <= val <= 1:
        fig.add_trace(go.Scatter(x=[0, t_max], y=[val, val], mode='lines', line=dict(color='green', dash='dash'), name='Ваш ответ'))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Показательное распределение")
    st.plotly_chart(fig, use_container_width=True)

def draw_normal_simulation(ans_str):
    val = parse_float(ans_str)
    
    x = [i/10.0 for i in range(-40, 41)]
    y = [math.exp(-0.5 * ((v/10)**2)) for v in x]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='rgba(100,150,250,0.8)', width=3), name='f(x)'))
    
    if val is not None and 0 <= val <= 1:
        center = len(x) // 2
        limit = int((len(x) / 2) * val)
        fill_x = x[center-limit:center+limit+1]
        fill_y = y[center-limit:center+limit+1]
        if fill_x:
            fig.add_trace(go.Scatter(x=fill_x, y=fill_y, fill='tozeroy', mode='none', fillcolor='rgba(0, 200, 100, 0.5)', name='Ваша площадь'))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Нормальное распределение", xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    st.plotly_chart(fig, use_container_width=True)

def draw_threesigma_simulation(ans_str, task_data):
    a = task_data.get('a', 500)
    sig = task_data.get('sigma', 20)
    
    x = list(range(a - 4*sig, a + 4*sig))
    y = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in x]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='gray', width=2), name='Трафик'))
    
    parts = str(ans_str).split()
    if len(parts) >= 2:
        try:
            s_min, s_max = float(parts[0]), float(parts[1])
            fill_x = [v for v in x if s_min <= v <= s_max]
            fill_y = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in fill_x]
            if fill_x:
                fig.add_trace(go.Scatter(x=fill_x, y=fill_y, fill='tozeroy', mode='none', fillcolor='rgba(0, 200, 100, 0.4)', name='Ваш интервал'))
            
            anom_x1 = [v for v in x if v < s_min]
            anom_y1 = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in anom_x1]
            if anom_x1:
                fig.add_trace(go.Scatter(x=anom_x1, y=anom_y1, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', showlegend=False))
                
            anom_x2 = [v for v in x if v > s_max]
            anom_y2 = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in anom_x2]
            if anom_x2:
                fig.add_trace(go.Scatter(x=anom_x2, y=anom_y2, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', showlegend=False))
        except:
            pass

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Правило 3 Сигм")
    st.plotly_chart(fig, use_container_width=True)

if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.student_id = ""
    st.session_state.start_time = None
    st.session_state.report_json = None
    st.session_state.filename = ""
    st.session_state.sent_to_cloud = False

if not st.session_state.started:
    st.title("📉 Практическая работа №4 - ТВиМС")
    st.write("Непрерывные случайные величины (НСВ) и законы их распределения")
    
    with st.container():
        st.info("Введите номер вашей зачетной книжки. От этого номера зависит ваш уникальный вариант.")
        student_id_input = st.text_input("Номер зачетной книжки:", placeholder="Например: 220156")
        
        if st.button("🚀 Начать практику", use_container_width=True):
            if student_id_input.strip():
                st.session_state.student_id = student_id_input.strip()
                st.session_state.started = True
                st.session_state.start_time = datetime.now()
                st.rerun()
            else:
                st.error("Поле не может быть пустым!")

elif st.session_state.started and st.session_state.report_json is None:
    st.title(f"🎓 Практика №4 | Зачетка: {st.session_state.student_id}")
    
    engine = PracticeEngine(st.session_state.student_id)
    variant = engine.generate_variant()
    
    st.warning("⚠️ Для зачета каждой задачи ОБЯЗАТЕЛЬНО необходимо прикрепить фотографию рукописного решения! Можно прикреплять несколько фото.")
    
    if 'student_answers' not in st.session_state:
        st.session_state.student_answers = {}
    if 'student_photos' not in st.session_state:
        st.session_state.student_photos = {}

    for task_key, task_data in variant.items():
        st.divider()
        if task_key == 'task_99':
            st.markdown(f"### 📝 {task_data['title']}")
            st.write(task_data['text'])
            ans = st.text_input("Краткий комментарий (необязательно):", key=f"ans_{task_key}")
            st.session_state.student_answers[task_key] = ans
            photos = st.file_uploader("📸 Прикрепить фото с ответами (можно несколько)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"photo_{task_key}")
            st.session_state.student_photos[task_key] = photos
        else:
            task_num = task_key.split('_')[1]
            st.markdown(f"### 🔹 Задача {task_num}")
            st.write(task_data['text'])
            
            ans = st.text_input("Ваш ответ:", key=f"ans_{task_key}")
            st.session_state.student_answers[task_key] = ans
            
            t_type = task_data.get('type')
            if t_type == 'uniform':
                draw_uniform_simulation(ans, task_data)
            elif t_type == 'exponential':
                draw_exponential_simulation(ans, task_data)
            elif t_type == 'normal':
                draw_normal_simulation(ans)
            elif t_type == '3sigma':
                draw_threesigma_simulation(ans, task_data)
                
            photos = st.file_uploader("📸 Прикрепить решение (можно несколько фото)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"photo_{task_key}")
            st.session_state.student_photos[task_key] = photos
        
    st.divider()
    if st.button("✅ Завершить и отправить преподавателю", use_container_width=True, type="primary"):
        delta = datetime.now() - st.session_state.start_time
        mins = int(delta.total_seconds() // 60)
        secs = int(delta.total_seconds() % 60)
        time_spent_str = f"{mins} мин. {secs} сек."
        
        student_answers_raw = {}
        encrypted_answers = {}
        
        for k, text_val in st.session_state.student_answers.items():
            raw_val = text_val.strip().replace(',', '.')
            student_answers_raw[k] = raw_val
            encrypted_answers[k] = base64.b64encode(raw_val[::-1].encode('utf-8')).decode('utf-8')
            
        for k, file_list in st.session_state.student_photos.items():
            if file_list: 
                compressed_photos = []
                encrypted_photos = []
                for file in file_list:
                    img = Image.open(file).convert("RGB")
                    img.thumbnail((1200, 1200))
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=75)
                    b64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    compressed_photos.append(b64_str)
                    encrypted_photos.append(base64.b64encode(b64_str[::-1].encode('utf-8')).decode('utf-8'))
                
                student_answers_raw[f"{k}_photo"] = compressed_photos
                encrypted_answers[f"{k}_photo"] = encrypted_photos
                
        security_hash = engine.generate_security_hash(engine.student_id, student_answers_raw)
        
        report_data = {
            "student_id": engine.student_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time_spent": time_spent_str,
            "answers": encrypted_answers,
            "verification_key": security_hash
        }
        
        st.session_state.report_json = json.dumps(report_data, ensure_ascii=False, indent=4)
        time_tag = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        st.session_state.filename = f"Отчет_Практика4_{engine.student_id}_{time_tag}.json"
        st.rerun()

if st.session_state.get('report_json') is not None:
    st.title("🎉 Работа успешно завершена!")
    
    if not st.session_state.get('sent_to_cloud', False):
        with st.spinner("⏳ Идет отправка отчета на Google Диск преподавателя..."):
            success = upload_to_google_drive(st.session_state.report_json, st.session_state.filename)
            if success:
                st.session_state.sent_to_cloud = True
                st.rerun()
                
    if st.session_state.get('sent_to_cloud', False):
        st.success("✅ Отчет успешно отправлен преподавателю в облако! Все данные и фотографии зафиксированы.")
        st.info("Вы можете закрыть эту вкладку.")
        
    if st.button("Пройти заново / Сменить зачетку"):
        st.session_state.started = False
        st.session_state.report_json = None
        st.session_state.sent_to_cloud = False
        st.rerun()
