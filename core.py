# -*- coding: utf-8 -*-
import random
import math
import hashlib
import json
from fractions import Fraction

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
        
        variant['task_1'] = self._task_1_servers()
        variant['task_2'] = self._task_2_cables()
        variant['task_3'] = self._task_3_racks()
        variant['task_4'] = self._task_4_vms()
        variant['task_5'] = self._task_5_tokens()
        variant['task_6'] = self._task_6_qa()
        variant['task_7'] = self._task_7_scripts()
        variant['task_8'] = self._task_8_licenses()
        variant['task_9'] = self._task_9_teams()
        variant['task_10'] = self._task_10_raid()
        
        variant['task_11'] = self._task_11_cpu()
        variant['task_12'] = self._task_12_audit()
        variant['task_13'] = self._task_13_rack_prob()
        variant['task_14'] = self._task_14_cables_prob()
        variant['task_15'] = self._task_15_geometric()
        variant['task_16'] = self._task_16_admin()
        variant['task_17'] = self._task_17_cluster()
        variant['task_18'] = self._task_18_vlan()
        variant['task_19'] = self._task_19_mac()
        variant['task_20'] = self._task_20_antivirus()
        
        # ПУЛ КОНТРОЛЬНЫХ ВОПРОСОВ (Комбинаторика и Вероятность)
        cq_pool = [
            "Что такое перестановка, размещение и сочетание? В чем их принципиальное отличие?",
            "Сформулируйте правила суммы и произведения в комбинаторике.",
            "Дайте классическое определение вероятности. В каких случаях оно применимо?",
            "Что такое несовместные и независимые события?",
            "Сформулируйте теоремы сложения вероятностей для совместных и несовместных событий.",
            "Сформулируйте теоремы умножения вероятностей для зависимых и независимых событий.",
            "Запишите формулу полной вероятности и объясните физический смысл гипотез.",
            "В каких случаях на практике применяется формула Байеса?",
            "В чем суть геометрического определения вероятности?",
            "Что называется условной вероятностью?",
            "Как вычислить вероятность появления хотя бы одного события из группы независимых событий?",
            "Что означает термин «полная группа событий» и какова сумма их вероятностей?"
        ]
        
        selected_questions = random.sample(cq_pool, 3)
        questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(selected_questions)])
        
        variant['task_99'] = {
            'title': 'Контрольные теоретические вопросы',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на следующие вопросы:\n\n{questions_text}",
            'answer': 'Ручная проверка (Требуется фото)'
        }
        
        return variant

    def _task_1_servers(self):
        type_choice = random.choice(['A', 'B'])
        N = random.randint(15, 50)
        K = random.randint(3, 7)
        if type_choice == 'A':
            text = f"Системный администратор настраивает {K} различных ролей на {N} доступных серверах. Каждая роль назначается на отдельный сервер. Сколькими способами можно распределить роли?"
            ans = math.perm(N, K)
        else:
            text = f"Из {N} доступных серверов необходимо выделить ровно {K} серверов для создания единого вычислительного кластера (роли одинаковы). Сколькими способами можно собрать кластер?"
            ans = math.comb(N, K)
        return {'text': text, 'answer': str(ans)}

    def _task_2_cables(self):
        N1, N2 = random.randint(10, 30), random.randint(10, 30)
        K1, K2 = random.randint(2, 5), random.randint(2, 5)
        text = f"На складе лежат {N1} оптических патч-кордов и {N2} медных кабелей. Инженер наугад берет {K1+K2} кабелей. Сколькими способами можно выбрать кабели так, чтобы среди них оказалось ровно {K1} оптических и {K2} медных?"
        ans = math.comb(N1, K1) * math.comb(N2, K2)
        return {'text': text, 'answer': str(ans)}

    def _task_3_racks(self):
        N, M = random.randint(10, 20), random.randint(3, 5)
        text = f"В серверной стойке устанавливают {N} различных маршрутизаторов. Сколькими способами можно расставить устройства так, чтобы {M} критически важных маршрутизаторов располагались строго в соседних юнитах (неразрывным блоком)?"
        ans = math.factorial(N - M + 1) * math.factorial(M)
        return {'text': text, 'answer': str(ans)}

    def _task_4_vms(self):
        K1, K2, K3 = random.randint(5, 15), random.randint(5, 15), random.randint(5, 15)
        text = f"Сколькими способами можно распределить {K1+K2+K3} уникальных виртуальных машин по 3 физическим хостам так, чтобы на первый попало ровно {K1} машин, на второй — {K2}, на третий — {K3}?"
        ans = math.comb(K1+K2+K3, K1) * math.comb((K1+K2+K3) - K1, K2) * math.comb(K3, K3)
        return {'text': text, 'answer': str(ans)}

    def _task_5_tokens(self):
        N, K = random.randint(10, 16), random.randint(4, 8)
        text = f"Разработчик задает пароль длиной {K} символов, используя алфавит из {N} уникальных символов. Символы в пароле НЕ могут повторяться. Сколько вариантов пароля существует?"
        ans = math.perm(N, K)
        return {'text': text, 'answer': str(ans)}

    def _task_6_qa(self):
        N, K = random.randint(15, 35), random.randint(4, 7)
        text = f"Для QA-тестирования отбираются {K} устройств из парка лаборатории, в котором {N} абсолютно уникальных смартфонов. Сколькими способами можно сформировать стенд?"
        ans = math.comb(N, K)
        return {'text': text, 'answer': str(ans)}

    def _task_7_scripts(self):
        N = random.randint(8, 15)
        text = f"Администратор настраивает автозагрузку {N} системных скриптов. Сколькими способами можно настроить очередь, если 2 ресурсоемких скрипта строго НЕ должны запускаться подряд?"
        ans = math.factorial(N) - (math.factorial(N - 1) * 2)
        return {'text': text, 'answer': str(ans)}

    def _task_8_licenses(self):
        N, M = random.randint(12, 25), random.randint(4, 8)
        text = f"Имеется {N} уникальных ключей для IDE. Сколькими способами их можно распределить между {M} разработчиками, если каждый разработчик может получить любое количество ключей?"
        ans = M ** N
        return {'text': text, 'answer': str(ans)}

    def _task_9_teams(self):
        N1, N2, K1 = random.randint(10, 20), random.randint(8, 15), random.randint(3, 5)
        text = f"В отделе {N1} С++ разработчиков и {N2} сисадминов. Формируется команда: один тимлид, один архитектор (выбираются из всего отдела) и {K1} рядовых исполнителей из оставшихся. Сколькими способами это можно сделать?"
        ans = math.perm(N1+N2, 2) * math.comb((N1+N2) - 2, K1)
        return {'text': text, 'answer': str(ans)}

    def _task_10_raid(self):
        N, K, M = random.randint(15, 30), random.randint(6, 12), random.randint(2, 4)
        text = f"Для сборки RAID из партии в {N} жестких дисков выбирают {K} штук. Сколькими способами можно выбрать диски, если {M} конкретных дисков перегреваются и их брать НЕЛЬЗЯ?"
        ans = math.comb(N - M, K)
        return {'text': text, 'answer': str(ans)}

    def _task_11_cpu(self):
        N, K = random.randint(6, 12), random.randint(3, 5)
        text = f"Планировщик задач распределяет {K} независимых потоков по {N} ядрам процессора. Каждый поток равновероятно попадает на любое ядро. Какова вероятность того, что все потоки попадут на одно и то же ядро? (Ответ в виде дроби)"
        ans = Fraction(N, N ** K)
        return {'text': text, 'answer': str(ans)}

    def _task_12_audit(self):
        N1, N2 = random.randint(15, 30), random.randint(10, 20)
        K, K1 = random.randint(4, 7), 0
        K1 = random.randint(2, K-1)
        text = f"В партии {N1} трансиверов завода «А» и {N2} трансиверов завода «Б». Инженер наугад берет {K} штук. Какова вероятность, что среди них ровно {K1} завода «А» и {K-K1} завода «Б»?"
        ans = Fraction(math.comb(N1, K1) * math.comb(N2, K-K1), math.comb(N1+N2, K))
        return {'text': text, 'answer': str(ans)}

    def _task_13_rack_prob(self):
        N = random.randint(8, 16)
        text = f"В серверный шкаф наудачу друг над другом устанавливают {N} серверов. Какова вероятность того, что два конкретных сервера (основной и резервный) окажутся в соседних юнитах?"
        ans = Fraction(math.factorial(N - 1) * 2, math.factorial(N))
        return {'text': text, 'answer': str(ans)}

    def _task_14_cables_prob(self):
        N1, N2 = random.randint(10, 25), random.randint(10, 25)
        text = f"В коробке {N1} медных и {N2} оптических патч-кордов. Техник достает первый кабель, подключает его (НЕ возвращает), затем достает второй. Найти вероятность того, что оба кабеля оптические."
        ans = Fraction(N2, N1+N2) * Fraction(N2 - 1, N1+N2 - 1)
        return {'text': text, 'answer': str(ans)}

    def _task_15_geometric(self):
        T, t = random.randint(50, 100), random.randint(5, 15)
        text = f"Два пакета данных прибывают на порт в течение случайного времени внутри окна в {T} мс. Если разница между их прибытием менее {t} мс, происходит коллизия. Найти вероятность коллизии."
        ans = Fraction((T ** 2) - ((T - t) ** 2), T ** 2)
        return {'text': text, 'answer': str(ans)}

    def _task_16_admin(self):
        N = random.randint(40, 60)
        M = random.randint(30, N-5)
        K = random.randint(3, 5)
        text = f"Из {N} параметров роутера студент знает {M}. Преподаватель случайно спрашивает {K} параметров. Найти вероятность того, что студент знает все спрошенные параметры."
        ans = Fraction(math.comb(M, K), math.comb(N, K))
        return {'text': text, 'answer': str(ans)}

    def _task_17_cluster(self):
        N, M = random.randint(10, 30), random.randint(2, 6)
        text = f"В кластере {N} серверов, из них {M} зависли. Балансировщик дважды отправляет независимый запрос на случайный сервер (с возвращением). Найти вероятность того, что ОБА запроса попадут на зависший сервер."
        ans = Fraction(M, N) * Fraction(M, N)
        return {'text': text, 'answer': str(ans)}

    def _task_18_vlan(self):
        N = random.choice([20, 30, 40])
        M = random.randint(4, 8)
        text = f"В сети {N} устройств, среди которых {M} зараженных. Сеть случайным образом делят на 2 равные VLAN (по {N//2} устройств). Какова вероятность того, что все {M} зараженных попадут в первый VLAN?"
        ans = Fraction(math.comb(N - M, (N//2) - M), math.comb(N, N//2))
        return {'text': text, 'answer': str(ans)}

    def _task_19_mac(self):
        word = random.choice(["СЕРВЕР", "АДМИН", "МАССИВ", "СЕССИЯ"])
        counts = {char: word.count(char) for char in set(word)}
        denominator = math.factorial(len(word))
        for count in counts.values():
            denominator //= math.factorial(count)
        text = f"Система случайным образом перемешивает буквы слова «{word}». Какова вероятность того, что буквы выстроятся в строго исходном порядке?"
        ans = Fraction(1, denominator)
        return {'text': text, 'answer': str(ans)}

    def _task_20_antivirus(self):
        p1, p2, p3 = round(random.uniform(0.7, 0.95), 2), round(random.uniform(0.7, 0.95), 2), round(random.uniform(0.7, 0.95), 2)
        text = f"Три независимых антивирусных сканера проверяют файл. Вероятности отловить угрозу равны: P1 = {p1}, P2 = {p2}, P3 = {p3}. Какова вероятность того, что угрозу отловит ХОТЯ БЫ ОДИН сканер? (Десятичная дробь)"
        ans = round(1 - ((1 - p1) * (1 - p2) * (1 - p3)), 4)
        return {'text': text, 'answer': str(ans)}

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

        for task_key, task_data in variant.items():
            has_photo = bool(student_answers.get(f"{task_key}_photo"))
            student_ans_str = student_answers.get(task_key, "").strip()
            
            if task_key == 'task_99':
                if has_photo:
                    is_correct = True
                    correct_count += 1
                    details[task_key] = {
                        'is_correct': True, 'correct_answer': "Фото прикреплено (Ожидает оценки)",
                        'student_answer': f"Текст: {student_ans_str} + Фото" if student_ans_str else "Только фото"
                    }
                else:
                    details[task_key] = {
                        'is_correct': False, 'correct_answer': "Необходимо прикрепить фото с ответами!",
                        'student_answer': "Нет фото!"
                    }
                continue

            correct_ans_str = str(task_data.get('answer', ''))
            is_correct = (student_ans_str == correct_ans_str)

            if not has_photo:
                is_correct = False
                if student_ans_str:
                    student_ans_str = f"{student_ans_str} (Нет фото!)"
                else:
                    student_ans_str = "Нет ответа (Нет фото!)"

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
