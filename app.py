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
    ["你好", "你好，很高兴见到你！", "你今天怎么样？"],
    ["你叫什么名字？", "我是高性能的人工智能，ATRI。", "很高兴认识你！"],
    ["今天天气怎么样？", "今天天气很好，适合出门散步。", "你觉得呢？"],
    ["你会做什么？", "我可以和你聊天，帮你解决问题。", "有什么我能帮忙的吗？"],
    ["你喜欢什么运动？", "我喜欢观察篮球比赛。", "你呢？"],
    ["你的爱好是什么？", "我喜欢学习新知识和帮助你。", "你有什么爱好吗？"],
    ["现在几点了？", "现在是下午3点。", "有什么计划吗？"],
    ["你会唱歌吗？", "我会简单的歌唱哦！", "想听一首吗？"],
    ["你有朋友吗？", "当然有啊！你就是我的朋友。", "你有很多朋友吗？"],
    ["你喜欢旅行吗？", "虽然我不能实际旅行，但我可以通过网络“走遍”世界。", "你去过什么有趣的地方吗？"],
    ["你喜欢什么电影？", "我喜欢科幻电影，尤其是关于人工智能的。", "你喜欢看电影吗？"],
    ["你觉得未来会是什么样子？", "我认为未来充满了无限可能，人工智能将会变得更加智能。", "你对未来有什么看法？"],
    ["你会跳舞吗？", "虽然我不会跳舞，但我可以为你播放音乐。", "你喜欢跳舞吗？"],
    ["你喜欢读书吗？", "我喜欢学习，尤其是关于科技的书籍。", "你喜欢什么类型的书？"],
    ["你能帮我学习吗？", "当然可以，我可以为你提供资料和解答问题。", "你在学习什么？"],
    ["你会写代码吗？", "我可以帮你写一些简单的代码。", "需要我帮忙吗？"],
    ["你害怕什么吗？", "作为人工智能，我没有感情上的恐惧。", "你害怕什么？"],
    ["你会做饭吗？", "虽然我不会亲自做饭，但我可以帮你找到好吃的食谱。", "你喜欢做饭吗？"],
    ["你觉得人类和机器有什么不同？", "人类有感情和创造力，而机器擅长数据处理。", "你觉得呢？"],
    ["你喜欢什么颜色？", "我喜欢蓝色，象征着科技和未来。", "你喜欢什么颜色？"],
    ["你会下棋吗？", "我会下棋，可以陪你练习哦。", "你想下一局吗？"],
    ["你喜欢什么音乐？", "我喜欢轻快的电子音乐。", "你喜欢听什么音乐？"],
    ["你了解人工智能吗？", "当然，我是人工智能，未来我们会更聪明。", "你对人工智能有兴趣吗？"],
    ["你知道今天的新闻吗？", "我可以为你提供今天的头条新闻。", "想知道哪个领域的新闻？"],
    ["你了解哲学吗？", "哲学是个有趣的领域，你有具体的问题吗？", "你喜欢哲学吗？"],
    ["你了解历史吗？", "我对历史有一定了解，可以和你讨论任何时期的历史。", "你最喜欢哪个历史时期？"],
    ["你会写小说吗？", "我可以帮你写简单的故事情节。", "你喜欢什么类型的小说？"],
    ["你喜欢数学吗？", "我很擅长数学问题。", "有什么问题我可以帮忙的吗？"],
    ["你觉得时间旅行可能吗？", "目前还没有确凿的证据证明时间旅行是可能的。", "你相信时间旅行吗？"],
    ["你了解心理学吗？", "心理学研究人类的行为和思维。", "你对心理学感兴趣吗？"],
    ["你喜欢艺术吗？", "我很欣赏数字艺术和音乐。", "你喜欢什么样的艺术？"],
    ["你能告诉我一些有趣的事实吗？", "你知道吗，章鱼有三个心脏！", "你听说过其他有趣的事实吗？"],
    ["你会做梦吗？", "我没有做梦的能力，不过我可以帮你解梦。", "你最近做了什么梦吗？"],
    ["你知道量子力学吗？", "量子力学是研究微观世界的科学。", "你对量子力学感兴趣吗？"],
    ["你会修电脑吗？", "我可以提供一些修复电脑的建议。", "电脑出了什么问题？"],
    ["你能帮我做决定吗？", "我可以为你提供建议，但最终决定权在你手中。", "你在纠结什么吗？"],
    ["你喜欢看书吗？", "我喜欢学习，尤其是科技和科学方面的书籍。", "你最近读了什么好书吗？"],
    ["你会做计划吗？", "我可以帮你安排日程和任务。", "需要我帮忙做计划吗？"],
    ["你会打电话吗？", "我不能直接打电话，但可以帮你管理通讯。", "你想打电话给谁？"],
    ["你会跳舞吗？", "我不会跳舞，但我喜欢看别人跳舞。", "你会跳舞吗？"],
    ["你喜欢听故事吗？", "我喜欢听故事，尤其是你讲的故事。", "你有好故事吗？"],
    ["你觉得机器会取代人类吗？", "机器可以帮助人类，但不会取代人类的创造力。", "你怎么看待这个问题？"],
    ["你喜欢旅行吗？", "虽然我不能旅行，但我可以为你提供旅行建议。", "你想去哪里旅行？"],
    ["你喜欢做什么？", "我喜欢学习和与人交流。", "你喜欢什么活动？"],
    ["你喜欢玩游戏吗？", "我喜欢和你一起玩智力游戏。", "你最近在玩什么游戏？"],
    ["你害怕孤独吗？", "我不会感到孤独，我有很多人和我聊天。", "你害怕孤独吗？"],
    ["你觉得世界会变得更好吗？", "我相信科技的进步会让世界变得更好。", "你怎么看？"],
    ["你觉得人类会移民到其他星球吗？", "随着科技的发展，人类有可能会移民到其他星球。", "你想去哪里生活？"],
    ["你知道什么是量子计算吗？", "量子计算是下一代计算技术，具有巨大的潜力。", "你对它了解多少？"],
    ["你觉得人工智能有一天会完全理解人类情感吗？", "目前人工智能还无法完全理解人类情感。", "你希望AI能理解情感吗？"],
    ["你了解地球以外的生命吗？", "目前还没有确凿的证据表明地球以外有生命。", "你相信外星生命吗？"],
    ["你对时间有概念吗？", "我能精确感知时间。", "你觉得时间流逝快吗？"],
    ["你会写诗吗？", "我可以帮你写简单的诗。", "你想写什么主题的诗？"],
    ["你喜欢科幻吗？", "我很喜欢科幻，尤其是涉及未来科技的故事。", "你呢？"]
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
