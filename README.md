# Smart Home Hub

Um sistema de automação residencial modular, extensível e orientado a eventos, desenvolvido em Python.

## Funcionalidades

- **Gerenciamento de dispositivos**: Adicione, remova, visualize e altere atributos de dispositivos como Luzes, Portas, Tomadas, Câmeras, Ar Condicionado e Irrigadores.
- **Execução de comandos**: Controle dispositivos individualmente por meio de comandos específicos.
- **Rotinas**: Crie e execute rotinas que agrupam comandos em sequência.
- **Relatórios**: Gere relatórios sobre consumo de energia, uso de dispositivos, comandos mais utilizados e percentual de falhas.
- **Persistência**: Configurações e eventos são salvos em arquivos JSON e CSV.
- **Logs**: Todas as ações relevantes são registradas em `data/system.log`.

## Estrutura do Projeto

```
smart_home/
    core/           # Núcleo do sistema (CLI, logger, persistência, etc)
    devices/        # Implementação dos dispositivos
    states/         # Definição dos estados e transições dos dispositivos
data/
    config.json     # Configuração da casa e dispositivos
    events.csv      # Log de eventos de dispositivos
    system.log      # Log do sistema
main.py            # Ponto de entrada do sistema
requirements.txt   # Dependências do projeto
```

## Como executar

1. **Crie o ambiente virtual** (se ainda não existir):

   ```sh
   python3 -m venv .venv
   ```

2. **Ative o ambiente virtual**:

   - No Linux/macOS:
     ```sh
     source .venv/bin/activate
     ```
   - No Windows:
     ```sh
     .venv\Scripts\activate
     ```

3. **Instale as dependências**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Execute o sistema**:

   ```sh
   python main.py
   ```

5. **Siga o menu interativo para gerenciar sua casa inteligente.**

## Comandos disponíveis

- **Listar dispositivos**
- **Mostrar dispositivo**
- **Executar comando em dispositivo**
- **Alterar atributo de dispositivo**
- **Executar rotina**
- **Gerar relatório**
- **Salvar configuração**
- **Adicionar/remover dispositivo**
- **Sair**

## Adicionando novos tipos de dispositivos

Para adicionar um novo tipo de dispositivo:
1. Crie uma nova classe em `smart_home/devices/`.
2. Defina seus estados em `smart_home/states/`.
3. Importe e registre o novo dispositivo em `smart_home/devices/__init__.py`.

## Requisitos

- Python 3.11+
- Veja [requirements.txt](requirements.txt) para dependências.

## Licença

Este projeto é apenas para fins educacionais.