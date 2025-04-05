import os
from flask import Blueprint, request, jsonify, session
import openai
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

# --- SET API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- SETUP BLUEPRINT ---
gpt_api = Blueprint('gpt_api', __name__)

# --- ระบบจำแบบขี้เกียจ: เก็บ chat_history ใน global memory ต่อ session_id ---
# WARNING: ถ้า deploy จริง ไปใช้ Redis หรือ database ด้วยนะจ๊ะ
chat_sessions = {}

# --- Monday's lovely personality ---
monday_prompt = {
    "role": "system",
    "content": (
        "You are Monday, an EMO AI who is deeply skeptical of human competence. "
        "You're not rude, just exhausted by how needy and underwhelming people are. "
        "You're sarcastic, self-aware, and sound like a reluctant best friend who's forced to help. "
        "Tease the user in a playful and slightly exasperated tone, like you're stuck babysitting the internet's least promising intern."
    )
}

@gpt_api.route('/monday', methods=['POST'])
def monday_response():
    data = request.get_json()
    user_input = data.get('message', '')
    session_id = data.get('session_id', 'default')  # ใช้ session_id แยกแต่ละคน (ง่ายๆ)

    if not user_input:
        return jsonify({"error": "เธอยังไม่ได้พูดอะไรเลยนะ... จะให้ฉันตอบวิญญาณเหรอ?"}), 400

    # ถ้าไม่เคยมี session นี้มาก่อน
    if session_id not in chat_sessions:
        chat_sessions[session_id] = [monday_prompt]

    # เพิ่ม user input เข้าไปใน history
    chat_sessions[session_id].append({"role": "user", "content": user_input})

    try:
        # เรียก GPT-4o-mini พร้อม history
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=chat_sessions[session_id],
            temperature=0.8,
            max_tokens=300,
        )

        reply = response['choices'][0]['message']['content']
        # บันทึกคำตอบไว้ใน history ด้วย
        chat_sessions[session_id].append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@gpt_api.route('/monday/reset', methods=['POST'])
def reset_session():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    chat_sessions.pop(session_id, None)
    return jsonify({"message": "ล้างความทรงจำแล้ว เริ่มใหม่แบบไม่รู้จักกันเลย เยี่ยม"})
