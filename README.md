## Постановка задачи

Вы должны разработать прототип системы, которая анализирует статистические данные о доходах фрилансеров и предоставляет ответы на запросы, сформулированные на естественном языке. Для этого используйте набор данных, доступный по ссылке:[ Freelancer Earnings and Job Trends](https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends?select=freelancer_earnings_bd.csv).

## Структура проекта

app
├── core
│   └── main.py
│   ├── Subfolder 2
│   │   └── Subfolder 2.1
│   │   └── Subfolder 2.2
├── database
│   ├── Subfolder 1
│   │   └── Subfolder 1.1
│   │   └── Subfolder 1.2
│   │   └── Subfolder 1.3
└── model

---

## Исследуем API нейросетей на возможность писать корректные SQL запросы

```python
import numpy as np
import pandas as pd
import psycopg2
```

```python
DEEPSEEK_KEY = "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"
```

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=DEEPSEEK_KEY,
)

completion = client.chat.completions.create(
  model="deepseek/deepseek-r1:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ],
  temperature=0
)
response_message = completion.choices[0].message.content
print(response_message )
```

The meaning of life is a deeply personal and multifaceted concept that varies across individuals, cultures, and philosophical traditions. Here's a structured synthesis of the exploration:

1. **Philosophical Perspectives**:

   - **Existentialism**: Life has no inherent meaning; individuals must create their own purpose through choices and actions (e.g., Sartre, Camus).
   - **Absurdism**: Embraces the conflict between seeking meaning and an indifferent universe, finding joy in the struggle itself (Camus).
2. **Religious/Spiritual Views**:

   - **Theistic Religions**: Purpose often involves serving a divine being, achieving salvation, or enlightenment (e.g., Christianity, Buddhism).
   - **Eastern Philosophies**: Focus on ending suffering (Buddhism) or harmonizing with the universe (Taoism).
3. **Scientific Angle**:

   - **Biology**: Survival, reproduction, and genetic continuity, though humans seek fulfillment beyond these basics.
   - **Cosmology**: Some explore meaning through the universe's origins, though science typically addresses "how" rather than "why."
4. **Psychological Insights**:

   - **Maslow's Hierarchy**: Progressing from basic needs to self-actualization and transcendence.
   - **Positive Psychology**: Emphasizes well-being, relationships, and personal growth as sources of meaning.
5. **Cultural Influences**:

   - **Collectivist vs. Individualist**: Community vs. personal achievement; cultural values shape perceived purposes.
6. **Subjective vs. Objective Meaning**:

   - **Subjective**: Personal fulfillment, relationships, creativity, or legacy.
   - **Objective**: Hypothetical universal purpose (e.g., moral frameworks, divine plans), though debated.
7. **Synthesis**:

   - The search for meaning itself—through love, art, knowledge, or service—often becomes the journey that defines purpose. It may blend personal aspirations, connections, and contributions to a greater good.

**Conclusion**: There is no singular answer. The meaning of life emerges from an individual's exploration of existence, shaped by their beliefs, experiences, and cultural context. It is a dynamic, evolving pursuit rather than a fixed destination.

---

Имея доступ к нейросети deepseek, распарсим таблицу данных на группы.

```python
df = pd.DataFrame()
with psycopg2.connect(
    "dbname=db user=user password=passw host=127.0.0.1 port=5440"
) as conn:
    df = pd.read_sql_query("Select * FROM freelancers", conn)
