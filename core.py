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
        
        # --- БЛОК 1: Комбинаторика (Перестановки, размещения, сочетания) (Задачи 1 - 5) ---
        
        # Задача 1: Перестановки
        n1 = random.randint(5, 8)
        variant['task_1'] = {
            'text': f"Сколькими различными способами можно расставить на серверной стойке {n1} уникальных коммутационных модулей в ряд? (Введите целое число).",
            'answer': str(math.factorial(n1))
        }

        # Задача 2: Размещения
        n2 = random.randint(8, 12)
        k2 = random.randint(3, 5)
        variant['task_2'] = {
            'text': f"Из {n2} сетевых администраторов нужно выбрать начальника отдела, заместителя и ведущего инженера. Сколькими способами это можно сделать? (Введите целое число).",
            'answer': str(math.perm(n2, k2))
        }

        # Задача 3: Сочетания
        n3 = random.randint(10, 16)
        k3 = random.randint(3, 6)
        variant['task_3'] = {
            'text': f"В группе из {n3} студентов для тестирования новой сетевой утилиты выбирают комиссию из {k3} человек. Сколькими способами можно сформировать такую комиссию? (Введите целое число).",
            'answer': str(math.comb(n3, k3))
        }

        # Задача 4: Перестановки с повторениями (или буквы/символы)
        n4_a = random.randint(2, 4)
        n4_b = random.randint(2, 3)
        n4_c = 2
        total_letters = n4_a + n4_b + n4_c
        variant['task_4'] = {
            'text': f"Сколько различных «слов» (последовательностей символов) можно составить, переставляя буквы в сетевом идентификаторе, состоящем из {n4_a} букв 'A', {n4_b} букв 'B' и {n4_c} букв 'C'? (Введите целое число).",
            'answer': str(math.factorial(total_letters) // (math.factorial(n4_a) * math.factorial(n4_b) * math.factorial(n4_c)))
        }

        # Задача 5: Круговые перестановки или формула выбора
        n5 = random.randint(6, 10)
        k5 = random.randint(2, 4)
        variant['task_5'] = {
            'text': f"На защищенном канале связи требуется составить кодовую комбинацию из {k5} различных цифр, выбранных из набора в {n5} доступных цифр. Сколькими способами это можно сделать с учетом порядка? (Введите целое число).",
            'answer': str(math.perm(n5, k5))
        }

        # --- БЛОК 2: Классическое определение вероятности (Задачи 6 - 10) ---
        
        # Задача 6: Классическая вероятность с деталями
        n6_total = random.randint(20, 35)
        n6_defect = random.randint(3, 7)
        n6_draw = random.randint(2, 4)
        variant['task_6'] = {
            'text': f"В партии из {n6_total} трансиверов имеется {n6_defect} бракованных. Наудачу выбирают {n6_draw} трансивера. Найти вероятность того, что все выбранные трансиверы исправны. (Округление до 4 знаков).",
            'answer': str(round(math.comb(n6_total - n6_defect, n6_draw) / math.comb(n6_total, n6_draw), 4))
        }

        # Задача 7
        n7_w = random.randint(5, 10)
        n7_b = random.randint(5, 10)
        tot7 = n7_w + n7_b
        k7 = random.randint(2, 3)
        variant['task_7'] = {
            'text': f"В сетевом узле хранятся {n7_w} IPv4 и {n7_b} IPv6 адресов. Администратор случайно запрашивает {k7} адресов. Какова вероятность, что среди них ровно 1 адрес IPv4? (Округление до 4 знаков).",
            'answer': str(round((math.comb(n7_w, 1) * math.comb(n7_b, k7 - 1)) / math.comb(tot7, k7), 4))
        }

        # Задача 8
        n8 = random.randint(10, 15)
        variant['task_8'] = {
            'text': f"Студент выучил {n8} битов из 20. В билете 2 вопроса. Какова вероятность, что студент знает оба вопроса билета? (Округление до 4 знаков).",
            'answer': str(round(math.comb(n8, 2) / math.comb(20, 2), 4))
        }

        # Задача 9
        n9 = random.randint(5, 8)
        variant['task_9'] = {
            'text': f"В лифт на первом этаже зашли {n9} человек. Лифт останавливается на {n9} этажах. Какова вероятность, что все выйдут на разных этажах? (Округление до 4 знаков).",
            'answer': str(round(math.factorial(n9) / (n9 ** n9), 4))
        }

        # Задача 10
        n10 = random.randint(4, 7)
        variant['task_10'] = {
            'text': f"Наудачу набирается секретный пин-код из {n10} цифр (цифры не повторяются). Какова вероятность угадать его с первой попытки? (Округление до 4 знаков).",
            'answer': str(round(1 / math.perm(10, n10), 4))
        }

        # --- БЛОК 3: Теоремы сложения и умножения вероятностей (Задачи 11 - 15) ---
        
        # Задача 11
        p11_1 = round(random.uniform(0.7, 0.9), 2)
        p11_2 = round(random.uniform(0.6, 0.8), 2)
        variant['task_11'] = {
            'text': f"Вероятности отказа двух независимых модулей равны {round(1-p11_1, 2)} и {round(1-p11_2, 2)}. Найти вероятность отказа системы, если модули соединены последовательно.",
            'answer': str(round(1 - (p11_1 * p11_2), 4))
        }

        # Задача 12
        p12_1 = round(random.uniform(0.7, 0.9), 2)
        p12_2 = round(random.uniform(0.6, 0.8), 2)
        variant['task_12'] = {
            'text': f"Два независимых канала связи работают с надежностью {p12_1} и {p12_2}. Найти вероятность безотказной работы хотя бы одного канала.",
            'answer': str(round(p12_1 + p12_2 - (p12_1 * p12_2), 4))
        }

        # Задача 13
        p13_1 = round(random.uniform(0.8, 0.95), 2)
        p13_2 = round(random.uniform(0.75, 0.9), 2)
        p13_3 = round(random.uniform(0.7, 0.85), 2)
        variant['task_13'] = {
            'text': f"Три независимых прибора имеют надежности {p13_1}, {p13_2} и {p13_3}. Найти вероятность того, что откажут ровно два прибора.",
            'answer': str(round((1-p13_1)*(1-p13_2)*p13_3 + (1-p13_1)*p13_3*(1-p13_2) + p13_1*(1-p13_2)*(1-p13_3), 4))
        }

        # Задача 14
        p14_1 = round(random.uniform(0.6, 0.8), 2)
        p14_2 = round(random.uniform(0.5, 0.7), 2)
        variant['task_14'] = {
            'text': f"Два оператора обрабатывают заявки. Вероятность успешной обработки первым равна {p14_1}, вторым — {p14_2}. Найти вероятность успешной обработки ровно одним оператором.",
            'answer': str(round(p14_1*(1-p14_2) + p14_2*(1-p14_1), 4))
        }

        # Задача 15
        p15 = round(random.uniform(0.7, 0.9), 2)
        variant['task_15'] = {
            'text': f"Сервер успешно обрабатывает запрос с вероятностью {p15}. Какова вероятность, что из 3 независимых запросов успешными будут ровно 2?",
            'answer': str(round(3 * (p15**2) * (1 - p15), 4))
        }

        # --- БЛОК 4: Полная вероятность и формула Байеса (Задачи 16 - 20) ---
        
        # Задача 16
        s1, s2 = random.randint(10, 20), random.randint(15, 25)
        p16_1 = round(random.uniform(0.8, 0.95), 2)
        p16_2 = round(random.uniform(0.5, 0.7), 2)
        tot16 = s1 + s2
        res16 = (s1/tot16)*p16_1 + (s2/tot16)*p16_2
        variant['task_16'] = {
            'text': f"В первой группе {s1} серверов (надежность {p16_1}), во второй {s2} серверов (надежность {p16_2}). Запрос случайным образом направляется на одну из групп. Найти полную вероятность успешной обработки запроса.",
            'answer': str(round(res16, 4))
        }

        # Задача 17
        variant['task_17'] = {
            'text': f"Используя условия предыдущей задачи, запрос был успешно обработан. Найти вероятность того, что он был направлен на первую группу серверов (формула Байеса).",
            'answer': str(round(((s1/tot16)*p16_1) / res16, 4))
        }

        # Задача 18
        sh1, sh2, sh3 = 3, 5, 2
        t18 = sh1 + sh2 + sh3
        variant['task_18'] = {
            'text': f"Три дата-центра содержат {sh1}, {sh2} и {sh3} стоек. Вероятности сбоя в них равны 0.05, 0.1 и 0.2 соответственно. Найти общую вероятность сбоя при обращении к случайной стойке.",
            'answer': str(round((sh1/t18)*0.05 + (sh2/t18)*0.1 + (sh3/t18)*0.2, 4))
        }

        # Задача 19
        variant['task_19'] = {
            'text': f"Студент может сдать экзамен у трех преподавателей с равными вероятностями. Вероятности сдать у них: 0.9, 0.6 и 0.4. Студент сдал экзамен. Какова вероятность, что он сдавал первому преподавателю?",
            'answer': str(round((1/3 * 0.9) / (1/3*0.9 + 1/3*0.6 + 1/3*0.4), 4))
        }

        # Задача 20
        variant['task_20'] = {
            'text': f"В специализированном узле 70% устройств первого класса и 30% второго. Вероятность безотказной работы для них 0.95 и 0.8. Наудачу выбранное устройство вышло из строя. Какова вероятность, что оно было второго класса?",
            'answer': str(round((0.3 * 0.2) / (0.7 * 0.05 + 0.3 * 0.2), 4))
        }

        # Контрольный теоретический вопрос
        cq_pool = [
            "Дайте определения основных комбинаторных соединений: перестановок, размещений и сочетаний. Напишите их формулы.",
            "Дайте классическое определение вероятности события. Каковы его основные свойства?",
            "В чем различие между совместными и несовместными событиями? Приведите примеры.",
            "Сформулируйте теорему умножения вероятностей для зависимых и независимых событий.",
            "Запишите и объясните формулу полной вероятности и формулу Байеса."
        ]
        variant['task_99'] = {
            'title': 'Контрольный теоретический вопрос',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на вопрос:\n\n{random.choice(cq_pool)}",
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
