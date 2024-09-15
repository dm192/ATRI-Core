import pickle
import json

# 从 pickle 文件中加载数据
with open('pretrained_data.pkl', 'rb') as f:
    data = pickle.load(f)

# 保存为 JSON 文件
with open('pretrained_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("数据已保存为 JSON 文件。")
