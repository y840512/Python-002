import pandas as pd
import numpy as np
import sys

output = sys.stdout
outputfile = open("result.txt", "w")
sys.stdout = outputfile

group = ['x', 'y', 'z']
data1 = pd.DataFrame({
    "id": [_ for _ in range(20)],
    "order_id": np.random.randint(15, 30, 20),
    "group": [group[x] for x in np.random.randint(0, len(group), 20)],
    "age": np.random.randint(15, 50, 20)
    })

# print(data1)

# 1. SELECT * FROM data;
print(data1)
print("##############################")

# 2. SELECT * FROM data LIMIT 10;
print(data1.head(10))
print("##############################")

# 3. SELECT id FROM data;
print(data1['age'])
print("##############################")

# 4. SELECT COUNT(id) FROM data;
print(data1['id'].count())
print("##############################")

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
print(data1[(data1['id'] < 1000) & (data1['age'] > 30)])
print("##############################")

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
print(data1.groupby('id').aggregate({'order_id': 'nunique'}))
print("##############################")

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
data2 = pd.DataFrame({
    "id": [_ for _ in range(10)],
    "group": [group[x] for x in np.random.randint(0, len(group), 10)] ,
    "salary": np.random.randint(5, 50, 10),
    })
print(pd.merge(data1, data2, on= 'id', how='inner'))
print("##############################")

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
print(pd.merge(data1, data2))
print("##############################")

# 9. DELETE FROM table1 WHERE id=10;
print(data1[data1['id'] != 10])
print("##############################")

# 10. ALTER TABLE table1 DROP COLUMN column_name;
print(data1.drop('age', axis=1))
print("##############################")

outputfile.close()