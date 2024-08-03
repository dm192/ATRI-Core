# ATRI-Core
The concept and realization of the real version of ATRI

-------------
~~Believe me, I am just an ardent ATRI pursuer~~  
First of all, I have liked this character since I saw ATRI. In addition, ATRI itself is a robot, which is at least somewhat related to reality.~~At the instigation of a mysterious person~~I came up with the idea of ​​creating a "Real ATRI" in reality.  
After many days of deep thinking~~and staring at ATRI in the middle of the night~~, I have a general idea of ​​the whole plan.  
### AI system
First of all, the AI ​​system is relatively difficult. You can imagine that a mini host has to control the whole person and take into account a mess of sensors and whatnot. The most performance-intensive part is its AI, which is even better than ChatGPT-4o. It also has to be integrated into a host, which is very tricky.  
So I thought that I should create a brand new model. When I was watching videos on Bilibili, I accidentally saw a video about the thinking process of the human brain. I thought about it and thought that it would not be too difficult to implement it with code. Then I planned to develop the entire AI system by simulating the thinking process of the human brain through C++. ~~I am indeed a high-performance person, haha~~  
But in fact, this is also a technical problem, because I know nothing about C++... but using other things will encounter problems with running speed, so... learn it  
For the logical framework of the entire system, I currently have a vague concept. First, from input information → extract information that needs to be judged and processed → query memory based on this information → emotional module preprocessing → simulate human brain judgment mechanism → hand it over to the emotional module for emotional processing → control system analysis → control peripherals to output  
### Energy
At present, I plan to use ~~eating and excretion~~small controlled nuclear fusion to provide energy (this is still the idea of ​​a certain mysterious person). The advantage of doing this is that after 10 generations of your family, ATRI can still be used; the disadvantage is that after 10 generations of your family, ATRI can still be used...  
I don’t know too much about this. I only know that the Chinese sun (not the one in Liu Cixin’s novel, the real one) uses a tokamak device to achieve nuclear fusion. The research and development of this thing seems to be very difficult in physics and chemistry. Its mathematical model is like a mini star. Physically, it must ensure that it does not melt the outer shell, but chemically, it is relatively simple.  

?> If it is realized, it will be no problem to use it for at least 200 years.

### Remote control (???)
Guess why I have this idea... The reason is that when I was browsing B station, I saw Bomb being possessed. This technology is not as cool as ZZZ (Zero Zone) in reality. In order to meet the technical requirements, we have to use Mr. Elon Musk's brain-computer interface. Then, if you want, you can also pose like in ZZZ, and let ATRI be your stand-in to do anything for you. But this requires a high-speed wireless connection!  
For the technical details of this function: use Websocket connection or high-power UHD connection, provided that you cannot run too far, otherwise the Websocket will have a certain delay and the UHD will be disconnected. Although some artificial earth satellites also use UHD, the interference on the ground is much more than in the air, which is a technical problem.  
For this function, I plan to use a brain-computer interface to achieve the transmission of control instructions and sensory data. Encryption is very important in this regard, and I plan to use an undisclosed encryption algorithm + verification to solve it.  
### Peripherals and hardware
In terms of peripherals and hardware, I plan to follow the original work, so I won’t describe it in detail (because the content in the original work is not difficult to implement at present, but it is just a waste of money)  
There are some places that are not mentioned in the original work. In terms of power, I plan to use a high-power motor and achieve the effect by adjusting the voltage and appropriately increasing the force arm.  
In terms of processors and main control boards, I plan to use the existing OrangePi AIpro (20T), plus my own hardware control system and self-developed operating system based on Linux.  
For heat dissipation, I plan to use a semiconductor heat conduction sheet to conduct the heat from the head (where the main control board is located) downward alone, and the heat below the head is dissipated by circulating the cooling fluid that imitates the capillaries in human skin, which can also be used to simulate body temperature.  
As for the eating mentioned in the original work... a human-like digestive system is set up in the body, but it is done by burning, adding chemical reagents, and then... (I won't say too much)  
The bus is currently planned to use I2C, which will be responsible for connecting all sensors, motors and other components to communicate with the main control board.  
### Budget
|Technology or components|Estimated budget|
|--------|-------|
|Small controlled nuclear fusion|*To be supplemented*|
|Brain-computer interface|*To be supplemented*|
|High-power wireless chip|*To be supplemented*|
|OrangePi AIpro(20T)| 1499 CNY |
|Artificial skin|*To be supplemented*|
|Self-developed operating system|*To be supplemented*|
|Heat dissipation|*To be supplemented*|
|*To be supplemented*|*To be supplemented*|

### Other content, to be supplemented

-------------
### Compile
***Take Debian / Ubuntu on x86_64 platform as an example***  
First, you need to install bash, g++, git and other tools. Use the following command to install:
```bash
sudo apt install bash g++ git -y
```
Then, go to any directory you like with read and write permissions and execute:
```bash
git clone https://github.com/dm192/ATRI-Core.git -b master
```
This will create an "ATRI-Core" folder in the current directory, go into it:
```bash
cd ./ATRI-Core/
```
Add executable permissions to the compilation script:
```bash
chmod +x ./make/make.sh
```
Then compile, execute:
```bash
./make/make.sh
```
After waiting for the execution to complete, you can see the output file in `./out/`.

?> If there is a compilation error, it is not your problem. If you know C++, please help me check the error...

*Since I like to play with memes too much, if there is any inappropriate expression or need to be modified, please [PR](https://github.com/dm192/ATRI-Core/pulls)*
