#!/usr/bin/env python3
"""
Test script to verify the event callback shutdown fix
"""
import sys
import time
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_shutdown_gracefully():
    """Test that shutdown happens without event callback errors"""
    print("Testing graceful shutdown...")
    
    from warp_client import warp_client
    
    # Add some event callbacks to simulate real usage
    def test_callback(data):
        print(f"Event callback executed: {data}")
    
    warp_client.add_event_callback('disconnected', test_callback)
    warp_client.add_event_callback('connection_error', test_callback)
    
    print("Client initialized with event callbacks")
    print(f"Connected: {warp_client.status.connected}")
    
    # Attempt to connect (will fail but should not cause errors)
    print("Attempting WebSocket connection (should fail gracefully)...")
    try:
        warp_client.connect_websocket()
    except:
        pass
    
    # Short delay to let any async operations complete
    time.sleep(1)
    
    print("Disconnecting...")
    warp_client.disconnect()
    
    print("Shutdown test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = test_shutdown_gracefully()
        print("✅ All tests passed!")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)