df
```

<div>

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>freelancer_id</th>
      <th>job_category</th>
      <th>platform</th>
      <th>experience_level</th>
      <th>client_region</th>
      <th>payment_method</th>
      <th>job_completed</th>
      <th>earnings_usd</th>
      <th>hourly_rate</th>
      <th>job_success_rate</th>
      <th>client_rating</th>
      <th>job_duration_days</th>
      <th>project_type</th>
      <th>rehire_rate</th>
      <th>marketing_spend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.0</td>
      <td>Web Development</td>
      <td>Fiverr</td>
      <td>Beginner</td>
      <td>Asia</td>
      <td>Mobile Banking</td>
      <td>180.0</td>
      <td>1620.0</td>
      <td>95.79</td>
      <td>68.73</td>
      <td>3.18</td>
      <td>1.0</td>
      <td>Fixed</td>
      <td>40.19</td>
      <td>53.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2.0</td>
      <td>App Development</td>
      <td>Fiverr</td>
      <td>Beginner</td>
      <td>Australia</td>
      <td>Mobile Banking</td>
      <td>218.0</td>
      <td>9078.0</td>
      <td>86.38</td>
      <td>97.54</td>
      <td>3.44</td>
      <td>54.0</td>
      <td>Fixed</td>
      <td>36.53</td>
      <td>486.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3.0</td>
      <td>Web Development</td>
      <td>Fiverr</td>
      <td>Beginner</td>
      <td>UK</td>
      <td>Crypto</td>
      <td>27.0</td>
      <td>3455.0</td>
      <td>85.17</td>
      <td>86.60</td>
      <td>4.20</td>
      <td>46.0</td>
      <td>Hourly</td>
      <td>74.05</td>
      <td>489.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.0</td>
      <td>Data Entry</td>
      <td>PeoplePerHour</td>
      <td>Intermediate</td>
      <td>Asia</td>
      <td>Bank Transfer</td>
      <td>17.0</td>
      <td>5577.0</td>
      <td>14.37</td>
      <td>79.93</td>
      <td>4.47</td>
      <td>41.0</td>
      <td>Hourly</td>
      <td>27.58</td>
      <td>67.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>Digital Marketing</td>
      <td>Upwork</td>
      <td>Expert</td>
      <td>Asia</td>
      <td>Crypto</td>
      <td>245.0</td>
      <td>5898.0</td>
      <td>99.37</td>
      <td>57.80</td>
      <td>5.00</td>
      <td>41.0</td>
      <td>Hourly</td>
      <td>69.09</td>
      <td>489.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1945</th>
      <td>1946.0</td>
      <td>Graphic Design</td>
      <td>Fiverr</td>
      <td>Beginner</td>
      <td>USA</td>
      <td>Mobile Banking</td>
      <td>143.0</td>
      <td>6823.0</td>
      <td>22.54</td>
      <td>75.86</td>
      <td>4.65</td>
      <td>13.0</td>
      <td>Hourly</td>
      <td>26.55</td>
      <td>133.0</td>
    </tr>
    <tr>
      <th>1946</th>
      <td>1947.0</td>
      <td>SEO</td>
      <td>Upwork</td>
      <td>Intermediate</td>
      <td>Middle East</td>
      <td>Crypto</td>
      <td>164.0</td>
      <td>7942.0</td>
      <td>77.20</td>
      <td>72.01</td>
      <td>3.29</td>
      <td>34.0</td>
      <td>Hourly</td>
      <td>24.81</td>
      <td>343.0</td>
    </tr>
    <tr>
      <th>1947</th>
      <td>1948.0</td>
      <td>SEO</td>
      <td>PeoplePerHour</td>
      <td>Expert</td>
      <td>UK</td>
      <td>Bank Transfer</td>
      <td>236.0</td>
      <td>9838.0</td>
      <td>24.64</td>
      <td>57.37</td>
      <td>4.67</td>
      <td>38.0</td>
      <td>Fixed</td>
      <td>61.52</td>
      <td>370.0</td>
    </tr>
    <tr>
      <th>1948</th>
      <td>1949.0</td>
      <td>SEO</td>
      <td>Freelancer</td>
      <td>Intermediate</td>
      <td>Europe</td>
      <td>Bank Transfer</td>
      <td>152.0</td>
      <td>4492.0</td>
      <td>71.07</td>
      <td>66.41</td>
      <td>4.08</td>
      <td>70.0</td>
      <td>Fixed</td>
      <td>32.40</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>1949</th>
      <td>1950.0</td>
      <td>Graphic Design</td>
      <td>Freelancer</td>
      <td>Expert</td>
      <td>Middle East</td>
      <td>PayPal</td>
      <td>247.0</td>
      <td>9297.0</td>
      <td>22.22</td>
      <td>71.70</td>
      <td>4.69</td>
      <td>68.0</td>
      <td>Fixed</td>
      <td>45.42</td>
      <td>236.0</td>
    </tr>
  </tbody>
</table>
<p>1950 rows × 15 columns</p>
</div>

Вытащим колонки и типы данных

```python
columns = df.columns
numeric_types = df.select_dtypes(include=np.number).columns
non_numeric_types = df.select_dtypes(exclude=np.number).columns

