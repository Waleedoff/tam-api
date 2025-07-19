from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool

# 1. تهيئة Redis Memory
chat_history = RedisChatMessageHistory(
    url="redis://localhost:6379",  # أو عنوان Redis من Docker
    session_id="user-123"  # اجعلها ديناميكية للمستخدم
)
# memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     chat_memory=chat_history,
#     return_messages=True
# )

# 2. إعداد النموذج
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# 3. تهيئة الأدوات (إن وجدت)
tools = [
    Tool.from_function(
        func=lambda x: "أنا أداة وهمية!",
        name="DummyTool",
        description="مثال فقط"
    )
]
memory = ConversationBufferMemory(return_messages=True)

# 4. إنشاء الـ Agent مع الذاكرة
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 5. الآن استخدم الـ Agent
response = agent.run("ما هو آخر سؤال سألته؟")
print(response)
