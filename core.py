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
        rng = random.Random(self.seed)
        pool = []

        # 1. Комбинаторика: Перестановки
        n1 = rng.randint(5, 8)
        pool.append({
            'text': f"Сколькими различными способами можно расставить на серверной стойке {n1} уникальных коммутационных модулей в ряд? (Введите целое число).",
            'answer': str(math.factorial(n1))
        })

        # 2. Комбинаторика: Размещения
        n2 = rng.randint(8, 12)
        k2 = rng.randint(3, 5)
        pool.append({
            'text': f"Из {n2} сетевых администраторов нужно выбрать начальника отдела, заместителя и ведущего инженера. Сколькими способами это можно сделать? (Введите целое число).",
            'answer': str(math.perm(n2, k2))
        })

        # 3. Комбинаторика: Сочетания
        n3 = rng.randint(10, 16)
        k3 = rng.randint(3, 6)
        pool.append({
            'text': f"В группе из {n3} студентов для тестирования новой сетевой утилиты выбирают комиссию из {k3} человек. Сколькими способами можно сформировать такую комиссию? (Введите целое число).",
            'answer': str(math.comb(n3, k3))
        })

        # 4. Комбинаторика: Перестановки с повторениями
        n4_a = rng.randint(2, 4)
        n4_b = rng.randint(2, 3)
        n4_c = 2
        tot_let = n4_a + n4_b + n4_c
        pool.append({
            'text': f"Сколько различных «слов» можно составить, переставляя буквы в сетевом идентификаторе, состоящем из {n4_a} букв 'A', {n4_b} букв 'B' и {n4_c} букв 'C'? (Введите целое число).",
            'answer': str(math.factorial(tot_let) // (math.factorial(n4_a) * math.factorial(n4_b) * math.factorial(n4_c)))
        })

        # 5. Смешанный тип: Детали / бракованные блоки
        n5_tot = rng.randint(18, 25)
        n5_def = rng.randint(3, 6)
        n5_dr = rng.randint(2, 4)
        pool.append({
            'text': f"В партии из {n5_tot} серверных блоков содержится {n5_def} бракованных. Системный администратор случайно выбирает для проверки {n5_dr} блока. Найти вероятность того, что среди выбранных блоков окажется ровно 1 бракованный. (Округление до 4 знаков).",
            'answer': str(round((math.comb(n5_def, 1) * math.comb(n5_tot - n5_def, n5_dr - 1)) / math.comb(n5_tot, n5_dr), 4))
        })

        # 6. Классическая вероятность: IP-адреса
        n6_w = rng.randint(6, 10)
        n6_b = rng.randint(5, 9)
        tot6 = n6_w + n6_b
        k6 = rng.randint(2, 3)
        pool.append({
            'text': f"В сетевом узле хранятся {n6_w} валидных и {n6_b} заблокированных IP-адресов. Администратор случайно запрашивает {k6} адреса. Какова вероятность, что все запрошенные адреса окажутся валидными? (Округление до 4 знаков).",
            'answer': str(round(math.comb(n6_w, k6) / math.comb(tot6, k6), 4))
        })

        # 7. Смешанный тип: Выборка по типам (IPv4 / IPv6)
        n7_v4 = rng.randint(6, 10)
        n7_v6 = rng.randint(6, 10)
        tot7 = n7_v4 + n7_v6
        k7 = rng.randint(2, 4)
        pool.append({
            'text': f"В базе данных {n7_v4} записей IPv4 и {n7_v6} записей IPv6. Администратор выбирает случайным образом {k7} записей. Найти вероятность того, что ровно 2 записи окажутся формата IPv4. (Округление до 4 знаков).",
            'answer': str(round((math.comb(n7_v4, 2) * math.comb(n7_v6, k7 - 2)) / math.comb(tot7, k7), 4))
        })

        # 8. Классическая вероятность: Билеты
        n8_learn = rng.randint(10, 16)
        pool.append({
            'text': f"Студент выучил {n8_learn} битов из 20. В экзаменационном билете содержатся 2 вопроса. Какова вероятность того, что студент знает оба вопроса выпавшего билета? (Округление до 4 знаков).",
            'answer': str(round(math.comb(n8_learn, 2) / math.comb(20, 2), 4))
        })

        # 9. Классическая вероятность: Лифт / Этажи
        n9 = rng.randint(5, 8)
        pool.append({
            'text': f"В лифт на первом этаже жилого дома зашли {n9} человек. Лифт может останавливаться на {n9} этажах. Какова вероятность, что все пассажиры выйдут на разных этажах? (Округление до 4 знаков).",
            'answer': str(round(math.factorial(n9) / (n9 ** n9), 4))
        })

        # 10. Комбинаторика + Вероятность: Пин-коды
        n10_dig = rng.randint(4, 6)
        pool.append({
            'text': f"Наудачу набирается цифровой пин-код из {n10_dig} уникальных цифр (цифры не повторяются, выбираются из 10 возможных). Какова вероятность угадать верную комбинацию с первой попытки? (Округление до 4 знаков).",
            'answer': str(round(1 / math.perm(10, n10_dig), 4))
        })

        # 11. Теоремы вероятностей: Последовательное соединение
        p11_1 = round(rng.uniform(0.7, 0.9), 2)
        p11_2 = round(rng.uniform(0.6, 0.8), 2)
        pool.append({
            'text': f"Вероятности отказа двух независимых модулей равны {round(1-p11_1, 2)} и {round(1-p11_2, 2)}. Найти вероятность отказа всей системы, если модули соединены последовательно. (Округление до 4 знаков).",
            'answer': str(round(1 - (p11_1 * p11_2), 4))
        })

        # 12. Теоремы вероятностей: Параллельное соединение
        p12_1 = round(rng.uniform(0.7, 0.9), 2)
        p12_2 = round(rng.uniform(0.6, 0.8), 2)
        pool.append({
            'text': f"Два независимых канала связи работают с надежностью {p12_1} и {p12_2}. Найти вероятность безотказной работы хотя бы одного канала в системе. (Округление до 4 знаков).",
            'answer': str(round(p12_1 + p12_2 - (p12_1 * p12_2), 4))
        })

        # 13. Теоремы вероятностей: Ровно два отказа
        p13_1 = round(rng.uniform(0.8, 0.95), 2)
        p13_2 = round(rng.uniform(0.75, 0.9), 2)
        p13_3 = round(rng.uniform(0.7, 0.85), 2)
        pool.append({
            'text': f"Три независимых прибора имеют надежности {p13_1}, {p13_2} и {p13_3}. Найти вероятность того, что из строя выйдут ровно два прибора. (Округление до 4 знаков).",
            'answer': str(round((1-p13_1)*(1-p13_2)*p13_3 + (1-p13_1)*p13_3*(1-p13_2) + p13_1*(1-p13_2)*(1-p13_3), 4))
        })

        # 14. Теоремы вероятностей: Совместные/несовместные события
        p14_1 = round(rng.uniform(0.6, 0.8), 2)
        p14_2 = round(rng.uniform(0.5, 0.7), 2)
        pool.append({
            'text': f"Два оператора обрабатывают заявки. Вероятность успешной обработки первым равна {p14_1}, вторым — {p14_2}. Найти вероятность успешной обработки заявки ровно одним оператором. (Округление до 4 знаков).",
            'answer': str(round(p14_1*(1-p14_2) + p14_2*(1-p14_1), 4))
        })

        # 15. Формула Бернулли
        p15 = round(rng.uniform(0.7, 0.9), 2)
        pool.append({
            'text': f"Сервер успешно обрабатывает сетевой запрос с вероятностью {p15}. Какова вероятность, что из 3 независимых запросов успешными будут ровно 2? (Округление до 4 знаков).",
            'answer': str(round(3 * (p15**2) * (1 - p15), 4))
        })

        # 16. Полная вероятность: Серверные группы
        s1, s2 = rng.randint(10, 20), rng.randint(15, 25)
        p16_1 = round(rng.uniform(0.8, 0.95), 2)
        p16_2 = round(rng.uniform(0.5, 0.7), 2)
        tot16 = s1 + s2
        res16 = (s1/tot16)*p16_1 + (s2/tot16)*p16_2
        pool.append({
            'text': f"В первой группе {s1} серверов (надежность {p16_1}), во второй {s2} серверов (надежность {p16_2}). Запрос случайным образом направляется на одну из групп. Найти полную вероятность успешной обработки запроса. (Округление до 4 знаков).",
            'answer': str(round(res16, 4))
        })

        # 17. Формула Байеса
        pool.append({
            'text': f"Используя условия предыдущей задачи, запрос был успешно обработан. Найти вероятность того, что он был направлен именно на первую группу серверов (формула Байеса). (Округление до 4 знаков).",
            'answer': str(round(((s1/tot16)*p16_1) / res16, 4))
        })

        # 18. Полная вероятность: Дата-центры
        sh1, sh2, sh3 = 3, 5, 2
        t18 = sh1 + sh2 + sh3
        pool.append({
            'text': f"Три дата-центра содержат {sh1}, {sh2} и {sh3} стоек. Вероятности сбоя в них равны 0.05, 0.1 и 0.2 соответственно. Найти общую вероятность сбоя при обращении к случайно выбранной стойке. (Округление до 4 знаков).",
            'answer': str(round((sh1/t18)*0.05 + (sh2/t18)*0.1 + (sh3/t18)*0.2, 4))
        })

        # 19. Формула Байеса: Преподаватели
        pool.append({
            'text': f"Студент может сдать экзамен у трех преподавателей с равными вероятностями. Вероятности сдать у них: 0.9, 0.6 и 0.4. Студент успешно сдал экзамен. Какова вероятность, что он сдавал первому преподавателю? (Округление до 4 знаков).",
            'answer': str(round((1/3 * 0.9) / (1/3*0.9 + 1/3*0.6 + 1/3*0.4), 4))
        })

        # 20. Смешанный тип: Устройства классов
        pool.append({
            'text': f"В узле связи 70% устройств первого класса и 30% второго. Вероятность безотказной работы для них составляет 0.95 и 0.8 соответственно. Наудачу выбранное устройство вышло из строя. Какова вероятность, что оно было второго класса? (Округление до 4 знаков).",
            'answer': str(round((0.3 * 0.2) / (0.7 * 0.05 + 0.3 * 0.2), 4))
        })

        # Перемешиваем пул индивидуально для студента
        rng.shuffle(pool)

        # Собираем словарь вариантов явно через индексы (исключает NameError)
        variant = {}
        for idx, task_item in enumerate(pool):
            task_num = idx + 1
            variant[f"task_{task_num}"] = task_item

        # Контрольный теоретический вопрос
        cq_pool = [
            "Дайте определения основных комбинаторных соединений: перестановок, размещений и сочетаний. Напишите их формулы.",
            "Дайте классическое определение вероятности события. Каковы его основные свойства?",
            "В чем различие между совместными и несовместными событиями? Приведите примеры из IT.",
            "Сформулируйте теорему умножения вероятностей для зависимых и независимых событий.",
            "Запишите и объясните формулу полной вероятности и формулу Байеса."
        ]
        variant['task_99'] = {
            'title': 'Контрольный теоретический вопрос',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на вопрос:\n\n{rng.choice(cq_pool)}",
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
