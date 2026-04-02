FROM python:3.8-slim-buster
LABEL version="0.1.1" maintainer="Nando Lopes <lopes.fernando@hotmail.com>"

# 1. Define o diretório de trabalho (mais padrão e limpo)
WORKDIR /app

# 2. Instala as dependências primeiro para ganhar velocidade no deploy
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia todo o resto do projeto (incluindo o ypo.py e as pastas de temas)
COPY . .

# 4. O comando de execução sem o conflito de ENTRYPOINT
CMD ["streamlit", "run", "ypo.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