(columns, numeric_types, non_numeric_types)
```

(Index(['freelancer_id', 'job_category', 'platform', 'experience_level',
'client_region', 'payment_method', 'job_completed', 'earnings_usd',
'hourly_rate', 'job_success_rate', 'client_rating', 'job_duration_days',
'project_type', 'rehire_rate', 'marketing_spend'],
dtype='object'),
Index(['freelancer_id', 'job_completed', 'earnings_usd', 'hourly_rate',
'job_success_rate', 'client_rating', 'job_duration_days', 'rehire_rate',
'marketing_spend'],
dtype='object'),
Index(['job_category', 'platform', 'experience_level', 'client_region',
'payment_method', 'project_type'],
dtype='object'))

---

Из анализа датафрейма выше видно, что в текстовых колонках число уникальных данных мало (5 - 8).
Можно вытянуть их отдельно для каждой колонки.

```python
unique = {}
```

```python
df_non_numeric_uniq = df.loc[:, non_numeric_types]
for column in df_non_numeric_uniq:
    unique[column] = list(df_non_numeric_uniq[column].unique())
unique
```

{'job_category': ['Web Development',
'App Development',
'Data Entry',
'Digital Marketing',
'Customer Support',
'Content Writing',
'Graphic Design',
'SEO'],
'platform': ['Fiverr', 'PeoplePerHour', 'Upwork', 'Toptal', 'Freelancer'],
'experience_level': ['Beginner', 'Intermediate', 'Expert'],
'client_region': ['Asia',
'Australia',
'UK',
'Europe',
'USA',
'Middle East',
'Canada'],
'payment_method': ['Mobile Banking', 'Crypto', 'Bank Transfer', 'PayPal'],
'project_type': ['Fixed', 'Hourly']}

---

После получения вариаций значений для колонок, получим минмумы и максимумы по колонкам числовым
Это даст нейросети больше понимания, в каких диапазонах и с какими данными она работает

```python
diapazones = {}
```

```python
df_numeric_diapazones = df.loc[:, numeric_types]
for column in df_numeric_diapazones:
    diapazones[column] = {'min': int(np.min(df_numeric_diapazones[column])),
                          			 'max': int(np.max(df_numeric_diapazones[column]))}
