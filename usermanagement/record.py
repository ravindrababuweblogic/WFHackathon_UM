import pyaudio
import wave
import os



def record_audio():
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    frames = []

    for i in range(0, int(44100 / 1024 * 5)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    audio.terminate()

    wf = wave.open('D:\\Python\\first_sample\\usermanagement\\recorded_audio.wav', 'wb')

    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()