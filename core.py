# -*- coding: utf-8 -*-
import random
import math
import hashlib
import json

SECRET_SALT = "Ural_Telecom_2026_Secret"

class PracticeEngine:
    def __init__(self, student_id: str):
        self.student_id = student_id.strip().upper()
        self.seed = self._generate_seed()
        random.seed(self.seed)

    def _generate_seed(self):
        hash_obj = hashlib.md5(self.student_id.encode())
        return int(hash_obj.hexdigest(), 16)

    def generate_variant(self) -> dict:
        variant = {}
        
        # Задача 1: Классическая вероятность / Комбинаторика
        n_total = random.randint(15, 25)
        k_defect = random.randint(3, 6)
        k_draw = random.randint(2, 4)
        variant['task_1'] = {
            'text': f"На серверной стойке находится {n_total} коммутаторных блоков, из которых {k_defect} имеют скрытый заводской брак. Системный администратор случайно выбирает для тестирования {k_draw} блока. Найти вероятность того, что ровно 1 блок из выбранных окажется бракованным. (Ответ округлите до 4 знаков).",
            'answer': str(round((math.comb(k_defect, 1) * math.comb(n_total - k_defect, k_draw - 1)) / math.comb(n_total, k_draw), 4))
        }

        # Задача 2: Теорема сложения вероятностей
        p1 = round(random.uniform(0.75, 0.90), 2)
        p2 = round(random.uniform(0.70, 0.85), 2)
        variant['task_2'] = {
            'text': f"Надежность (безотказная работа в течение суток) первого канала связи равна {p1}, а второго независимого резервного канала — {p2}. Найти вероятность того, что в течение суток будет работать ХОТЯ БЫ ОДИН канал. (Ответ округлите до 4 знаков).",
            'answer': str(round(p1 + p2 - (p1 * p2), 4))
        }

        # Задача 3: Теорема умножения вероятностей
        n_white = random.randint(5, 10)
        n_black = random.randint(4, 8)
        total_balls = n_white + n_black
        variant['task_3'] = {
            'text': f"В сетевом узле хранятся IP-адреса: {n_white} валидных и {n_black} заблокированных. Администратор последовательно (без возвращения) запрашивает 2 адреса. Какова вероятность того, что оба запрошенных адреса окажутся валидными? (Ответ округлите до 4 знаков).",
            'answer': str(round((n_white / total_balls) * ((n_white - 1) / (total_balls - 1)), 4))
        }

        # Задача 4: Формула полной вероятности
        s1 = random.randint(3, 5)
        s2 = random.randint(4, 6)
        s3 = random.randint(3, 7)
        total_srv = s1 + s2 + s3
        
        eff1 = round(random.uniform(0.95, 0.99), 2)
        eff2 = round(random.uniform(0.85, 0.92), 2)
        eff3 = round(random.uniform(0.70, 0.80), 2)
        
        total_prob = (s1/total_srv)*eff1 + (s2/total_srv)*eff2 + (s3/total_srv)*eff3
        variant['task_4'] = {
            'text': f"Дата-центр обрабатывает запросы с трех серверных групп: первая группа включает {s1} сервера (вероятность сбоя обработки {eff1}), вторая — {s2} сервера (вероятность {eff2}), третья — {s3} сервера (вероятность {eff3}). Найти общую полную вероятность успешной обработки случайного запроса. (Ответ округлите до 4 знаков).",
            'answer': str(round(total_prob, 4))
        }

        # Теоретический вопрос
        cq_pool = [
            "Дайте классическое определение вероятности события. Каковы его основные свойства?",
            "В чем различие между совместными и несовместными событиями? Приведите примеры из IT.",
            "Сформулируйте теорему умножения вероятностей для зависимых и независимых событий.",
            "Запишите и объясните формулу полной вероятности и теорему Байеса."
        ]
        selected_q = random.choice(cq_pool)
        variant['task_99'] = {
            'title': 'Контрольный теоретический вопрос',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на вопрос:\n\n1. {selected_q}",
            'answer': 'Ручная проверка (Требуется фото)'
        }
        
        return variant

    @staticmethod
    def generate_security_hash(student_id: str, student_answers: dict) -> str:
        answers_str = json.dumps(student_answers, sort_keys=True)
        raw_data = f"{student_id}_{answers_str}_{SECRET_SALT}"
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    def check_answers(self, student_answers: dict) -> dict:
        variant = self.generate_variant()
        correct_count = 0
        total_count = len(variant)
        details = {}

        def is_close(val1, val2, tol=0.005):
            try:
                return abs(float(val1) - float(val2)) <= tol
            except ValueError:
                return str(val1).strip().lower() == str(val2).strip().lower()

        for task_key, task_data in variant.items():
            photo_list = student_answers.get(f"{task_key}_photo", [])
            has_photo = bool(photo_list)
            
            student_ans_str = student_answers.get(task_key, "").strip().replace(',', '.')
            correct_ans_str = str(task_data.get('answer', ''))
            
            if task_key == 'task_99':
                if has_photo:
                    is_correct = True
                    correct_count += 1
                    details[task_key] = {'is_correct': True, 'correct_answer': "Фото прикреплено", 'student_answer': f"Фото ({len(photo_list)} шт.)"}
                else:
                    details[task_key] = {'is_correct': False, 'correct_answer': "Требуется фото", 'student_answer': "Нет фото!"}
                continue

            is_correct = is_close(student_ans_str, correct_ans_str)
            if not has_photo:
                is_correct = False
                student_ans_str = f"{student_ans_str} (Нет фото!)" if student_ans_str else "Нет ответа (Нет фото!)"

            if is_correct: correct_count += 1
            details[task_key] = {'is_correct': is_correct, 'correct_answer': correct_ans_str, 'student_answer': student_ans_str}

        score_percent = (correct_count / total_count) * 100
        if score_percent >= 85: mark = 5
        elif score_percent >= 70: mark = 4
        elif score_percent >= 50: mark = 3
        else: mark = 2

        photos_dict = {k: student_answers.get(f"{k}_photo") for k in variant.keys() if student_answers.get(f"{k}_photo")}

        return {
            'correct_count': correct_count,
            'total_count': total_count,
            'percent': round(score_percent, 1),
            'mark': mark,
            'details': details,
            'photos': photos_dict
        }
