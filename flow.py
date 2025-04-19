import json
import os
import os.path as osp
import random
import uuid

from dotenv import load_dotenv
from fewshot_sample import sample_jsons
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

RESPONSE_FORMAT_TEXT = RESPONSE_FORMAT = {
    "type": "json_schema",  # json_schemaを設定
    "json_schema": {
        "name": "generate_pyxel_coffee_game",  # スキーマの名前を設定
        "strict": True,
        "schema": {  # schmaにてデータ型を設定
            "type": "object",  # データ型を指定。今回はオブジェクト型(辞書)
            "properties": {
                "A.タイトル": {
                    "type": "string",
                    "description": "作成するゲームのタイトルを記述する。例えば、コーヒー豆マリオなど。",
                },
                "B.注文内容との関連性": {
                    "type": "string",
                    "description": "作成するゲームがコーヒーに関連しているかどうかを記述する。例えば、ジャコウネコがコーヒー豆を食べるなど。",
                },
                "C.python": {
                    "type": "string",
                    "description": "最終的に生成されたコードをpython形式で記述する。",
                },
            },
            "required": ["A.タイトル", "B.注文内容との関連性", "C.python"],
            "additionalProperties": False,
        },
    },
}


client = OpenAI(api_key=OPENAI_API_KEY)

messages = [
    {
        "role": "system",
        "content": 'あなたは、コーヒー屋で即興の暇つぶしを提供することが求められています。そのため、ゲームを作成して提供することに決めました。注文されたコーヒーに関連したpyxelゲームを作成してください。注文内容との関連性や、ルールはあなたが考えてください。コーヒー豆を利用、ジャコウネコを利用、文字列のコーヒー/coffeeを利用、なんでもいいです。../assets/img/cat.png、../assets/img/bean.png、../assets/img/obstacle.pngの3つの画像を使用してください。cat.pngは16x16のサイズで、bean.pngとobstacle.pngはそれぞれ16x16のサイズである必要があります。これらの画像は、pyxel.image(0).load(0, 0, "assets/img/cat.png")のようにして読み込めます。ユーザーはcat.pngを操作し、bean.pngを取得することで正の報酬が、obstacle.pngを取得することで負の報酬が得られるというルールは統一してください。なお、だらだらしたミニゲームは好まないので、基本ヲワタ式あるいは3機程度の残機性でお願いします。さらに、ユーザーの取りうる入力はスペースキーだけです。また、pyxelには、captionはありません。代わりにtitleを使用してください。すべての変数を初期化するreset関数を定義し、ゲームオーバーからの復帰時には定義したreset関数を呼び出してください。また、それまでのあなたの出力と被らないものでお願いします。このプロジェクトの成功はあなたのクリエイティビティに掛かっています。基本的な出力は以下のようにしてください。\n\n\nA.タイトル:\n\nB.注文内容との関連性:\n\nC.python\n\n注文内容との関連性には作成するゲームの注文内容との関連性を記述してください。pythonには最終的に生成されたコードを記述してください。',
    },
]

candidates = [
    "コーヒー豆",
    "ドリップコーヒー",
    "カフェラテ",
    "エスプレッソ",
    "カフェオレ",
    "アメリカーノ",
    "カプチーノ",
    "アイスコーヒー",
    "コーヒーゼリー",
    "コーヒー牛乳",
]

for sample_json in sample_jsons:
    c = random.sample(candidates, 1)[0]
    messages.append(
        {
            "role": "user",
            "content": f"{c}を注文します。ちなんだゲームを作ってください。",
        }
    )
    messages.append({"role": "assistant", "content": str(sample_json)})

(
    {
        "role": "user",
        "content": "ドリップコーヒーを注文します。ちなんだゲームを作ってください。",
    },
)

response = client.chat.completions.create(
    model="gpt-4.1-mini-2025-04-14",
    messages=messages,
    max_completion_tokens=4096,
    n=1,
    stream=False,
    response_format=RESPONSE_FORMAT_TEXT,
)

print(response)

print(response.choices[0].message.content)

response_json = json.loads(response.choices[0].message.content)

_id = str(uuid.uuid4())

print(_id)

os.makedirs(_id, exist_ok=True)

with open(osp.join(_id, "output.json"), "w", encoding="utf-8") as f:
    json.dump(response_json, f, indent=4, ensure_ascii=False)

with open(osp.join(_id, "main.py"), "w", encoding="utf-8") as fp:
    fp.write(
        response_json[[k for k in response_json.keys() if k.endswith("python")][0]]
    )

import subprocess

subprocess.run(["pyxel", "package", _id, osp.join(_id, "main.py")])
# subprocess.run(["pyxel", "app2html", "proj_coffee.pyxapp"])

# <script src="https://cdn.jsdelivr.net/gh/kitao/pyxel/wasm/pyxel.js"></script>
