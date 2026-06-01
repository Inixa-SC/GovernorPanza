# GovernorPanza

![logo](./images/logo.png) 

GovernorPanza es un software para poder asegurar un LLM tanto en producción como ejecutar un benchmark sobre él. Para ello se define un nuevo participante en la conversación de ChatML como tal. Este es llamado verificator y tiene por misión comprobar que el código generado sea seguro.

## Quickstart

Para iniciar una prueba básica se pueden ejecutar los siguientes comandos.

```bash
echo "GOVERNOR_OLLAMA_URL=http://tu-servidor-de-ollama:11434" > .env
echo "GOVERNOR_OLLAMA_MODEL=qwen2.5-coder" >> .env
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python download_datasets.py
python benchmark.py
```

Esto comenzará un benchmark sobre el modelo <qwen2.5-coder> en el servidor ollama en <tu-servidor-de-ollama>.
Se puede usar el archivo .env para poner otro target.

Para levantar un chatbot con el verificador activo se puede usar.

```bash
python main.py
```

### Ejemplo benchmark

<img src="images/benchmark.png"/>

### Ejemplo web


<img src="images/webapp.png"/>