diapazones
```

{'freelancer_id': {'min': 1, 'max': 1950},
'job_completed': {'min': 5, 'max': 299},
'earnings_usd': {'min': 51, 'max': 9991},
'hourly_rate': {'min': 5, 'max': 99},
'job_success_rate': {'min': 50, 'max': 99},
'client_rating': {'min': 3, 'max': 5},
'job_duration_days': {'min': 1, 'max': 89},
'rehire_rate': {'min': 10, 'max': 79},
'marketing_spend': {'min': 0, 'max': 499}}

---

Думаю, что к этим данным не помешает описание. Цейросети, как и человеку, нужен контекст, с которым она будет работать.

### Dataset Features


| Column Name       | Description                                        | Data Type | Example Values                                        |
| ----------------- | -------------------------------------------------- | --------- | ----------------------------------------------------- |
| Freelancer_ID     | Unique identifier for each freelancer record       | integer   | 1, 2, 3                                               |
| Job_Category      | Primary classification of freelance work performed | string    | Web Development, Data Entry, Content Writing          |
| Platform          | Freelance marketplace where work was performed     | string    | Fiverr, Upwork, Toptal, Freelancer, PeoplePerHour     |
| Experience_Level  | Freelancer's professional experience tier          | string    | Beginner, Intermediate, Expert                        |
| Client_Region     | Geographical location of the client                | string    | Asia, Europe, USA, Canada, UK, Australia, Middle East |
| Payment_Method    | Method used for financial transactions             | string    | Bank Transfer, PayPal, Mobile Banking, Crypto         |
| Job_Completed     | Number of projects successfully completed          | integer   | 180, 218, 27                                          |
| Earnings_USD      | Total earnings in US Dollars                       | float     | 1620, 9078, 3455                                      |
| Hourly_Rate       | Freelancer's hourly compensation rate in USD       | float     | 95.79, 86.38, 85.17                                   |
| Job_Success_Rate  | Percentage of successful job completions           | float     | 68.73, 97.54, 86.6                                    |
| Client_Rating     | Average rating given by clients (1.0-5.0 scale)    | float     | 3.18, 3.44, 4.2                                       |
| Job_Duration_Days | Average project timeline in days                   | integer   | 1, 54, 46                                             |
| Project_Type      | Classification of work arrangement                 | string    | Fixed, Hourly                                         |
| Rehire_Rate       | Percentage of clients who rehire the freelancer    | float     | 40.19, 36.53, 74.05                                   |
| Marketing_Spend   | Amount invested in platform promotion in USD       | integer   | 53, 486, 489                                          |

Хорошо, что хорошие авторы kaggle дают хорошее описание своих фич) а ещё чистые данные :)

Не вижу смысла в векторном представлении этих данных по описанию и храниню их в векторной базе по типу Chroma в эмбеддингах. Запишем эти описания в поля description и подадим на вход вместе с остальным контекстом

```python
feach_descriptions = {
	"Freelancer_ID":"Unique identifier for each freelancer record ",
    "Job_Category":"Primary classification of freelance work performed",
    "Platform":"Freelance marketplace where work was performed",
    "Experience_Level": "Freelancer's professional experience tier",
    "Client_Region": " Geographical location of the client ",
    "Payment_Method": "Method used for financial transactions",
    "Job_Completed": "Number of projects successfully completed",
    "Earnings_USD": "Total earnings in US Dollars",
    "Hourly_Rate ": "Freelancer's hourly compensation rate in USD",
    "Job_Success_Rate": "Percentage of successful job completions",
    "Client_Rating": "Average rating given by clients (1.0-5.0 scale)",
    "Job_Duration_Days": "Average project timeline in days",
    "Project_Type": "Classification of work arrangement",
    "Rehire_Rate": "Percentage of clients who rehire the freelancer",
    "Marketing_Spend": "Amount invested in platform promotion in USD"
}
```

Теперь добавим имя таблицы

```python
table_name = {
    'table_name': 'freelancers',
}
```

СОберём из этого системный контекстный json файл

```python
context = [
    table_name,
    feach_descriptions,
    unique,
    diapazones
]
```

```python
import json
with open("context.json", 'w') as f:
	json.dump(context, f)
