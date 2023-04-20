import pyaudio

# 상수 정의
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# PyAudio 객체 초기화
p = pyaudio.PyAudio()

# 스트림 열기
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Start streaming...")

try:
    while True:
        # 스피커에서 데이터 읽기
        data = stream.read(CHUNK)
        # 읽은 데이터를 스피커에 출력
        stream.write(data, CHUNK)
except KeyboardInterrupt:
    print("End streaming.")

# 스트림 정리
stream.stop_stream()
stream.close()

# PyAudio 객체 종료
p.terminate()