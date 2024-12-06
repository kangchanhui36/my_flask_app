from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 설정

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])  # POST 메서드만 허용
def calculate():
    try:
        data = request.json
        hits = int(data["hits"])  # 안타 수
        at_bats = int(data["at_bats"])  # 타수
        walks = int(data.get("walks", 0))  # 볼넷 수
        hit_by_pitch = int(data.get("hit_by_pitch", 0))  # 몸에 맞는 공 수
        doubles = int(data.get("doubles", 0))  # 2루타 수
        triples = int(data.get("triples", 0))  # 3루타 수
        home_runs = int(data.get("home_runs", 0))  # 홈런 수

        if at_bats == 0:
            return jsonify({"error": "타수는 0일 수 없습니다."}), 400

        # 타율 계산
        batting_average = hits / at_bats
        # 출루율 계산
        obp = (hits + walks + hit_by_pitch) / (at_bats + walks + hit_by_pitch)
        # 장타율 계산
        total_bases = hits + doubles * 2 + triples * 3 + home_runs * 4
        slg = total_bases / at_bats

        return jsonify({
            "batting_average": round(batting_average, 3),
            "obp": round(obp, 3),
            "slg": round(slg, 3)
        })
    except ValueError:
        return jsonify({"error": "유효한 숫자를 입력해주세요."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