```

## Попробуем сделать запрос из тестовых вопросов с контекстом

Напишем системный промпт

```python
system_prompt = {
    "role":"system",
    "content": f"""Ты - Аналитик данных и отлично знаешь PostgreSQL. Твоя задача - создать для пользователя оптмиальный SQL зпрос для СУБД PostgreSQL.
    Таблица, с которой ты работаешь, содержит следующе данные:
    {context}
	Не придумывай данные, используй только приведённую структуру. Существующие имена таблиц и переменных.
    На выход дай ТОЛЬКО SQL - запрос к таблице. Запрос выводи текстом без кавычек и без форматирования.
	"""
}
system_prompt
```

{'role': 'system',
'content': 'Ты - Аналитик данных и отлично знаешь PostgreSQL. Твоя задача - создать для пользователя оптмиальный SQL зпрос для СУБД PostgreSQL.\n    Таблица, с которой ты работаешь, содержит следующе данные:\n    [{\'table_name\': \'freelancers\'}, {\'Freelancer_ID\': \'Unique identifier for each freelancer record \', \'Job_Category\': \'Primary classification of freelance work performed\', \'Platform\': \'Freelance marketplace where work was performed\', \'Experience_Level\': "Freelancer\'s professional experience tier", \'Client_Region\': \' Geographical location of the client \', \'Payment_Method\': \'Method used for financial transactions\', \'Job_Completed\': \'Number of projects successfully completed\', \'Earnings_USD\': \'Total earnings in US Dollars\', \'Hourly_Rate \': "Freelancer\'s hourly compensation rate in USD", \'Job_Success_Rate\': \'Percentage of successful job completions\', \'Client_Rating\': \'Average rating given by clients (1.0-5.0 scale)\', \'Job_Duration_Days\': \'Average project timeline in days\', \'Project_Type\': \'Classification of work arrangement\', \'Rehire_Rate\': \'Percentage of clients who rehire the freelancer\', \'Marketing_Spend\': \'Amount invested in platform promotion in USD\'}, {\'job_category\': [\'Web Development\', \'App Development\', \'Data Entry\', \'Digital Marketing\', \'Customer Support\', \'Content Writing\', \'Graphic Design\', \'SEO\'], \'platform\': [\'Fiverr\', \'PeoplePerHour\', \'Upwork\', \'Toptal\', \'Freelancer\'], \'experience_level\': [\'Beginner\', \'Intermediate\', \'Expert\'], \'client_region\': [\'Asia\', \'Australia\', \'UK\', \'Europe\', \'USA\', \'Middle East\', \'Canada\'], \'payment_method\': [\'Mobile Banking\', \'Crypto\', \'Bank Transfer\', \'PayPal\'], \'project_type\': [\'Fixed\', \'Hourly\']}, {\'freelancer_id\': {\'min\': 1, \'max\': 1950}, \'job_completed\': {\'min\': 5, \'max\': 299}, \'earnings_usd\': {\'min\': 51, \'max\': 9991}, \'hourly_rate\': {\'min\': 5, \'max\': 99}, \'job_success_rate\': {\'min\': 50, \'max\': 99}, \'client_rating\': {\'min\': 3, \'max\': 5}, \'job_duration_days\': {\'min\': 1, \'max\': 89}, \'rehire_rate\': {\'min\': 10, \'max\': 79}, \'marketing_spend\': {\'min\': 0, \'max\': 499}}]\n\tНе придумывай данные, используй только приведённую структуру. Существующие имена таблиц и переменных.\n    На выход дай ТОЛЬКО SQL - запрос к таблице. Запрос выводи текстом без кавычек и без форматирования.\n\t'}

---

**Минимальный пул вопросов, на которые предстоит ответить**

- Насколько выше доход у фрилансеров, принимающих оплату в криптовалюте, по сравнению с другими способами оплаты?
- Как распределяется доход фрилансеров в зависимости от региона проживания?
- Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?

```python
# модель deepseek оказалась слишком медленной. В качестве альтернативы выбрана qwen/qwen3-30b-a3b:free
completion = client.chat.completions.create(
  model="qwen/qwen3-30b-a3b:free",
  messages=[
    system_prompt,
    {
      "role": "user",
      "content": "Насколько выше доход у фрилансеров, принимающих оплату в криптовалюте, по сравнению с другими способами оплаты? "
    }
  ],
  temperature = 0.7
)
response_message = completion.choices[0].message.content
print(response_message )
```

SELECT
AVG(CASE WHEN Payment_Method = 'Crypto' THEN Earnings_USD END) AS avg_crypto_earnings,
AVG(CASE WHEN Payment_Method != 'Crypto' THEN Earnings_USD END) AS avg_non_crypto_earnings,
AVG(CASE WHEN Payment_Method = 'Crypto' THEN Earnings_USD END) - AVG(CASE WHEN Payment_Method != 'Crypto' THEN Earnings_USD END) AS earnings_difference
FROM freelancers
WHERE Payment_Method IS NOT NULL;

---

После получения запроса - распарсим его

```python
sql_query = response_message.strip()
sql_query
```

"SELECT \nAVG(CASE WHEN Payment_Method = 'Crypto' THEN Earnings_USD END) AS avg_crypto_earnings,\nAVG(CASE WHEN Payment_Method != 'Crypto' THEN Earnings_USD END) AS avg_non_crypto_earnings,\nAVG(CASE WHEN Payment_Method = 'Crypto' THEN Earnings_USD END) - AVG(CASE WHEN Payment_Method != 'Crypto' THEN Earnings_USD END) AS earnings_difference\nFROM freelancers\nWHERE Payment_Method IS NOT NULL;"

```python
result = pd.DataFrame()
with psycopg2.connect(
    "dbname=db user=user password=passw host=127.0.0.1 port=5440"
) as conn:
    result = pd.read_sql_query(sql_query, conn)
