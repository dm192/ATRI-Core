import pickle
import json

# 从 JSON 文件加载数据
with open('pretrained_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 保存回 pickle 文件
with open('pretrained_data.pkl', 'wb') as f:
    pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

print("数据已保存回 pickle 文件。")
