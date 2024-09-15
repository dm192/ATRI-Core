import numpy as np
import os
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
from datetime import datetime
import signal
import sys

# 默认对话数据
new_var = [
    [
        "你好",
        "我很好，谢谢！",
        "你呢？"
    ],
    #...省略其他对话部分，保持不变
]

DEFAULT_CONVERSATIONS = new_var

# 数据文件
data_file = 'pretrained_data.pkl'
memory_file = 'memory.pkl'

# 初始化分词器
def initialize_tokenizer(conversations):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([word for conversation in conversations for word in conversation])
    return tokenizer

# 准备数据
def prepare_data(conversations, tokenizer):
    input_sequences = []
    for conversation in conversations:
        for i in range(1, len(conversation)):
            n_gram_sequence = tokenizer.texts_to_sequences([conversation[:i+1]])[0]
            input_sequences.append(n_gram_sequence)
    
    if not input_sequences:
        raise ValueError("生成的序列数据为空，请检查对话数据。")
    
    max_sequence_length = max([len(x) for x in input_sequences])
    input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')
    X, y = input_sequences[:, :-1], input_sequences[:, -1]
    y = to_categorical(y, num_classes=len(tokenizer.word_index) + 1)
    return X, y, max_sequence_length

# 初始化模型
def initialize_model(input_shape, vocab_size):
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length=input_shape))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(vocab_size, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 保存模型、分词器和数据
def save_model_and_tokenizer(model, tokenizer):
    model.save('chatbot_model.keras')
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# 加载模型、分词器和数据
def load_model_and_tokenizer():
    model = None
    tokenizer = None
    if os.path.exists('chatbot_model.keras'):
        model = load_model('chatbot_model.keras')
    if os.path.exists('tokenizer.pickle'):
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
            print(f"分词器加载成功")
    return model, tokenizer

# 保存对话历史
def save_memory(memory):
    with open(memory_file, 'wb') as f:
        pickle.dump(memory, f)

# 加载对话历史
def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, 'rb') as f:
            memory = pickle.load(f)
        print("记忆加载成功")
    else:
        memory = []
    return memory

# 保存对话数据
def save_data(conversations):
    with open(data_file, 'wb') as f:
        pickle.dump(conversations, f)

# 加载对话数据
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'rb') as f:
            conversations = pickle.load(f)
    else:
        print(f"{data_file} 不存在，创建默认数据集")
        conversations = DEFAULT_CONVERSATIONS
        save_data(conversations)
    return conversations

# 生成响应
def generate_response(model, tokenizer, seed_text, next_words=10, temperature=1.0):
    if temperature < 0.5 or temperature > 2:
        raise ValueError("温度超出范围，应在 0.5 到 2 之间。")
    
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    max_sequence_length = model.input_shape[1]
    token_list = pad_sequences([token_list], maxlen=max_sequence_length, padding='pre')
    predicted_probs = model.predict(token_list, verbose=0)[0]
    predicted_probs = np.asarray(predicted_probs).astype('float64')
    predicted_probs = np.log(predicted_probs + 1e-10) / temperature
    predicted_probs = np.exp(predicted_probs)
    predicted_probs = predicted_probs / np.sum(predicted_probs)
    predicted_word_index = np.random.choice(len(predicted_probs), p=predicted_probs)
    predicted_word = tokenizer.index_word.get(predicted_word_index, '')
    return predicted_word

# 信号处理，确保在 Ctrl+C 时保存对话历史
def signal_handler(sig, frame):
    print("\n检测到 Ctrl+C，正在保存记忆...")
    save_memory(memory)
    print("记忆已保存，程序退出。")
    sys.exit(0)

# 主程序
def main():
    global memory
    conversations = load_data()
    model, tokenizer = load_model_and_tokenizer()
    memory = load_memory()

    if model is None or tokenizer is None:
        print("模型或分词器未找到，将使用默认设置进行初始化...")
        tokenizer = initialize_tokenizer(conversations)
        X, y, max_sequence_length = prepare_data(conversations, tokenizer)
        model = initialize_model(input_shape=max_sequence_length, vocab_size=len(tokenizer.word_index) + 1)
        model.fit(X, y, epochs=10, verbose=1)
        save_model_and_tokenizer(model, tokenizer)
    
    print("模型和分词器已准备好。")
    
    # 绑定 Ctrl+C 信号处理
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        user_input = input("你: ")
        
        # 增加对话历史记录
        memory.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_input': user_input
        })
        
        response = generate_response(model, tokenizer, user_input)
        print("ATRI: ", response)
        
        memory[-1]['response'] = response  # 将生成的响应加入到记忆中
        save_memory(memory)  # 实时保存记忆

if __name__ == "__main__":
    main()
