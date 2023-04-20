import pyaudio
from time import sleep
import whisper
import numpy as np
import os
import torch
from tempfile import NamedTemporaryFile
import speech_recognition as sr
import array
import io

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
    
    #audio_data = b''.join(frames)
    #return audio_data
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
    

def transcribe_audio_data(audio_data, sample_rate_hz):
    #print(audio_data)
    #byte_data = bytes(audio_data)
    #print(type(byte_data))
    #if isinstance(audio_data, (list, array.array)):
    #    byte_data = bytes(audio_data)
    #    print("1: ",type(byte_data))
    #elif isinstance(audio_data, bytes):
    #    byte_data = audio_data
    #    print("2: ",type(byte_data))
    #else:
    #    raise ValueError("Unsupported audio_data type")
    #print(type(byte_data))
    
    #with open(temp_file,'w+b')as f:
       # f.write(byte_data)\
    # Write wav data to the temporary file as bytes.
    #arr = []
    #transcription = ['']
    #whisper_model = whisper.load_model("base")  # 모델 이름 변경
    #print("Whisper model loaded")
    #audio_np = np.array(audio_data,dtype=np.float32)
   # audio_np = np.frombuffer(audio_data, dtype=np.float32)
    #with open(temp_file,'rb') as f:
    #    audio_bytes = f.read()
    
    wav_data = io.BytesIO(audio_data.get_wav_data())
    # Write wav data to the temporary file as bytes.
    with open(temp_file, 'w+b') as f:
        f.write(wav_data.read())

    
    whisper_model = whisper.load_model("base")  # 모델 이름 변경
    print("Whisper model loaded")
    # load audio and pad/trim it to fit 30 seconds
   # audio = whisper.load_audio(audio_data)
   # audio = whisper.pad_or_trim(audio)
#
   # # make log-Mel spectrogram and move to the same device as the model
   # mel = whisper.log_mel_spectrogram(audio).to(model.device)
#
   # # detect the spoken language
   # _, probs = model.detect_language(mel)
   # print(f"Detected language: {max(probs, key=probs.get)}")
#
   # # decode the audio
   # options = whisper.DecodingOptions()
   # result = whisper.decode(model, mel, options)
   # return result.text
   # audio = whisper.load_audio(audio_data)
   # audio = whisper.pad_or_trim(audio)
   # mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
   # _, probs = whisper_model.detect_language(mel)
   # print(f"Detected language: {max(probs, key=probs.get)}")
   # options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16 = False)
   # result = whisper.decode(whisper_model, mel, options)
   # print(result.text)
    
    #result = whisper_model.transcribe(audio_data)
    ##print(result['text'])
    #audio_np = np.frombuffer(audio_data, dtype=np.float32)
    
    #transcriptions = whisper_model.transcribe(audio_np)
    #for transcription in transcriptions:
    # load model and processor
     #    print(f"Transcript: {transcription.text}")
    #with whisper_model.transcribe() as transcriber:
    #    transcriber.feed(audio_data, sample_rate_hz)
    #    transcriptions = transcriber.transcribe()
    #    for transcription in transcriptions:
    #        print(f"Transcript: {transcription.text}")
            
            
    result = whisper_model.transcribe(temp_file,fp16=torch.cuda.is_available())
    text = result['text'].strip()
    #transcription = [text]  # 이전 결과를 대체
    os.system('cls' if os.name=='nt' else 'clear')
    #for line in transcription:
    for line in text:
        print(line)
    print('', end='', flush=True)
    # sleep(0.25)  # 무한 루프가 없는 경우 이 줄을 삭제하거나 주석 처리할 수 있습니다.

  #  transcription = ['']
  #  whisper_model = whisper.load_model("Base")
  #  print("Whisper model loaded")
  #  audio_np=np.frombuffer(audio_data, dtype=np.float32)
  # # audio= torch.from_numpy(audio_np)
  #  result = whisper_model.transcribe(audio_np)
  #  text = result['text'].strip()
  #  transcription.append(text)
  #   # Clear the console to reprint the updated transcription.
  #  os.system('cls' if os.name=='nt' else 'clear')
  #  for line in transcription:
  #      print(line)
  #  # Flush stdout.
  #  print('', end='', flush=True)
#
  #  # Infinite loops are bad for processors, must sleep.
  #  sleep(0.25)
    #audio_np = np.frombuffer(audio_data, dtype=np.int32)
   ##time_stamps = get_speech_ts( audio_np, model, sampling_rate=ARGS.rate)

     # Call transcribe() method with numpy array
    #transcriptions = whisper_model.transcribe(audio=audio_np, padding=sample_rate_hz)

    #print(transcriptions['text'])
        
    #transcriptions = whisper_model.transcribe(audio=audio_np,padding=sample_rate_hz)
    print(f"Transcript: {transcriptions.text}")

    #transcriptions = whisper.transcribe(audio_data, sample_rate_hz, whisper_model)
    #for transcription in transcriptions:
    #    print(f"Transcript: {transcription.text}")
    #with whisper_model.transcribe() as transcriber:
    #    transcriber.feed(audio_data, sample_rate_hz)
    #    transcriptions = transcriber.transcribe()
    #    for transcription in transcriptions:
    #        print(f"Transcript: {transcription.text}")

if __name__ == "__main__":
    input_device_index = select_input_device()
    output_device_index = get_matched_output_device(input_device_index)
    temp_file = NamedTemporaryFile(suffix='.wav', delete=False).name
    print("temp_file : ", temp_file)

    if output_device_index is None:
        print("No matching output device found.")
    else:
        duration = 3
        recorded_audio = record_audio(input_device_index, duration)
        play_audio(output_device_index, recorded_audio)
        
        transcribe_audio_data(recorded_audio, 44100)
       
        
   