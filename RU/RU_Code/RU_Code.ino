
// ----------- Declaração dos pinos dos 9 botões -----------
const int botoes[3][3] = {
  { 2, 3, 4 },  // carne vermelha:  ótimo, bom, ruim
  { 5, 6, 7 },  // carne branca:    ótimo, bom, ruim
  { 8, 9, 10 }  // vegetariano:     ótimo, bom, ruim
};

// ---------- Opções --------------
const char* pratos[3] = { "carne_vermelha", "carne_branca", "vegetariano" };
const char* avaliacoes[3] = { "otimo", "bom", "ruim" };

// ----------- Contadores de votos -----------
unsigned int votos[3][3] = { 0 };  // [prato][avaliação]
unsigned int votosTotal = 0;       // soma global

// ----------- Estados anteriores dos botões -----------
bool estadoAnterior[3][3] = { 0 };

// ----------- Difinir Saida do LED -----------------
const int SOM = 49;

void setup() {
  Serial.begin(9600);

  pinMode(SOM, OUTPUT);

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      pinMode(botoes[i][j], INPUT_PULLUP);
      estadoAnterior[i][j] = digitalRead(botoes[i][j]);
    }
  }
}

void loop() {
  int botoesPressionados = 0;
  int pratoSelecionado = -1;
  int avaliacaoSelecionada = -1;

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      bool estadoAtual = digitalRead(botoes[i][j]);

      //------ Se houve transição HIGH→LOW  (botão pressionado) ------
      if (estadoAnterior[i][j] == HIGH && estadoAtual == LOW) {
        botoesPressionados++;
        pratoSelecionado=i;
        avaliacaoSelecionada=j;
      }
      estadoAnterior[i][j] = estadoAtual;
    }
  }
    if (botoesPressionados == 1) {
    enviarVotosSerial(pratoSelecionado, avaliacaoSelecionada);
    som();
    delay(200);  // debounce
  }
}

void som() {
  digitalWrite(SOM, HIGH);
  delay(200);
  digitalWrite(SOM, LOW);
}

// ----------- Envia os dados via Serial -----------
void enviarVotosSerial(int prato, int avaliacao) {
  Serial.print(pratos[prato]);
  Serial.print("_");
  Serial.print(avaliacoes[avaliacao]);
}
