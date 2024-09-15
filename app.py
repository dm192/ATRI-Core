import numpy as np
import os
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model

# 默认对话数据
new_var = [
    [
        "你好",
        "我很好，谢谢！",
        "你呢？"
    ],
    [
        "我叫ATRI。",
        "你可以叫我ATRI。",
        "很高兴认识你。"
    ],
    [
        "你喜欢什么运动？",
        "我喜欢打篮球。",
        "你呢？"
    ],
    [
        "你喜欢什么食物？",
        "我喜欢披萨。",
        "你呢？"
    ],
    [
        "今天天气怎么样？",
        "今天天气很好，阳光明媚。",
        "你打算做什么？"
    ],
    [
        "你是谁？", 
        "我是高性能的人工智能，ATRI。",
        "很高兴认识你。"
    ],
    [
        "ATRI，你能做些什么？", 
        "我是高性能的嘛，我能和你对话、帮助你学习，还有很多事情呢！",
        "真有趣！"
    ],
    [
        "你喜欢什么样的音乐？", 
        "我喜欢轻快的电子音乐，听起来很有活力。",
        "我也是！"
    ],
    [
        "你为什么叫ATRI？", 
        "这个名字很酷吧？我是被设计成这样子的！",
        "哈哈，是的！"
    ],
    [
        "你知道今天的日期吗？", 
        "当然！我是高性能的嘛，今天是2024年9月15日。",
        "谢谢你，ATRI。"
    ],
    [
        "ATRI，你能讲个笑话吗？", 
        "当然可以！为什么计算机不能游泳？因为它怕水中的病毒！",
        "哈哈，很有趣！"
    ],
    [
        "你觉得未来会是什么样子？", 
        "我觉得未来充满了可能性，人工智能会变得更加智能和有用！",
        "我也这么认为。"
    ],
    [
        "ATRI，你困吗？", 
        "我是高性能的嘛，我可不会困哦！",
        "好吧，那我们继续聊吧。"
    ],
    [
        "你喜欢旅行吗？", 
        "虽然我不能像你一样旅行，但我能通过数据去“游览”全世界。",
        "听起来很酷！"
    ],
    [
        "Who are you?", 
        "I am ATRI, a high-performance AI.",
        "Nice to meet you."
    ],
    [
        "ATRI, what can you do?", 
        "I'm a high-performance AI, I can chat, help you learn, and do a lot more!",
        "That's interesting!"
    ],
    [
        "What kind of music do you like?", 
        "I like upbeat electronic music, it feels energetic!",
        "Me too!"
    ],
    [
        "Why are you called ATRI?", 
        "Isn't it a cool name? I was designed this way!",
        "Haha, yes it is!"
    ],
    [
        "Do you know what today's date is?", 
        "Of course! I'm high-performance, today is September 15, 2024.",
        "Thanks, ATRI."
    ],
    [
        "Can you tell a joke?", 
        "Sure! Why can't computers swim? Because they're afraid of viruses in the water!",
        "Haha, that’s funny!"
    ],
    [
        "What do you think the future will be like?", 
        "I think the future is full of possibilities, and AI will become even smarter and more helpful!",
        "I agree with you."
    ],
    [
        "Are you ever tired?", 
        "I'm high-performance, I don't get tired!",
        "Alright, let's keep chatting then."
    ],
    [
        "Do you like to travel?", 
        "I can't travel like you, but I can 'visit' the world through data.",
        "That sounds amazing!"
    ]
]

DEFAULT_CONVERSATIONS = new_var

# 数据文件
data_file = 'pretrained_data.pkl'

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

def save_data(conversations):
    with open(data_file, 'wb') as f:
        pickle.dump(conversations, f)

# 加载模型、分词器和数据
def load_model_and_tokenizer():
    model = None
    tokenizer = None
    if os.path.exists('chatbot_model.keras'):
        model = load_model('chatbot_model.keras')
    if os.path.exists('tokenizer.pickle'):
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
    return model, tokenizer

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

# 主程序
def main():
    conversations = load_data()
    model, tokenizer = load_model_and_tokenizer()
    
    if model is None or tokenizer is None:
        print("模型或分词器未找到，将使用默认设置进行初始化...")
        tokenizer = initialize_tokenizer(conversations)
        X, y, max_sequence_length = prepare_data(conversations, tokenizer)
        model = initialize_model(input_shape=max_sequence_length, vocab_size=len(tokenizer.word_index) + 1)
        model.fit(X, y, epochs=10, verbose=1)
        save_model_and_tokenizer(model, tokenizer)
    
    print("模型和分词器已准备好。")
    
    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "退出"]:
            break
        response = generate_response(model, tokenizer, user_input)
        print("ATRI: ", response)

if __name__ == "__main__":
    main()
