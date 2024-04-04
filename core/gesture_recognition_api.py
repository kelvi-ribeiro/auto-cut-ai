import cv2
import mediapipe as mp

# Inicializa o módulo MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Função para detectar o gesto de joinha no quadro atual
def detect_thumb_up(frame):
    # Converte a imagem para tons de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta as mãos na imagem em tons de cinza
    results = hands.process(gray)

    # Verifica se pelo menos uma mão foi detectada
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Verifica a posição do polegar (ID 4) e do indicador (ID 8)
            thumb_up = hand_landmarks.landmark[4].y < hand_landmarks.landmark[8].y

            if thumb_up:
                return True

    return False

# Abre o vídeo
cap = cv2.VideoCapture('Polegar_Pra_Cima.mp4')

# Lista para armazenar os segundos de início de cada gesto de joinha
thumbs_up_times = []

# Loop para processar cada quadro do vídeo
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Detecta o gesto de joinha no quadro atual
    if detect_thumb_up(frame):
        # Armazena o segundo de início do gesto de joinha
        thumbs_up_times.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)  # Converte para segundos

    # Exibe o quadro
    cv2.imshow('Video', frame)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()

# Imprime os segundos de início de cada gesto de joinha
print("Segundos de início de cada gesto de joinha:")
print(thumbs_up_times)
