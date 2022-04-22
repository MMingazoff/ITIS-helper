import pandas as pd

df_student = pd.read_excel('data/all_students.xlsx')
list_group = set(df_student['Группа'])
