from keras.models import load_model
import numpy as np


# 保存したモデルを読み込む
model = load_model('save_data/new_model.keras')

# 訓練時に使用した元素辞書
elements = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10,
            "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 10, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20,
            "Fe": 26, "Cu": 29, "Zn": 30, "I": 53}

# データ変換関数
def convert_element(data):
    for y, element_list in enumerate(data):
        for x, element in enumerate(element_list):
            if element in elements:
                data[y][x] = elements[element]
            else:
                print(f"Unknown element: {element}")
    return data

# データを数値に変換
def predict(hand):
    new_data = []
    new_data.append(hand)
    new_data = np.array(new_data)
    new_data = new_data.reshape(-1, new_data.shape[1])
    new_data = convert_element(new_data)
    new_data = new_data.astype(np.int32)

    # モデルで予測を実行
    predictions = model.predict(new_data)

    # 予測結果の表示
    if predictions[0] <= 0.5:
        return 'generate'
    return 'exchange'