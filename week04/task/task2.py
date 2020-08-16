import pandas as pd

df = pd.DataFrame(
    {
        "A": [1, 2, 3, None],
        "B": [5, 6, 8, 7],
        "C": [9, None, 12, 11],
        "age": [33, 14, 13, 16],
        "id": [17, 18, 18, 10],
        "order_id": [19, 19, 19, 32],
    }
)
df2 = pd.DataFrame(
    {
        "A": [1, 2, 4, None, 12],
        "B": [5, 6, 8, 7, None],
        "C": [9, None, 12, 11, None],
        "age": [33, 14, 15, 16, None],
        "id": [17, 18, 18, 17, 12],
        "order_id": [19, 19, 19, 32, 12],
    }
)

# 1. SELECT * FROM data;
df.iloc[:, :]

# 2. SELECT * FROM data LIMIT 10;
df.iloc[:10, :]

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
df['id']

# 4. SELECT COUNT(id) FROM data;
df['id'].count()

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df[(df['id'] < 1000) & (df['age'] > 30)]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df.groupby('id').aggregate({
    "order_id": pd.Series.nunique
})

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(df, df2, how='inner', on='id')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([df, df2]).drop_duplicates()

# 9. DELETE FROM table1 WHERE id=10;
df.drop(df[df.id == 10].index, axis=0, inplace=True)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
df.drop('id', axis=1, inplace=True)