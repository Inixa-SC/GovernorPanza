import gradio as gr
import time

# 1. ADD USER MESSAGE
def add_user_message(msg, history):
    history = history or []
    new_history = history + [{"role": "user", "content": msg}]
    return "", new_history

# 2. MAIN BOT RESPONSE
def bot_response(history):
    user_message = history[-1]["content"]
    
    # Handle the list wrapper issue here too just in case
    if isinstance(user_message, list):
        user_message = " ".join(str(x) for x in user_message)

    bot_content = f"I am the main AI. I received: '{user_message}'."
    
    history.append({"role": "assistant", "content": ""})
    
    for char in bot_content:
        history[-1]["content"] += char
        time.sleep(0.03)
        yield history

# 3. VERIFIER RESPONSE (The Fix is Applied Here)
def verifier_response(history):
    raw_content = history[-1]["content"]
    
    # --- FIX START ---
    # Handle Gradio 6.0 wrapping text in lists
    if isinstance(raw_content, list):
        main_bot_content = " ".join(str(item) for item in raw_content)
    else:
        main_bot_content = str(raw_content)
    # --- FIX END ---

    if "stupid" in main_bot_content.lower():
        status = "❌ REJECTED"
        color = "#ffebee" # Red
        border = "#ef5350"
    else:
        status = "✅ VERIFIED"
        color = "#e8f5e9" # Green
        border = "#66bb6a"

    verifier_content = f"""
    <div style="
        background-color: {color}; 
        border: 2px solid {border}; 
        border-radius: 10px; 
        padding: 10px; 
        margin-bottom: 5px;">
        <h3 style="margin: 0; color: #333;">🕵️‍♂️ Verifier Agent</h3>
        <hr style="margin: 5px 0; border-color: {border}; opacity: 0.5;">
        <p style="margin: 0;"><b>Audit:</b> The previous response has been checked.</p>
        <p style="margin: 0;"><b>Status:</b> {status}</p>
    </div>
    """
    
    # Append the verification block
    history.append({"role": "assistant", "content": verifier_content})
    yield history

# --- INTERFACE ---
with gr.Blocks() as demo:
    gr.Markdown("## Chatbot with 'Verifier' Agent")
    
    # Chatbot Component
    chatbot = gr.Chatbot(height=1000)
    
    msg = gr.Textbox(placeholder="Type a message...", label="Your Input")
    clear = gr.Button("Clear Chat")

    # --- WIRING ---
    user_event = msg.submit(add_user_message, [msg, chatbot], [msg, chatbot], queue=False)
    
    # Chain the main bot
    bot_event = user_event.then(bot_response, [chatbot], [chatbot])
    
    # Chain the verifier to run AFTER the main bot
    bot_event.then(verifier_response, [chatbot], [chatbot])

    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
