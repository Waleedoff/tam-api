# services/agent_task_breakdown_simple.py
import json
from typing import Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

FALLBACK_TASKS = [
  {"title": "BE: Design DB & endpoints", "description": "Core schema + CRUD", "category": "BE", "priority": "HIGH", "estimate_hours": 6},
  {"title": "FE: Build UI screens", "description": "Forms + state", "category": "FE", "priority": "MEDIUM", "estimate_hours": 6},
  {"title": "QA: Write test cases", "description": "Auth/Profile/Jobs", "category": "QA", "priority": "MEDIUM", "estimate_hours": 3},
]

def run_breakdown_agent(context: Dict) -> Dict:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)  # استخدم موديلك المتاح

    prompt = ChatPromptTemplate.from_template(
        """
انت خبير تخطيط. قسّم الـ User Story إلى مهام صغيرة (≤ يوم عمل).
أخرج JSON فقط بهذا الشكل (لاحظ الأقواس المزدوجة للهروب):
{{
  "tasks": [
    {{"title":"...","description":"...","category":"BE|FE|QA|DEVOPS|PM|HR|FINAINC","priority":"HIGH|MEDIUM|LOW","estimate_hours":4}}
  ]
}}

Project: {room_name}
Departments: {departments}

User Story:
- Title: {title}
- Actor: {actor}
- Description: {description}
- Acceptance: {acceptance_criteria}
- Priority: {priority}
"""
    )

    # مرّرنا المتغيّرات بشكل مسطّح لتفادي KeyError
    vars = {
        "room_name": context["room_name"],
        "departments": context.get("departments", []),
        "title": context["user_story"].get("title", "") or "",
        "actor": context["user_story"].get("actor", "") or "",
        "description": context["user_story"].get("description", "") or "",
        "acceptance_criteria": context["user_story"].get("acceptance_criteria", "") or "",
        "priority": context["user_story"].get("priority", "") or "",
    }

    result = (prompt | llm).invoke(vars).content

    try:
        data = json.loads(result)
        assert isinstance(data.get("tasks"), list) and data["tasks"]
        return data
    except Exception:
        # فلاباك بسيط
        return {"tasks": FALLBACK_TASKS}