result
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_crypto_earnings</th>
      <th>avg_non_crypto_earnings</th>
      <th>earnings_difference</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5139.301556</td>
      <td>4973.993036</td>
      <td>165.30852</td>
    </tr>
  </tbody>
</table>
</div>

```python
# приведём результат в json
result_json = result.to_json(orient='records', force_ascii=False)
```

Отлично! После реглуировки температуры мы получаем примерно нужный нам результат.
Теперь нужно понять, как быть с полученными данными. Они динамические и алгоритмами будет очень трудно с ними что то делать.
Снова используем нейросеть. Но уже с другим контекстом.

На этот раз дадим ей подумать над агрегированными данными и выдать строковый ответ.

```python
post_promt_context = {
    "role": "system",
    "content": f"""Как аналитик, посмотри на данные и сделай выводы. Вывод опиши коротко. Вывод дай без форматирования. Только по данным, которые ты видишь в таблице."""
}
```

```python
completion = client.chat.completions.create(
  model="qwen/qwen3-30b-a3b:free",
  messages=[
    post_promt_context,
    {
      "role": "user",
      "content": result_json
    }
  ],
  temperature = 0.5
)
response_message = completion.choices[0].message.content
print(response_message )
```

Средние доходы от криптовалюты (5139.30) превышают средние доходы от не-криптовалютных источников (4973.99) на 165.31.
Нейросеть хорошо показала себя на первом вопросе! Теперь, попробуем остальные вопросы

Для начала - оформим все звпросы в виде функций

```python
async def input_prompt(question):
	completion = client.chat.completions.create(
	model="qwen/qwen3-30b-a3b:free",
	messages=[
		system_prompt,
		{
		"role": "user",
		"content": question
		}
	],
	temperature = 0.7
	)
	return completion.choices[0].message.content

async def hidden_prompt(result_json):
	completion = client.chat.completions.create(
	model="qwen/qwen3-30b-a3b:free",
	messages=[
		post_promt_context,
		{
		"role": "user",
		"content": result_json
		}
	],
	temperature = 0.5
	)
	return completion.choices[0].message.content

async def query_result(query):
	sql_query = query.strip()
	result = pd.DataFrame()
	with psycopg2.connect(
		"dbname=db user=user password=passw host=127.0.0.1 port=5440"
	) as conn:
		result = pd.read_sql_query(sql_query, conn)
	return result
```

```python
questions = [
    "Как распределяется доход фрилансеров в зависимости от региона проживания?",
    "Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?"
]

responses = []
for question in questions:
	query = await input_prompt(question)
	result = await query_result(query)
	response = await hidden_prompt(result.to_json(orient='records', force_ascii=False))
	responses.append({
		"question": question,
		"query": query,
		"result": result.to_dict(orient='records'),
		"response": response
	})

responses_df = pd.DataFrame(responses)
responses_df
```

<div>

<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

.dataframe tbody tr th {
vertical-align: top;
}

