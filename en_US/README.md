# ATRI-Core
Concept and Implementation of Real-life ATRI

-------------

~~Believe me, I'm just a fervent ATRI enthusiast~~

First of all, ever since I encountered ATRI, I've been deeply fond of this character. Plus, ATRI being a robot somewhat aligns with reality, ~~thanks to a certain mysterious individual's encouragement~~, I conceived the idea of creating a real-life "True • ATRI".

After many days of contemplation ~~and late-night staring at ATRI~~, I have a rough outline for the entire plan.

### AI System
Firstly, the AI system is quite challenging. Imagine a miniaturized host that controls the entire body, alongside various sensors and whatnot, with its AI being the most demanding aspect—more powerful than ChatGPT-4o and integrated into a single host, making it quite tricky.

So, I thought of creating a completely new model. While browsing Bilibili (B站), I stumbled upon a video discussing the human brain's thinking process. I realized coding this wouldn't be too difficult. Thus, I plan to simulate the brain's thought process using C++, although I'm quite clueless about C++. But using other languages could pose speed issues, so... time to learn.

For the logical framework of the entire system, I currently have a vague concept: Input Information → Extract Information needing assessment and processing → Query Memory based on this information → Pre-process Emotional Module → Human-like Judgment Mechanism → Emotional Module handles emotional processing → Control System interpretation → Control peripherals for external output.

### Energy
Currently, I plan to use small-scale controlled nuclear fusion for energy (another idea from that mysterious individual). The advantage is ATRI can keep going even after ten generations in your family pass away; the downside is the same—it keeps going.

I don't know much about this, except China's "Sun" (not Liu Cixin's novel, the real one) uses a Tokamak device for nuclear fusion. Developing this involves significant physical and chemical challenges, with its mathematical model akin to a miniature star, ensuring it doesn't melt its shell physically and chemically, respectively.

If achieved, it should last at least 200 years.

### Remote Control (???)
Can you guess why I had this idea? It's because I saw Bonbu being possessed while browsing Bilibili, though it's not as cool in reality as in ZZZ (Zenless Zone Zero). To meet the tech requirements, we'll lightly borrow Elon Musk's brain-computer interface. If you're willing, you can strike a pose like in ZZZ and let ATRI act as your surrogate for anything. But it needs high-speed wireless connectivity!

For the technical details: Use WebSocket or high-power UHD (Ultra High Definition) connections. WebSocket might have latency issues if you stray too far; UHD might disconnect. Some artificial Earth satellites use UHD, but ground interference is a significant issue—technical problem.

For this feature, plan to use brain-computer interface for command control and sensory data transmission. Encryption is crucial, planning to use a proprietary encryption algorithm + verification.

### Peripherals and Hardware
For peripherals and hardware, I plan to follow the original design (not much to elaborate since implementing from the original isn't difficult, except it burns money).

Unmentioned in the original, for power, I plan to use high-power electric motors, adjusting voltage and adding appropriate force arms for effects. Processor and mainboard: Use existing OrangePi AIpro(20T), with self-developed hardware control system and Linux-based OS. Heat dissipation: Use semiconductor thermal conductive sheets to direct head (where mainboard resides) heat downward, while cooling liquid circulating through body simulates human skin capillaries for overall cooling and body temperature simulation. As for eating mentioned in the original... simulate human digestive system internally, but via incineration, chemical agents, and... (let's not go into too much detail).

### Budget and Funding
*To be added*

### Other Content, To Be Added

-------------

### Compilation
*Using Debian/Ubuntu as an example*

Firstly, install Python3, g++, git, and other tools using the following command:
```bash
sudo apt install python3 g++ git -y
```
Then, enter any directory you have read-write permissions for, and execute:
```bash
git clone https://github.com/dm192/ATRI-Core.git -b master
```
Wait for completion, then add executable permission to the compile script with:
```bash
chmod +x ./make/make.py
```
Proceed with compilation by executing:
```bash
./make/make.py
```
Once done, find your output files in `./out/.`
 
Due to my love for inside jokes, if there are any inaccuracies or modifications needed, please [PR](https://github.com/dm192/ATRI-Core/pulls)
