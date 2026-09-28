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
        
        # --- БЛОК 1: Классическая вероятность и комбинаторика (Задачи 1 - 5) ---
        
        # Задача 1
        n1 = random.randint(15, 25)
        k1 = random.randint(3, 6)
        m1 = random.randint(2, 3)
        variant['task_1'] = {
            'text': f"На сервере {n1} портов, из них {k1} с дефектами. Администратор проверяет {m1} порта. Найти вероятность того, что среди них ровно 1 дефектный. (Округление до 4 знаков).",
            'answer': str(round((math.comb(k1, 1) * math.comb(n1 - k1, m1 - 1)) / math.comb(n1, m1), 4))
        }

        # Задача 2
        n2_w = random.randint(6, 10)
        n2_b = random.randint(4, 7)
        tot2 = n2_w + n2_b
        k2 = random.randint(2, 3)
        variant['task_2'] = {
            'text': f"В узле {n2_w} белых и {n2_b} черных пакетных файлов. Наудачу берут {k2}. Какова вероятность, что все они белые? (Округление до 4 знаков).",
            'answer': str(round(math.comb(n2_w, k2) / math.comb(tot2, k2), 4))
        }

        # Задача 3
        n3 = random.randint(8, 12)
        variant['task_3'] = {
            'text': f"Студент выучил {n3} битов информации из 20. В билете 2 вопроса. Найти вероятность того, что студент ответит на оба вопроса. (Округление до 4 знаков).",
            'answer': str(round(math.comb(n3, 2) / math.comb(20, 2), 4))
        }

        # Задача 4
        n4 = random.randint(5, 8)
        variant['task_4'] = {
            'text': f"В лифт на первом этаже зашли {n4} человек. Лифт останавливается на {n4} этажах. Какова вероятность, что все выйдут на разных этажах? (Округление до 4 знаков).",
            'answer': str(round(math.factorial(n4) / (n4 ** n4), 4))
        }

        # Задача 5
        n5 = random.randint(4, 7)
        variant['task_5'] = {
            'text': f"Набирается пароль из {n5} цифр наудачу. Какова вероятность угадать все цифры, если они не повторяются? (Округление до 4 знаков).",
            'answer': str(round(1 / math.perm(10, n5), 4))
        }

        # --- БЛОК 2: Теоремы сложения и умножения (Задачи 6 - 10) ---
        
        # Задача 6
        p6_1 = round(random.uniform(0.7, 0.9), 2)
        p6_2 = round(random.uniform(0.6, 0.8), 2)
        variant['task_6'] = {
            'text': f"Вероятности отказа двух независимых модулей равны {1-p6_1:.2f} и {1-p6_2:.2f}. Найти вероятность отказа системы, если модули соединены последовательно.",
            'answer': str(round(1 - (p6_1 * p6_2), 4))
        }

        # Задача 7
        p7_1 = round(random.uniform(0.7, 0.9), 2)
        p7_2 = round(random.uniform(0.6, 0.8), 2)
        variant['task_7'] = {
            'text': f"Два независимых канала работают с надежностью {p7_1} и {p7_2}. Найти вероятность безотказной работы хотя бы одного канала.",
            'answer': str(round(p7_1 + p7_2 - (p7_1 * p7_2), 4))
        }

        # Задача 8
        p8_1 = round(random.uniform(0.8, 0.95), 2)
        p8_2 = round(random.uniform(0.75, 0.9), 2)
        p8_3 = round(random.uniform(0.7, 0.85), 2)
        variant['task_8'] = {
            'text': f"Три независимых прибора имеют надежности {p8_1}, {p8_2} и {p8_3}. Найти вероятность того, что откажут ровно два прибора.",
            'answer': str(round((1-p8_1)*(1-p8_2)*p8_3 + (1-p8_1)*p8_3*(1-p8_2) + p8_1*(1-p8_2)*(1-p8_3), 4))
        }

        # Задача 9
        p9_1 = round(random.uniform(0.6, 0.8), 2)
        p9_2 = round(random.uniform(0.5, 0.7), 2)
        variant['task_9'] = {
            'text': f"Два стрелка стреляют по мишени. Вероятность попадания первого {p9_1}, второго — {p9_2}. Найти вероятность ровно одного попадания.",
            'answer': str(round(p9_1*(1-p9_2) + p9_2*(1-p9_1), 4))
        }

        # Задача 10
        p10 = round(random.uniform(0.7, 0.9), 2)
        variant['task_10'] = {
            'text': f"Автомобиль проезжает перекресток с вероятностью {p10}. Какова вероятность, что из 3 проездов успешными будут ровно 2?",
            'answer': str(round(3 * (p10**2) * (1 - p10), 4))
        }

        # --- БЛОК 3: Полная вероятность и формула Байеса (Задачи 11 - 15) ---
        
        # Задача 11
        s1, s2 = random.randint(10, 20), random.randint(15, 25)
        p11_1 = round(random.uniform(0.8, 0.95), 2)
        p11_2 = round(random.uniform(0.5, 0.7), 2)
        tot11 = s1 + s2
        res11 = (s1/tot11)*p11_1 + (s2/tot11)*p11_2
        variant['task_11'] = {
            'text': f"В первой урне {s1} деталей (доля брака {1-p11_1:.2f}), во второй {s2} деталей (доля брака {1-p11_2:.2f}). Наудачу берут урну и из нее деталь. Найти полную вероятность того, что деталь бракованная.",
            'answer': str(round(1 - res11, 4))
        }

        # Задача 12
        variant['task_12'] = {
            'text': f"На базе {s1} деталей первого завода и {s2} второго. Качество первого {p11_1}, второго {p11_2}. Найти вероятность того, что наудачу взятая деталь стандартна.",
            'answer': str(round(res11, 4))
        }

        # Задача 13
        variant['task_13'] = {
            'text': f"Используя условия задач выше, взятая деталь оказалась качественной. Найти апостериорную вероятность того, что она была из первой группы (Байеса).",
            'answer': str(round(((s1/tot11)*p11_1) / res11, 4))
        }

        # Задача 14
        sh1, sh2, sh3 = 3, 5, 2
        t14 = sh1 + sh2 + sh3
        variant['task_14'] = {
            'text': f"Три партии деталей: {sh1}, {sh2} и {sh3} штук. Вероятности брака 0.05, 0.1 и 0.2 соответственно. Найти вероятность появления стандартной детали.",
            'answer': str(round((sh1/t14)*0.95 + (sh2/t14)*0.9 + (sh3/t14)*0.8, 4))
        }

        # Задача 15
        variant['task_15'] = {
            'text': f"Студент может сдать экзамен у трех преподавателей с равными вероятностями. Вероятности сдать у них: 0.9, 0.6 и 0.4. Студент сдал экзамен. Какова вероятность, что он сдавал первому преподавателю?",
            'answer': str(round((1/3 * 0.9) / (1/3*0.9 + 1/3*0.6 + 1/3*0.4), 4))
        }

        # --- БЛОК 4: Повторные независимые испытания (Задачи 16 - 20) ---
        
        # Задача 16
        n16 = 5
        p16 = 0.4
        variant['task_16'] = {
            'text': f"Монета подброшена 5 раз. Какова вероятность выпадения герба ровно 3 раза?",
            'answer': str(round(math.comb(5, 3) * (0.4**3) * (0.6**2), 4))
        }

        # Задача 17
        variant['task_17'] = {
            'text': f"Стрелок попадает с вероятностью 0.8. Сделано 4 выстрела. Найти вероятность ровно 2 попаданий.",
            'answer': str(round(math.comb(4, 2) * (0.8**2) * (0.2**2), 4))
        }

        # Задача 18
        variant['task_18'] = {
            'text': f"Вероятность брака 0.1. Проверено 4 детали. Какова вероятность наличия ровно 1 бракованной?",
            'answer': str(round(math.comb(4, 1) * 0.1 * (0.9**3), 4))
        }

        # Задача 19
        variant['task_19'] = {
            'text': f"Вероятность успеха в испытании 0.5. Найти вероятность того, что в 6 испытаниях успех будет от 3 до 5 раз.",
            'answer': str(round(sum(math.comb(6, k) * (0.5**6) for k in range(3, 6)), 4))
        }

        # Задача 20
        variant['task_20'] = {
            'text': f"Какова вероятность появления события не менее 2 раз в 4 независимых испытаниях, если вероятность успеха равна 0.3?",
            'answer': str(round(1 - (math.comb(4, 0)*(0.7**4) + math.comb(4, 1)*0.3*(0.7**3)), 4))
        }

        # Контрольный теоретический вопрос
        cq_pool = [
            "Дайте классическое определение вероятности события. Каковы его основные свойства?",
            "В чем различие между совместными и несовместными событиями? Приведите примеры.",
            "Сформулируйте теорему умножения вероятностей для зависимых и независимых событий.",
            "Запишите и объясните формулу полной вероятности и формулу Байеса.",
            "Сформулируйте теорему сложения вероятностей совместных и несовместных событий."
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
