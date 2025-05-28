import json
import pandas as pd

def jsonl_to_excel(jsonl_path, excel_path):
    data = []
    columns = set()
    # 读取每一行，解析为字典，并收集所有键
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                # 将值为list的项用逗号拼接为字符串
                for k, v in row.items():
                    if isinstance(v, list):
                        row[k] = ",".join(map(str, v))
                data.append(row)
                columns.update(row.keys())
    columns = list(columns)
    # 规范化所有行，缺失的键补None
    normalized_data = []
    for row in data:
        normalized_row = {col: row.get(col, None) for col in columns}
        normalized_data.append(normalized_row)
    # 写入Excel前去重
    df = pd.DataFrame(normalized_data, columns=columns)
    df = df.drop_duplicates()
    df.to_excel(excel_path, index=False)

# 示例用法
if __name__ == "__main__":
    jsonl_path = "D:/ProjectOpenSource/中医药开源数据/中国药典数据/Data/drug.json"  # 替换为你的json文件路径
    excel_path = "D:/ProjectOpenSource/中医药开源数据/中国药典数据/Result/drug_output.xlsx" # 替换为你想要保存的excel路径
    jsonl_to_excel(jsonl_path, excel_path)
