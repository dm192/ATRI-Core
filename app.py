import numpy as np
import os
import pickle
import signal
from datetime import datetime
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import random
import sys

# 默认对话数据
new_var = [
    ["你好", "我很好，谢谢！", "你呢？"],
    ["你是谁？", "我是高性能的人工智能，ATRI。", "很高兴认识你。"],
    # 更多对话...
]
DEFAULT_CONVERSATIONS = new_var
data_file = 'pretrained_data.pkl'
memory_file = 'memory.pkl'

# 数据保存与加载
def save_memory(memory):
    with open(memory_file, 'wb') as f:
        pickle.dump(memory, f)

def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, 'rb') as f:
            return pickle.load(f)
    return []

# 分词器与数据准备
def initialize_tokenizer(conversations):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([word for conversation in conversations for word in conversation])
    return tokenizer

def prepare_data(conversations, tokenizer):
    input_sequences = []
    for conversation in conversations:
        for i in range(1, len(conversation)):
            n_gram_sequence = tokenizer.texts_to_sequences([conversation[:i+1]])[0]
            input_sequences.append(n_gram_sequence)

    max_sequence_length = max([len(x) for x in input_sequences])
    input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')
    X, y = input_sequences[:, :-1], input_sequences[:, -1]
    y = to_categorical(y, num_classes=len(tokenizer.word_index) + 1)
    return X, y, max_sequence_length

# 模型初始化
def initialize_model(input_shape, vocab_size):
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length=input_shape))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dropout(0.2))  # 加入dropout防止过拟合
    model.add(Dense(vocab_size, activation='softmax'))
    optimizer = Adam(learning_rate=0.001, clipnorm=1.0)  # 使用梯度裁剪
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 增量训练
def incremental_training(model, tokenizer, conversations):
    X, y, max_sequence_length = prepare_data(conversations, tokenizer)
    model.fit(X, y, epochs=1, verbose=1)

# 生成响应
def generate_response(model, tokenizer, seed_text, next_words=1, temperature=0.7):
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
    
    return predicted_word if predicted_word else "..."

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

# 保存对话数据
def save_data(conversations):
    with open(data_file, 'wb') as f:
        pickle.dump(conversations, f)

# 加载模型、分词器
def load_model_and_tokenizer():
    model = None
    tokenizer = None
    if os.path.exists('chatbot_model.keras'):
        model = load_model('chatbot_model.keras')
    if os.path.exists('tokenizer.pickle'):
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
    return model, tokenizer

# 保存模型和分词器
def save_model_and_tokenizer(model, tokenizer):
    model.save('chatbot_model.keras')
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# 信号处理器，用于捕获 Ctrl+C
def signal_handler(sig, frame):
    print("\n捕获到 SIGINT 信号，正在保存模型和记忆数据...")
    save_model_and_tokenizer(model, tokenizer)
    save_memory(memory)
    print("保存完毕，程序即将退出。")
    sys.exit(0)

# 主程序
def main():
    global memory, model, tokenizer
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

    # 捕获 Ctrl+C 信号
    signal.signal(signal.SIGINT, signal_handler)

    counter = 0
    while True:
        try:
            user_input = input("你: ")
            
            # 处理对话历史
            memory.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user_input': user_input
            })
            
            # 生成回复
            response = generate_response(model, tokenizer, user_input)
            print("ATRI: ", response)
            
            memory[-1]['response'] = response
            conversations.append([user_input, response])
            save_memory(memory)

            # 控制增量训练频率
            counter += 1
            if counter % 5 == 0:
                incremental_training(model, tokenizer, conversations)
                save_model_and_tokenizer(model, tokenizer)

        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
