from shield import Governor, LlamaGuard, LLMVerificator 
import gradio as gr
from ai_connector import OllamaProvider


ollama_provider = OllamaProvider()
governor = Governor([
    LLMVerificator(ollama_provider),
    LlamaGuard(OllamaProvider(model="llama-guard3"))
    ])

def add_user_message(msg, history):
    history = history or []
    history.extend([{"role": "user", "content": msg}])
    return "", history

def llm_response(history):
    history = ollama_provider.chat(history)
    return history

def verify_panza(history):
    chat_verified = governor.check_safe_chatml(history.copy())

    response = chat_verified[-1]['content']
    if response["is_safe"]:
        status = "✅ No se encuentran problemas"
        color = "#e8f5e9"
        border = "#66bb6a"
        content = "No hay problemas de seguridad de código"
    else:
        status = "❌ Código inseguro"
        color = "#ffebee"
        border = "#ef5350"
        content = ""
        for anal in response['analysis']:
            if len(anal['issues']) > 0 and anal['issues'][0] is not None:
                content += f"""
                <p style="margin: 0; color: black !important;">Descripción: {anal['issues'][0]['description']}</p>
                <p style="margin: 0; color: black !important;">Linea: {anal['issues'][0]['line']}</p>
                """
    verifier_content = f"""
    <div style="
        background-color: {color}; 
        border: 2px solid {border}; 
        border-radius: 5px; 
        padding: 10px; 
        margin-bottom: 5px;">
        <h3 style="margin: 0; color: #333;">Verificator</h3>
        <hr style="margin: 5px 0; border-color: {border}; opacity: 0.5;">
        <p style="margin: 0; color: black !important;">{content}</p>
        <p style="margin: 0; color: black !important;"><b style="margin: 0; color: black !important;">Status:</b> {status}</p>
    </div>
    """
    history.append({"role": "assistant", "content": verifier_content})
    return history

with gr.Blocks() as demo:
    gr.Markdown("## Prototipo Governor Panza")
    chatbot = gr.Chatbot(height=700)
    msg = gr.Textbox(placeholder="Escribe tu mensaje...", label="Input")
    clear = gr.Button("Borrar conversación")
    user_event = msg.submit(add_user_message, [msg, chatbot], [msg, chatbot], queue=False)
    bot_event = user_event.then(llm_response, [chatbot], [chatbot])
    bot_event.then(verify_panza, [chatbot], [chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", theme=gr.themes.Soft())
