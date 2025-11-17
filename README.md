# 🎃 Pumpkin Crawler

#### Jogo desenvolvido como Trabalho Final da disciplina Computação 2
###### Universidade Federal do Rio de Janeiro (UFRJ)

![6c0bb147f81e374](https://github.com/user-attachments/assets/6705b74a-ef1b-49b1-b777-51039bd86f14)
###### Créditos: Arte autoral

##

### Sobre o Jogo
Pumpkin Crawler é um RPG top-down do gênero Dungeon Crawler, ambientado em uma masmorra única inspirada na temática de Halloween. O jogador controla uma bruxinha que deve explorar o cenário, enfrentar um boss, coletar itens e desbloquear áreas até finalmente abrir o baú final e concluir a aventura.

Todo o desenvolvimento utiliza exclusivamente os conteúdos ensinados na disciplina Computação 2, sem bibliotecas externas além das permitidas.

##

### Gameplay

#### Objetivo geral
Explorar a masmorra, interagir com objetos, derrotar o boss, coletar chaves e abrir o baú final.


<img width="500" height="300" alt="1" src="https://github.com/user-attachments/assets/73ea7840-7c0c-468f-b324-7dec1a8f67c6" />
<img width="500" height="270" alt="2" src="https://github.com/user-attachments/assets/d1da5749-a6a7-47a8-a85d-f45ea1b2857c" />
<img width="500" height="300" alt="3" src="https://github.com/user-attachments/assets/3c69df97-ad5d-43bf-9eb9-732d716259dd" />
<img width="500" height="300" alt="4" src="https://github.com/user-attachments/assets/436d1906-bcbd-405d-b871-b89189bd4e82" />



#### Mecânicas principais
- **Movimentação:** \
  clique com o botão esquerdo do mouse no local desejado. ![idle_down](https://github.com/user-attachments/assets/ebb77a79-8b44-4972-a658-06a590d1385e)  ![run_down](https://github.com/user-attachments/assets/0d0ece3d-cf6c-4673-89c9-0de0a77e5b02)
- **Ataques:** \
  clique com o botão direito na direção do alvo. ![attack_down](https://github.com/user-attachments/assets/183b88dd-6ef4-441b-9d49-b3d602d308ea)

- **Interações:** \
  tecla E para:
  - puxar alavanca
  - destrancar fechadura
  - coletar itens
- **Usar poção de cura:** \
  tecla 1 (restaura todo o HP da personagem). <img width="32" height="32" alt="healing_potion" src="https://github.com/user-attachments/assets/844a4723-1bed-4912-b590-2cc3a7f34304" />



##

### Elementos Interativos

- **Alavancas:** abrem ou fecham portões. 
- **Fechaduras:** podem ser destrancadas com chaves específicas.
- **Porta e portão:** bloqueiam o caminho até serem abertos.
- **Caixotes:** podem ser destruídos com ataques.
- **Poção de cura:** dropada pelo caixote quebrado.
- **Chaves:**
  - *Mimic Key* — dropada ao derrotar o Mimic ![mimic_key](https://github.com/user-attachments/assets/6d021790-a686-4590-8324-d8a700739afc)
  - *Boss Key* — dropada ao derrotar o Boss ![boss_key](https://github.com/user-attachments/assets/df93ba76-02a7-4aaf-9205-3c2456f14b7a)

  - usadas para liberar a sala do tesouro e abrir o baú final, respectivamente. ![final_chest](https://github.com/user-attachments/assets/ad672fcb-cbd9-4171-a92a-3e4e25913e90)

 
##

### Inimigos

#### Mimic Chest
Um baú mímico não agressivo que se movimenta aleatoriamente quando ativado.
Ao ser derrotado, dropa uma chave necessária para desbloquear uma área do jogo.
![move_down](https://github.com/user-attachments/assets/174ae0f8-2b01-4336-be3f-3d72d5eafeab)

#### Boss
Um inimigo agressivo que persegue a personagem quando sua sala é revelada.
Possui animações de:
- movimento \
![boss_move_down](https://github.com/user-attachments/assets/7e23ed61-383d-420e-ad50-68d027a00326)
- ataque \
![boss_attack_down](https://github.com/user-attachments/assets/46c77776-de8c-4c5c-a784-6fd3719831f0)
- dano \
![boss_damage_down](https://github.com/user-attachments/assets/fc039cc3-6baa-46d7-bd2a-77c9d52e2094)
- morte \
![boss_death](https://github.com/user-attachments/assets/7f011e01-094a-4670-a3f4-7c0706df16b5) \
Ao derrotá-lo, o jogador recebe a chave do baú final.

##

### Mapa e Estrutura
O mapa é construído por meio de:
- uma matriz de tiles (0 = parede, 1 = movimentação permitida),
- tilesets carregados dinamicamente com PIL,
- uma área secreta (Boss Room) inicialmente oculta, sendo revelada apenas após a interação com a alavanca correspondente.

##

### Conteúdos de Computação 2 aplicados
O jogo foi desenvolvido utilizando exclusivamente alguns dos conceitos abordados na disciplina:

- [x] Definição de classes
- Organização do código em módulos orientados a objetos: \
`Player`, `Boss`, `MimicChest`, `Game`, além de estruturas auxiliares.

- [x] Dicionários e conjuntos
- Mapeamento de tiles e elementos interativos (`tileset`, `interactions`).
- Tabelas de animação, mapeamento de direções, rastreamento de itens no canvas.

- [x] Tratamento de exceções
- Erros ao carregar imagens
- Falhas ao validar movimentação
- Ações inesperadas durante animações
- Proteção contra estados inconsistentes

- [x] Biblioteca NumPy
- Cálculo de vetores de direção
- Normalização de movimento (Boss e Player)
- Distâncias e aproximações angulares

- [x] Construção de interfaces gráficas com Tkinter
- Criação da janela do jogo
- Canvas para renderização
- Eventos de mouse e teclado
- Sistema de animação usando `after()`
- Renderização de imagens com `PhotoImage` e `ImageTk`

##

### Estrutura do Projeto

    📂──Pumpkin_Crawler/
        |
        ├──📂  assets/
        |  |
        |  |
        |  ├──📂 boss/
        |  |   ├──📁 attack
        |  |   ├──📁 damage
        |  |   ├──📁 death
        |  |   └──📁 move
        |  |
        |  ├──📁 final_chest
        |  |
        |  ├──📁 interactive
        |  |
        |  ├──📁 keys
        |  |        
        |  ├──📁 menu
        |  |        
        |  ├──📂 mob_mimic_chest/
        |  |   ├──📁 damage
        |  |   └──📁 move
        |  |        
        |  ├──📂 player/
        |  |   ├──📁 attack
        |  |   ├──📁 death
        |  |   ├──📁 idle
        |  |   ├──📁 itens
        |  |   └──📁 run
        |  |
        |  └── 📁tileset     
        |  
        ├──📄 README.md
        ├──📄 enemies.py
        ├──📄 main.py
        ├──📄 map.py
        └──📄 player.py

##

### Como Executar

1. Certifique-se de ter Python instalado
  `python3 --version`
2. Clone o repositório
```
git clone https://github.com/Sara-Giannini/Pumpkin_Crawler.git
cd Pumpkin_Crawler
```
3. Crie um ambiente virtual. \
   Opcional, mas recomendado `python3 -m venv venv` 

Ative o ambiente:
  - Linux/macOS
`source venv/bin/activate`
  - Windows
`venv\Scripts\activate`
4. Instale as dependências necessárias \
O jogo usa apenas duas bibliotecas externas:
- Pillow → para carregar imagens e GIFs
- NumPy → para cálculos de vetores e direções \
Instale ambas com:
`pip install pillow numpy`
5. Execute o jogo \
Dentro do diretório principal: \
`python3 main.py` \
A janela do menu irá abrir com a animação de background. \
A partir daí, você pode: 
  - Start para iniciar o jogo
  - Quit para sair

#### Requisitos mínimos
- Python 3.8 ou superior
- Tkinter
  - vem embutido no Python em Windows e macOS. Em Linux pode precisar instalar
- No Linux, caso Tkinter não esteja instalado:

Distribuição | Comando
-- | --
Debian/Ubuntu e derivados	| `sudo apt-get install python3-tk`
Fedora/RHEL e derivados	| `sudo dnf install python3-tkinter`
Arch e derivados | `sudo pacman -S tk`

