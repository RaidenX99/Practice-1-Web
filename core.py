# -*- coding: utf-8 -*-
import hashlib
import random
import math
import json

class PracticeEngine9:
    def __init__(self, student_id):
        self.student_id = str(student_id)
        self.seed = self._generate_seed()
        random.seed(self.seed)

    def _generate_seed(self):
        hash_obj = hashlib.md5(self.student_id.encode())
        return int(hash_obj.hexdigest(), 16)

    def _generate_dataset(self):
        # Банк различных сценариев для заданий
        scenarios = [
            {
                "theme": "сетевой задержки (ping) до игрового сервера",
                "entity": "задержек",
                "unit": "мс",
                "base_min": 30, "base_max": 45,
                "step_min": 5, "step_max": 10
            },
            {
                "theme": "затухания сигнала в оптическом волокне на разных участках трассы",
                "entity": "затуханий",
                "unit": "дБ",
                "base_min": 10, "base_max": 20,
                "step_min": 2, "step_max": 4
            },
            {
                "theme": "скорости скачивания (Download) при тестировании Wi-Fi роутера",
                "entity": "скоростей",
                "unit": "Мбит/с",
                "base_min": 50, "base_max": 75,
                "step_min": 10, "step_max": 15
            },
            {
                "theme": "времени первого байта (TTFB) при обращении к веб-серверу",
                "entity": "времени отклика",
                "unit": "мс",
                "base_min": 100, "base_max": 150,
                "step_min": 20, "step_max": 30
            },
            {
                "theme": "температуры процессора маршрутизатора при пиковой нагрузке",
                "entity": "температур",
                "unit": "°C",
                "base_min": 55, "base_max": 65,
                "step_min": 3, "step_max": 5
            }
        ]

        # Выбираем случайный сценарий на основе зачетки студента
        scenario = random.choice(scenarios)

        # Генерация правдоподобных целых данных
        base_val = random.randint(scenario["base_min"], scenario["base_max"])
        step = random.randint(scenario["step_min"], scenario["step_max"])
        bounds = [base_val + i*step for i in range(6)]
        
        # Распределение частот по 5 интервалам (Колоколообразное, чтобы гистограмма была красивой)
        m = [random.randint(1, 2), random.randint(4, 6), random.randint(6, 8), random.randint(3, 5), random.randint(1, 2)]
        n = sum(m)
        w = [round(count / n, 2) for count in m]
        
        # Генерация сырой выборки целых чисел
        raw_data = []
        for i in range(5):
            for _ in range(m[i]):
                # Генерируем числа строго внутри интервала
                val = random.randint(bounds[i], bounds[i+1] - 1)
                raw_data.append(val)
                
        random.shuffle(raw_data)
        
        # Расчет точных статистик по сырой выборке
        mean = sum(raw_data) / n
        sorted_data = sorted(raw_data)
        if n % 2 == 0:
            median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            median = sorted_data[n//2]
            
        data_range = max(raw_data) - min(raw_data)
        
        # Исправленная выборочная дисперсия (на n-1)
        variance = sum((x - mean)**2 for x in raw_data) / (n - 1)
        std_dev = math.sqrt(variance)

        return {
            'raw_data': raw_data, 'bounds': bounds, 'frequencies': m, 'relative_frequencies': w, 'n': n,
            'mean': mean, 'median': median, 'range': data_range, 'variance': variance, 'std_dev': std_dev,
            'theme': scenario['theme'], 'entity': scenario['entity'], 'unit': scenario['unit']
        }

    def generate_variant(self):
        dataset = self._generate_dataset()
        raw_str = ", ".join(map(str, dataset['raw_data']))
        unit = dataset['unit']
        
        intro_text = (f"В ходе диагностики телекоммуникационного оборудования была собрана статистика "
                      f"{dataset['theme']}. Получена следующая сырая выборка {dataset['entity']} "
                      f"в {unit} из n={dataset['n']} наблюдений:\n\n"
                      f"[ {raw_str} ]\n\n"
                      f"Используя эти данные, выполните первичный статистический анализ (ответы округляйте до сотых).")

        variant = {}
        
        variant['task_1'] = {
            'type': 'calc', 'title': 'Задача 1. Размах выборки',
            'text': intro_text + f"\n\nОпределите размах выборки R (разность между максимальным и минимальным значениями) в {unit}.",
            'questions': {'A': {'label': f'Размах выборки R ({unit}):', 'ans': dataset['range'], 'placeholder': '(Пример: 25)'}}
        }
        
        variant['task_2'] = {
            'type': 'calc', 'title': 'Задача 2. Выборочное среднее',
            'text': "Для этой же выборки вычислите выборочное среднее арифметическое x̄.",
            'questions': {'A': {'label': f'Среднее значение x̄ ({unit}):', 'ans': round(dataset['mean'], 2), 'placeholder': '(Пример: 45.33)'}}
        }
        
        variant['task_3'] = {
            'type': 'calc', 'title': 'Задача 3. Медиана',
            'text': "Упорядочьте выборку по возрастанию (составьте вариационный ряд) и найдите медиану Me.",
            'questions': {'A': {'label': f'Медиана Me ({unit}):', 'ans': round(dataset['median'], 2), 'placeholder': '(Пример: 44.5)'}}
        }
        
        variant['task_4'] = {
            'type': 'calc', 'title': 'Задача 4. Исправленная дисперсия',
            'text': "Для оценки нестабильности показателя вычислите исправленную выборочную дисперсию s² (в знаменателе используется n-1).",
            'questions': {'A': {'label': 'Исправленная дисперсия s²:', 'ans': round(dataset['variance'], 3), 'placeholder': '(Пример: 85.125)'}}
        }
        
        variant['task_5'] = {
            'type': 'calc', 'title': 'Задача 5. Среднее квадратическое отклонение',
            'text': "Вычислите исправленное выборочное среднее квадратическое отклонение s (разброс показателя).",
            'questions': {'A': {'label': f'СКО s ({unit}):', 'ans': round(dataset['std_dev'], 3), 'placeholder': '(Пример: 9.226)'}}
        }

        intervals_str = " ; ".join([f"[{dataset['bounds'][i]}; {dataset['bounds'][i+1]})" for i in range(5)])
        variant['task_6'] = {
            'type': 'histogram', 'title': 'Задача 6. Построение гистограммы',
            'text': (f"Разбейте исходную выборку на 5 интервалов: {intervals_str}.\n"
                     f"Рассчитайте относительные частоты W = m/n для каждого интервала. "
                     f"Захватите верхний край столбцов на графике ниже мышкой и вытяните их до уровня рассчитанных относительных частот."),
            'bounds': dataset['bounds'],
            'correct_y': dataset['relative_frequencies'],
            'max_y': max(dataset['relative_frequencies']) + 0.1
        }

        # БЛОК КОНТРОЛЬНЫХ ВОПРОСОВ
        cq_pool = [
            "Что такое генеральная совокупность и что такое выборка? В чем их отличие?",
            "В чем разница между точечной и интервальной оценкой параметра?",
            "Дайте определение выборочного среднего и медианы. В каких случаях медиана показательнее среднего?",
            "Зачем при расчете исправленной выборочной дисперсии в знаменателе используют (n-1), а не n?",
            "Что такое мода выборки и как ее определить для дискретного и интервального рядов?",
            "Как строится интервальный статистический ряд? По какому правилу обычно выбирают число интервалов?",
            "Что такое гистограмма и полигон частот? В чем их визуальное и математическое отличие?",
            "В чем отличие относительной частоты от абсолютной?",
            "Какими свойствами обладает эмпирическая функция распределения?",
            "Как вычисляется выборочное среднее квадратическое отклонение (СКО) и каков его физический смысл?",
            "Что такое размах вариации и что он характеризует?",
            "В чем заключается суть первичной описательной статистики?"
        ]
        
        selected_questions = random.sample(cq_pool, 3)
        questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(selected_questions)])
        
        variant['task_99'] = {
            'type': 'control_questions',
            'title': 'Контрольные теоретические вопросы',
            'text': f"Ответьте на следующие вопросы. ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом:\n\n{questions_text}",
            'correct_answer': 'Ручная проверка (Требуется фото)'
        }

        return variant

    @staticmethod
    def generate_security_hash(student_id, answers_dict):
        data_string = f"{student_id}_" + "_".join([f"{k}:{v}" for k, v in sorted(answers_dict.items())])
        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    def check_answers(self, student_answers):
        variant = self.generate_variant()
        details = {}
        correct_count = 0
        total_count = 0

        for task_key, task_data in variant.items():
            has_photo = bool(student_answers.get(f"{task_key}_photo"))
            
            if task_data['type'] == 'control_questions':
                total_count += 1
                if has_photo:
                    is_correct = True
                    correct_count += 1
                    details[task_key] = {
                        'title': task_data['title'], 'is_correct': True,
                        'student_answer': "Фото прикреплено", 'correct_answer': "Ожидает оценки"
                    }
                else:
                    details[task_key] = {
                        'title': task_data['title'], 'is_correct': False,
                        'student_answer': "Нет фото!", 'correct_answer': "Необходимо прикрепить фото!"
                    }
                continue

            if task_data['type'] == 'histogram':
                total_count += 1
                ans_str = student_answers.get(task_key, '{}')
                try:
                    ans_dict = json.loads(ans_str)
                    is_correct = True
                    # Проверяем высоту каждого из 5 столбцов
                    for i in range(5):
                        sy = float(ans_dict.get(str(i), 0))
                        cy = task_data['correct_y'][i]
                        if abs(sy - cy) > 0.02: # Погрешность для ручного перетаскивания
                            is_correct = False
                            break
                            
                    if not has_photo:
                        is_correct = False
                        student_ans_disp = "Отрисован (Нет фото!)"
                    else:
                        student_ans_disp = "Отрисован" if ans_dict else "Пусто"

                    details[task_key] = {
                        'title': task_data['title'], 'is_correct': is_correct,
                        'student_answer': student_ans_disp, 'correct_answer': "Точный график"
                    }
                    if is_correct: correct_count += 1
                except:
                    details[task_key] = {'title': task_data['title'], 'is_correct': False, 'student_answer': "Ошибка", 'correct_answer': "График"}

            elif task_data['type'] == 'calc':
                for q_key, q_data in task_data.get('questions', {}).items():
                    total_count += 1
                    full_key = f"{task_key}_{q_key}"
                    correct_ans_str = str(q_data['ans'])
                    student_ans_str = student_answers.get(full_key, "").strip().replace(',', '.')
                    
                    is_correct = False
                    try:
                        if student_ans_str and abs(float(correct_ans_str) - float(student_ans_str)) <= 0.05:
                            is_correct = True
                    except ValueError:
                        is_correct = False
                        
                    if not has_photo:
                        is_correct = False
                        student_ans_str = f"{student_ans_str} (Нет фото!)" if student_ans_str else "Нет ответа (Нет фото!)"
                            
                    if is_correct: correct_count += 1
                        
                    details[full_key] = {
                        'title': task_data['title'],
                        'is_correct': is_correct,
                        'correct_answer': correct_ans_str,
                        'student_answer': student_ans_str
                    }
            
        percent = int((correct_count / total_count) * 100) if total_count > 0 else 0
        if percent == 100: mark = 5
        elif percent >= 75: mark = 4
        elif percent >= 50: mark = 3
        else: mark = 2

        photos_dict = {k: student_answers.get(f"{k}_photo") for k in variant.keys() if student_answers.get(f"{k}_photo")}
            
        return {
            'mark': mark, 'percent': percent, 'correct_count': correct_count,
            'total_count': total_count, 'details': details, 'photos': photos_dict
        }