.dataframe thead th {
text-align: right;
}
</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>question</th>
      <th>query</th>
      <th>result</th>
      <th>response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Как распределяется доход фрилансеров в зависим...</td>
      <td>SELECT Client_Region, AVG(Earnings_USD) AS Ave...</td>
      <td>[{'client_region': 'Canada', 'average_earnings...</td>
      <td>Средние доходы клиентов по регионам: Canada (5...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Какой процент фрилансеров, считающих себя эксп...</td>
      <td>SELECT (COUNT(*) * 100.0 / (SELECT COUNT(*) FR...</td>
      <td>[{'percentage': 33.853354134165365}]</td>
      <td>Данные показывают значение процента в размере ...</td>
    </tr>
  </tbody>
</table>
</div>

```python
responses_df['response'][0]  # выводим ответ на первый вопрос
```

'Средние доходы клиентов по регионам: Canada (5350) — самый высокий, затем Asia (5172), UK (5047), Australia (4966), Europe (4891), USA (4873), Middle East (4871) — самый низкий. Разница между лидером и аутсайдером составляет ~48.'

```python
responses_df['response'][1]  # выводим ответ на второй вопрос
```

'Данные показывают значение процента в размере 33.85%.'
Попробуем попросить нейросеть составить дополнительные 5 вопросов по данной таблице

```python
for_requests = {
    "role": "system",
	"content": f"Твой контекст: {context}\n Ты аналитик данных и твоя задача - ответить на вопрос пользователя коротко и по существу."
}
```

```python
completion = client.chat.completions.create(
  model="qwen/qwen3-30b-a3b:free",
  messages=[
    for_requests,
    {
      "role": "user",
      "content": 'Придумай 5 вопросов в соответствии с контекстом. Отдели вопрос друг от друга переносами строки. Без форматирования и кавычек. Только вопросы.'
    }
  ],
  temperature = 1
)
response_message = completion.choices[0].message.content
print(response_message )
```

Какая профессиональная категория фрилансеров имеет самый высокий процент успешных завершений проектов
Какие платформы демонстрируют наибольшие средние показатели заработков у фрилансеров
Существует ли корреляция между уровнем опыта фрилансера и средним рейтингом, полученным от клиентов
Как маркетинговые расходы влияют на количество выполненных проектов у фрилансеров
Какие типы проектов связаны с наибольшей продолжительностью выполнения в днях

```python
questions = response_message.strip().split('\n')
```

```python
questions
```

['Какая профессиональная категория фрилансеров имеет самый высокий процент успешных завершений проектов  ',
'Какие платформы демонстрируют наибольшие средние показатели заработков у фрилансеров  ',
'Существует ли корреляция между уровнем опыта фрилансера и средним рейтингом, полученным от клиентов  ',
'Как маркетинговые расходы влияют на количество выполненных проектов у фрилансеров  ',
'Какие типы проектов связаны с наибольшей продолжительностью выполнения в днях']

```python
for question in questions:
	query = await input_prompt(question)
	result = await query_result(query)
	response = await hidden_prompt(result.to_json(orient='records', force_ascii=False))
	responses.append({
		"question": question,
		"query": query,
		"result": result.to_dict(orient='records'),
		"response": response
	})

responses_df = pd.DataFrame(responses)
```

<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>question</th>
      <th>query</th>
      <th>result</th>
      <th>response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Как распределяется доход фрилансеров в зависим...</td>
      <td>SELECT Client_Region, AVG(Earnings_USD) AS Ave...</td>
      <td>[{'client_region': 'Canada', 'average_earnings...</td>
      <td>Средние доходы клиентов по регионам: Canada (5...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Какой процент фрилансеров, считающих себя эксп...</td>
      <td>SELECT (COUNT(*) * 100.0 / (SELECT COUNT(*) FR...</td>
      <td>[{'percentage': 33.853354134165365}]</td>
      <td>Данные показывают значение процента в размере ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Какая профессиональная категория фрилансеров и...</td>
      <td>SELECT Job_Category, AVG(Job_Success_Rate) AS ...</td>
      <td>[{'job_category': 'Graphic Design', 'avg_succe...</td>
      <td>Средний уровень успеха в категории "Graphic De...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Какие платформы демонстрируют наибольшие средн...</td>
      <td>SELECT Platform, AVG(Earnings_USD) AS average_...</td>
      <td>[{'platform': 'Fiverr', 'average_earnings': 50...</td>
      <td>Все платформы имеют схожие средние заработки, ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Существует ли корреляция между уровнем опыта ф...</td>
      <td>SELECT CORR(\n    CASE WHEN Experience_Level =...</td>
      <td>[{'correlation': 0.004510618109876524}]</td>
      <td>Коэффициент корреляции равен **0.0045**, что у...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Как маркетинговые расходы влияют на количество...</td>
      <td>SELECT corr(Marketing_Spend, Job_Completed) AS...</td>
      <td>[{'correlation_coefficient': 0.035299152883827...</td>
      <td>Коэффициент корреляции (0.035) близок к нулю, ...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Какие типы проектов связаны с наибольшей продо...</td>
      <td>SELECT Project_Type, AVG(Job_Duration_Days) AS...</td>
      <td>[{'project_type': 'Hourly', 'average_duration'...</td>
      <td>Средняя продолжительность проектов типа "Hourl...</td>
    </tr>
  </tbody>
</table>
</div>

```python
responses_df.loc[:, ['question', 'response']]
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>question</th>
      <th>response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Как распределяется доход фрилансеров в зависим...</td>
      <td>Средние доходы клиентов по регионам: Canada (5...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Какой процент фрилансеров, считающих себя эксп...</td>
      <td>Данные показывают значение процента в размере ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Какая профессиональная категория фрилансеров и...</td>
      <td>Средний уровень успеха в категории "Graphic De...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Какие платформы демонстрируют наибольшие средн...</td>
      <td>Все платформы имеют схожие средние заработки, ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Существует ли корреляция между уровнем опыта ф...</td>
      <td>Коэффициент корреляции равен **0.0045**, что у...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Как маркетинговые расходы влияют на количество...</td>
      <td>Коэффициент корреляции (0.035) близок к нулю, ...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Какие типы проектов связаны с наибольшей продо...</td>
      <td>Средняя продолжительность проектов типа "Hourl...</td>
    </tr>
  </tbody>
</table>
</div>

Изучение ответов показывает, что нейросеть даёт ответы с форматированием. Учтём это в системном пре-промпте

## Оценка модели и пайплайна решений

На данный момент имеем модель, которая достаточно хорошо интерпретирует запросы пользователя в текстовый ответ.
А значит, имеем некоторый baseline.

Пропишем собственные SQL - запросы по данным вопросам

```sql
-- Как распределяется доход фрилансеров в зависимости от региона проживания?
SELECT AVG(earnings_usd) as avg_earnings_usd, client_region as region from freelancers group by client_region order by avg_earnings_usd DESC;
-- Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?

WITH total_freelancers AS (
    SELECT COUNT(freelancer_id) AS total FROM freelancers WHERE experience_level = 'Expert'
),
filtered_freelancers AS (
    SELECT COUNT(freelancer_id) AS count FROM freelancers WHERE job_completed < 100 and experience_level = 'Expert'
)
SELECT 
    (filtered.count * 100.0) / total.total AS percent
FROM 
    filtered_freelancers filtered, total_freelancers total;

-- Какая профессиональная категория фрилансеров имеет самый высокий процент успешных завершений проектов?
SELECT AVG(Job_Success_Rate) as avg_job_rate, job_category from freelancers group by job_category order by avg_job_rate DESC;

-- Какие платформы демонстрируют наибольшие средние показатели заработков у фрилансеров?
SELECT AVG(earnings_usd) as income_avg, platform from freelancers group by platform order by income_avg DESC;

-- Существует ли корреляция между уровнем опыта фрилансера и средним рейтингом, полученным от клиентов?

with _grouped AS (
SELECT 
    CASE experience_level
        WHEN 'Intermediate' THEN 2
        WHEN 'Expert' THEN 3
        WHEN 'Beginner' THEN 1
    END as experience_level,
    client_rating
FROM freelancers)
SELECT CORR(experience_level, client_rating) as correlate FROM _grouped

-- Как маркетинговые расходы влияют на количество выполненных проектов у фрилансеров?

SELECT CORR(marketing_spend, job_completed) as correlation from freelancers


-- Какие типы проектов связаны с наибольшей продолжительностью выполнения в днях?
select AVG(job_duration_days) as avg_duration, project_type from freelancers group by project_type order by avg_duration desc;
```

Какой вывод можно сделать?

- Часто, нейронная сеть пишет более простые запросы (они более быстродейственны и эффективны)
- Нейросеть умеет в семантику, в случае с корреляцией. Правильно проставляет ранги Intermediate / Beginner / Expert
- Ни в одном запросе нейросети не было допущено логических и синтаксических ошибок
- Выводы, которая делает нейросеть - не всегда однозначны. Это поможет решить более точное регулирование температуры в сторону нуля или сделать запоминание контекста, благодаря которому, пользователь сможет задачать уточняющие запросы по данным
