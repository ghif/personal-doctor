import streamlit as st
from services.tts_service import get_summary_tts

def audio_player():
    """
    Audio player component for TTS responses
    """
    print("🔍 DEBUG: Audio Player Component called")
    
    if 'last_response' in st.session_state and st.session_state.last_response:
        response_text = st.session_state.last_response.strip()
        
        if len(response_text) > 10:
            with st.container():
                st.markdown("**🔊 Listen to Summary**")
                
                button_key = f"play_audio_{hash(response_text)}"
                
                # Callback function to handle button click
                def handle_audio_generation():
                    print("🎯 Button callback triggered!")
                    # Send full text to summary service
                    tts_text = response_text
                    print(f"Generating summary audio for text length: {len(tts_text)}...")
                    
                    try:
                        audio_bytes = get_summary_tts(tts_text)
                        print(f"Summary TTS service returned: {len(audio_bytes) if audio_bytes else 0} bytes")
                        
                        if audio_bytes and len(audio_bytes) > 0:
                            st.session_state['generated_audio'] = audio_bytes
                            print("✅ Audio stored in session state")
                        else:
                            st.session_state['generated_audio'] = None
                            print("❌ Audio generation failed")
                    except Exception as e:
                        print(f"Audio generation error: {e}")
                        st.session_state['generated_audio'] = None
                    
                    # Display audio if available in session state
                    if 'generated_audio' in st.session_state and st.session_state['generated_audio']:
                        print("✅ Displaying generated audio")
                        st.success("🎵 Audio Summary ready!")
                        st.audio(st.session_state['generated_audio'], format="audio/wav")
                        
                        # Save debug file
                        try:
                            with open("debug_audio.wav", "wb") as f:
                                f.write(st.session_state['generated_audio'])
                            st.info("Audio saved as debug_audio.wav for testing")
                            print("Debug audio file saved successfully")
                        except Exception as save_error:
                            print(f"Failed to save debug file: {save_error}")
                    
                    elif 'generated_audio' in st.session_state and st.session_state['generated_audio'] is None:
                        print("❌ Showing audio generation error")
                        st.error("❌ Failed to generate audio")
                        st.info("💡 Check backend TTS service")
                    
                    st.info("🎧 Click 'Play Audio' to hear the AI summary")
                
                # Button with callback
                button_clicked = st.button(
                    "🔊 Play Audio Summary", 
                    key=button_key, 
                    type="secondary",
                    on_click=handle_audio_generation
                )
                
                print(f"Button clicked: {button_clicked}")
                
                
        else:
            print("⚠️ Response too short for audio generation")
            st.info("Response too short for audio generation")
    else:
        print("ℹ️ No response available for audio generation")
        st.info("No response available for audio generation")

    print("=" * 50)
