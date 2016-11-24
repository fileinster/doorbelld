# doorbelld
A simple doorbell intercom for Raspberry Pi

Dependancies:
ffmpeg-0.10.7
pjproject-2.1.0
SDL-2.0.5-10608

Install packaged dependecies
sudo apt install libv4l-dev libx264-dev libssl-dev libasound2-dev

Requires an external SIP server (e.g. Asterisk)


Notable mentions:
https://github.com/tmakkonen/sipcmd

Setup help from http://marpoz.blogspot.co.uk/2013/05/build-door-berry-dependencies.html
SDL
  cd 
  mkdir tmp 
  cd $HOME/tmp 
  wget http://www.libsdl.org/tmp/SDL-2.0.tar.gz 
  tar xvfz SDL-2.0.tar.gz
  cd SDL-2.0.0-7125/ 
  ./configure 
  make 
  sudo make install

FFMPEG
  cd $HOME/tmp 
  wget http://ffmpeg.org/releases/ffmpeg-0.10.7.tar.bz2 
  tar xvfj ffmpeg-0.10.7.tar.bz2 
  cd ffmpeg-0.10.7 
  ./configure --enable-shared --disable-static --enable-memalign-hack --enable-gpl --enable-libx264 
  make 
  sudo make install

Build PjSIP
  cd $HOME/tmp 
  wget http://www.pjsip.org/release/2.1/pjproject-2.1.tar.bz2 
  tar xvfj pjproject-2.1.tar.bz2 
  cd pjproject-2.1.0/
  ./configure --disable-video 
  make dep 
  make


