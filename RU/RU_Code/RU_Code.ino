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
const int LED = 11;

void setup() {
  Serial.begin(9600);

  pinMode(LED, OUTPUT);

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      pinMode(botoes[i][j], INPUT_PULLUP);
      estadoAnterior[i][j] = digitalRead(botoes[i][j]);
    }
  }
}

void loop() {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      bool estadoAtual = digitalRead(botoes[i][j]);

      //------ Se houve transição HIGH→LOW  (botão pressionado) ------
      if (estadoAnterior[i][j] == HIGH && estadoAtual == LOW) {
        votos[i][j]++;
        votosTotal++;
        enviarVotosSerial();
        som();
        delay(200);
      }
      estadoAnterior[i][j] = estadoAtual;
    }
  }
}

void som() {
  digitalWrite(LED, HIGH);
  delay(50);
  digitalWrite(LED, LOW);
}

// ----------- Envia todos os contadores via Serial em JSON -----------
void enviarVotosSerial() {
  for (int i = 0; i < 3; i++) {
    int totalPrato = votos[i][0] + votos[i][1] + votos[i][2];

    for (int j = 0; j < 3; j++) {
      double porcento = (totalPrato > 0) ? (votos[i][j] * 100.0) / totalPrato : 0.0;

      Serial.print(pratos[i]);
      Serial.print("_");
      Serial.print(avaliacoes[j]);
      Serial.print(", ");
      Serial.print(votos[i][j]);
      Serial.print(", ");
      Serial.print(porcento, 2);
      Serial.print("; ");
    }
  }

  // Linha final com total global
  Serial.print(" total: ");
  Serial.print(votosTotal);
}
