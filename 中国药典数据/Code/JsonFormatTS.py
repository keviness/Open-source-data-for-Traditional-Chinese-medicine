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
        # 拼接"成份"和"组成"字段，生成"药物组成"
        comp = normalized_row.get("成份") or ""
        comp2 = normalized_row.get("组成") or ""
        if comp and comp2:
            drug_comp = f"{comp},{comp2}"
        else:
            drug_comp = comp or comp2
        normalized_row["药物组成"] = drug_comp
        normalized_data.append(normalized_row)
    # 写入Excel前去重
    df = pd.DataFrame(normalized_data, columns=columns + ["药物组成"])
    df = df.drop_duplicates()
    # 只保留class字段为中成药的数据
    df = df[df["class"] == "中成药"]
    # 去除"成份", "组成"字段都空的数据
    df = df[~(df["成份"].isnull() & df["组成"].isnull())]
    # 去除"功能主治"、"适应证"字段都空的数据
    df = df[~(df["功能主治"].isnull() & df["适应证"].isnull())]
    # 保留功能主治或者适应证字段含有“失眠”或者“焦虑”内容的数据
    '''
    mask = (
        df["功能主治"].fillna("").str.contains("失眠|焦虑", case=False, na=False) |
        df["适应证"].fillna("").str.contains("失眠|焦虑", case=False, na=False)
    )
    df = df[mask]
    '''
    # 去掉"成份", "组成"字段，只保留指定顺序字段
    columns_order = ["中心词", "class", "药物组成", "出处", "功能主治", "适应证", "分类", "药品类型"]
    df = df[columns_order]
    df.to_excel(excel_path, index=False)

# 示例用法
if __name__ == "__main__":
    jsonl_path = "D:/ProjectOpenSource/中医药开源数据/中国药典数据/Data/drug.json"  # 替换为你的json文件路径
    excel_path = "D:/ProjectOpenSource/中医药开源数据/中国药典数据/Result/drug_output.xlsx" # 替换为你想要保存的excel路径
    jsonl_to_excel(jsonl_path, excel_path)
