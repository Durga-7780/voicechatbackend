from fastapi import APIRouter, Request, HTTPException
from aiortc import RTCPeerConnection, RTCSessionDescription
from pydantic import BaseModel
import uuid
import asyncio

router = APIRouter()

class OfferSchema(BaseModel):
    sdp: str
    type: str
    
peers = set()

async def on_ice_connection_state_change(pc):
    if pc.iceConnectionState == "failed" or pc.iceConnectionState == "closed":
        pc.close()
        if pc in peers:
            peers.remove(pc)

@router.post("/offer")
async def offer(offer_data: OfferSchema):
    """
    WebRTC Offer handler. 
    Accepts an SDP offer from the browser, creates an answer, 
    and handles incoming/outgoing audio tracks.
    """
    offer = RTCSessionDescription(sdp=offer_data.sdp, type=offer_data.type)

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    peers.add(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "failed":
            await pc.close()
            peers.discard(pc)

    @pc.on("track")
    def on_track(track):
        # Here we receive the user's audio track.
        # We would pipe this to Deepgram (STT), then Groq (LLM), and ElevenLabs (TTS).
        # We process incoming media stream and optionally return our own synthetic audio track.
        pass

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
