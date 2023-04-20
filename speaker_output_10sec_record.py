import pyaudio
import time

def select_device():
    p = pyaudio.PyAudio()

    print("Available devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"{i}: {device_info['name']}")

    selected_device = int(input("Select the input device index: "))
    return selected_device

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
    device_index = select_device()
    duration = 10
    recorded_audio = record_audio(device_index, duration)
    play_audio(device_index, recorded_audio)