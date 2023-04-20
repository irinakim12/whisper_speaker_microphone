import pyaudio
import time

def select_input_device():
    p = pyaudio.PyAudio()

    print("Available input devices:")

    input_devices = {}
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)

        if device_info["maxInputChannels"] > 0:  # 입력 장치만 선택
            device_name = device_info['name']
            if device_name not in input_devices.values():
                input_devices[i] = device_name
                print(f"{i}: {device_name}")

    selected_device = int(input("Select the input device index: "))
    return selected_device

def get_matched_output_device(input_device_index):
    p = pyaudio.PyAudio()
    input_device_info = p.get_device_info_by_index(input_device_index)
    host_api = input_device_info['hostApi']
    host_api_info = p.get_host_api_info_by_index(host_api)

    output_devices = {}
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)

        # 입력 장치와 같은 호스트 API를 사용하는 출력 장치 찾기
        if device_info['hostApi'] == host_api and device_info['maxOutputChannels'] > 0:
            device_name = device_info['name']
            if device_name not in output_devices.values():
                output_devices[i] = device_name
                return i

    # 일치하는 출력 장치가 없으면 None 반환
    return None

def record_audio(device_index, duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

    print("Start recording...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames

def play_audio(device_index, frames):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    output_device_index=device_index,
                    frames_per_buffer=CHUNK)

    print("Start playing...")

    for frame in frames:
        stream.write(frame, CHUNK)

    print("Playback finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    input_device_index = select_input_device()
    output_device_index = get_matched_output_device(input_device_index)

    if output_device_index is None:
        print("No matching output device found.")
    else:
        duration = 10
        recorded_audio = record_audio(input_device_index, duration)
        play_audio(output_device_index, recorded_audio)
