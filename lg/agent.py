"""
Простой реактивный агент на LangGraph с DeepSeek LLM и инструментом-калькулятором.
Использует ключ API из переменной окружения DEEPSEEK_API_KEY.
"""

import os
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import operator


# Определение состояния агента
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Инструмент-калькулятор для 
@tool
def calculator(expression: str) -> str:
    """
    Выполняет математические вычисления.
    
    Args:
        expression: Математическое выражение для вычисления (например, "2 + 2", "10 * 5")
    
    Returns:
        Результат вычисления в виде строки
    """
    try:
        # Базовая валидация: разрешаем только цифры, операторы и пробелы
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Ошибка: выражение содержит недопустимые символы"
        
        result = eval(expression)
        return f"Результат: {result}"
    except Exception as e:
        return f"Ошибка вычисления: {str(e)}"


# Настройка LLM (DeepSeek)
def create_llm():
    """Создает и настраивает LLM с DeepSeek API."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY не установлен. "
            "Установите переменную окружения: export DEEPSEEK_API_KEY=your_key"
        )
    
    llm = ChatOpenAI(
        api_key=api_key,
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        temperature=0.7,
    )
    
    # Биндинг инструментов к LLM
    tools = [calculator]
    llm_with_tools = llm.bind_tools(tools)
    
    return llm_with_tools, tools


# Создание LLM и инструментов
llm, tools = create_llm()


# Узлы графа
def agent_node(state: AgentState) -> AgentState:
    """Узел агента: вызывает LLM с историей сообщений и инструментами."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def tool_node(state: AgentState) -> AgentState:
    """Узел инструмента: выполняет вызов инструмента и возвращает результат."""
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # Выполняем инструмент
        if tool_name == "calculator":
            result = calculator.invoke(tool_args)
        else:
            result = f"Неизвестный инструмент: {tool_name}"
        
        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )
    
    return {"messages": tool_messages}


def should_continue(state: AgentState) -> str:
    """Решает, нужно ли вызывать инструмент или завершить работу."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Если последнее сообщение содержит вызовы инструментов, переходим к инструменту
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    # Иначе завершаем работу
    return "end"


# Сборка графа
def create_agent_graph():
    """Создает и компилирует граф агента."""
    workflow = StateGraph(AgentState)
    
    # Добавляем узлы
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Добавляем рёбра
    workflow.add_edge(START, "agent")
    
    # Условное ветвление
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    
    # Возврат к агенту после выполнения инструмента
    workflow.add_edge("tools", "agent")
    
    # Компиляция графа
    app = workflow.compile()
    return app


# Создание графа
app = create_agent_graph()


# Пример использования
def run_agent():
    """Интерактивный запуск агента."""
    print("🤖 Агент готов к работе! Введите 'exit' для выхода.\n")
    
    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() in ["exit", "quit", "выход"]:
            print("До свидания!")
            break
        
        if not user_input.strip():
            continue
        
        try:
            # Создаем начальное состояние с сообщением пользователя
            initial_state = {"messages": [HumanMessage(content=user_input)]}
            
            # Запускаем агента
            result = app.invoke(initial_state)
            
            # Получаем последнее сообщение от агента
            last_message = result["messages"][-1]
            
            if isinstance(last_message, AIMessage):
                print(f"Агент: {last_message.content}\n")
            else:
                print(f"Агент: {last_message}\n")
                
        except Exception as e:
            print(f"Ошибка: {str(e)}\n")


if __name__ == "__main__":
    run_agent()
