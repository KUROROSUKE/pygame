import numpy as np
from keras.models import load_model
import action_use

# モデルの読み込み
models = []
for i in range(8):
    model_path = f'save_data/card_model_{i+1}.keras'
    model = load_model(model_path)
    models.append(model)
elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Fe', 'Cu', 'Zn', 'I']


# 新しい手札のデータ
def predict(new_hand):
    new_action = action_use.predict(new_hand)

    # 手札のエンコーディング
    element_index = {element: i for i, element in enumerate(elements)}
    encoded_hand = [element_index[elem] if elem in element_index else 0 for elem in new_hand]
    action = 0 if new_action == 'generate' else 1


    # モデルへの入力をバッチとして準備
    input_data = np.array([encoded_hand + [action]])

    # 全てのモデルに対して予測を一度に行う
    predictions = np.concatenate([model.predict(input_data, batch_size=8) for model in models], axis=1)

    # 選択されたカードを抽出
    selected_cards = [new_hand[i] for i, pred in enumerate(predictions[0]) if pred > 0.5]

    return new_action, selected_cards