import pyaudio
import wave
from flask import Flask, session
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def record_audio():
    
    username = session.get("username")
    print(username)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    frames = []

    for i in range(0, int(44100 / 1024 * 10)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    audio.terminate()

    wf = wave.open('D:\\Python\\first_sample\\Hackathon_UM\\usermanagement\\'+username+'.wav', 'wb')
    #wf = wave.open('D:\\Python\\first_sample\\Hackathon_UM\\usermanagement\\record.wav', 'wb')

    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    uploadToBlob(username)


def uploadToBlob(username) :
    # Initialize the connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=forblobwf;AccountKey=jVlmKuq+bwcCRykGhRMzETzW0BsOA6FYZrFG6n5ni0FEzT8UOYE2xPqGooFy9jT15ydld9ayPZmS+ASt4veXAw==;EndpointSuffix=core.windows.net"

    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Initialize the ContainerClient
    container_name = "blobwf"
    container_client = blob_service_client.get_container_client(container_name)

    # Initialize the BlobClient
    blob_name = username+".wav"
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)

    # List all blobs in the container
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        print("Blob name: ", blob.name)

    # Upload a file to the blobc
    with open("D:\\Python\\first_sample\\Hackathon_UM\\usermanagement\\"+username+".wav", "rb") as data:
        blob_client.upload_blob(data, overwrite="true")

    # Download a file from the blob
    with open("record.wav", "wb") as file:
        file.write(blob_client.download_blob().readall())

