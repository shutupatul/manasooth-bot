from llm_integration import MentalHealthAssistant
from vector_store import retrieve_similar_chunks
import time

def chat():
    assistant = MentalHealthAssistant()
    print("Mental Health Assistant (Type 'quit' to exit)\n")
    print("I'm here to listen. You can share as much or as little as you'd like.\n")
    
    conversation_history = []
    
    while True:
        try:
            query = input("You: ").strip()
            if query.lower() == 'quit':
                print("\nThank you for sharing. Remember: Your feelings matter.\n")
                break
            if not query:
                continue
            
            start_time = time.time()
            
            # Retrieve context if needed
            context = ""
            if len(conversation_history) > 2:
                context = "\n".join(conversation_history[-2:])
            
            # Get response
            response = assistant.get_response(query, context)
            print(f"\nAssistant: {response}")
            print(f"[Response time: {time.time()-start_time:.1f}s]\n")
            
            # Maintain last 3 exchanges
            conversation_history.extend([f"User: {query}", f"Assistant: {response}"])
            conversation_history = conversation_history[-6:]  # Keep last 3 pairs
            
        except KeyboardInterrupt:
            print("\n\nClosing conversation. Be gentle with yourself today.\n")
            break

if __name__ == "__main__":
    chat()