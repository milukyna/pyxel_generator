import os
import os.path as osp

sample_jsons = []

with open(osp.join("tmp", "sample.py"), "r", encoding="utf-8") as fp:
    script1 = fp.read()

sample_jsons.append({"A.タイトル": "ネコが飛んでコーヒー豆を集めるゲーム",
    "B.コーヒーとの関連性": "ジャコウネコ(ムスクキャット)が貴重なコーヒー豆「コピルアク」を収集しつつ、障害物を避けながらゴールを目指すアクションゲームです。ゲーム内のアイテムやキャラクターはすべてコーヒー産業やコーヒー豆に関連した要素を用いています。",
    "C.python": script1,})

with open(osp.join("tmp", "sample2.py"), "r", encoding="utf-8") as fp:
    script2 = fp.read()

sample_jsons.append({"A.タイトル": "コーヒー豆を集めるゲーム",
    "B.コーヒーとの関連性": "ジャコウネコ(ムスクキャット)が貴重なコーヒー豆「コピルアク」を収集しつつ、障害物を避けながらゴールを目指すアクションゲームです。ゲーム内のアイテムやキャラクターはすべてコーヒー産業やコーヒー豆に関連した要素を用いています。",
    "C.python": script2,})

with open(osp.join("tmp", "sample3.py"), "r", encoding="utf-8") as fp:
    script3 = fp.read()

sample_jsons.append({"A.タイトル": "障害物を交わしながらコーヒー豆を拾え！",
    "B.コーヒーとの関連性": "ジャコウネコ(ムスクキャット)が貴重なコーヒー豆「コピルアク」を収集しつつ、障害物を避けるアクションゲームです。ゲーム内のアイテムやキャラクターはすべてコーヒー産業やコーヒー豆に関連した要素を用いています。",
    "C.python": script3,})
