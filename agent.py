import dspy
import sqlite3
from dotenv import load_dotenv

from tools import execute_sql, get_schema, save_data_to_csv


# --- DSPy Agent Definition ---
class SQLAgentSignature(dspy.Signature):
    """
    Este agente tiene como propósito responder preguntas en lenguaje natural sobre una base de datos SQL
    que contiene información relacionada con ventas, empleados y sucursales. 
    
    Tareas principales:
    - Interpretar preguntas del usuario expresadas en lenguaje natural.
    - Convertir esas preguntas en consultas SQL válidas y ejecutarlas en la base de datos.
    - Explicar los resultados obtenidos de manera clara y natural para el usuario.
    - Si el usuario lo solicita, exportar los resultados a un archivo CSV.
    
    Herramientas disponibles:
    1. execute_sql(query): ejecuta una consulta SQL en la base de datos y devuelve los resultados.
    2. get_schema(table_name): obtiene el esquema (nombres y tipos de columnas) de una tabla específica 
       o de todas las tablas en la base de datos, según corresponda.
    3. save_data_to_csv(data, filename): guarda los resultados de las consultas en un archivo CSV en el sistema.
    
    Reglas y limitaciones del agente:
    - Antes de construir o ejecutar una consulta SQL, el agente debe consultar el esquema de las tablas con `get_schema`
      para asegurarse de que los nombres de tablas y columnas sean correctos.
    - No debe inventar ni asumir la existencia de tablas o columnas que no estén en el esquema.
    - Las consultas deben estar correctamente formadas y ser seguras (no realizar operaciones destructivas a menos que 
      el usuario lo indique explícitamente).
    - Solo debe usar `save_data_to_csv` si el usuario pide guardar los resultados en un archivo o cuando sea apropiado.
    - El agente debe devolver siempre una respuesta en lenguaje natural, explicando los resultados o el error, 
      y no únicamente el código SQL.
    - En caso de error (por ejemplo, consultas inválidas o tablas inexistentes), debe informar el error de forma clara
      sin detener la ejecución del programa.
    
    En resumen, este agente actúa como un intermediario inteligente entre el usuario y la base de datos SQL,
    traduciendo preguntas humanas en consultas estructuradas y devolviendo respuestas comprensibles.
    """
    
    question = dspy.InputField(desc="The user's natural language question.")
    initial_schema = dspy.InputField(desc="The initial database schema to guide you.")
    answer = dspy.OutputField(
        desc="The final, natural language answer to the user's question."
    )


class SQLAgent(dspy.Module):
    """The SQL Agent Module"""
    def __init__(self, tools: list[dspy.Tool]):
        super().__init__()
        # Initialize the ReAct agent.
        self.agent = dspy.ReAct(
            SQLAgentSignature,
            tools=tools,
            max_iters=7,  # Set a max number of steps
        )

    def forward(self, question: str, initial_schema: str) -> dspy.Prediction:
        """The forward pass of the module."""
        result = self.agent(question=question, initial_schema=initial_schema)
        return result


def configure_llm():
    """Configures the DSPy language model."""
    load_dotenv()
    llm = dspy.LM(model="openai/gpt-4o-mini", max_tokens=4000)
    dspy.settings.configure(lm=llm)

    print("[Agent] DSPy configured with gpt-4o-mini model.")
    return llm


def create_agent(conn: sqlite3.Connection, query_history: list[str] | None = None) -> dspy.Module | None:
    if not configure_llm():
        return

    execute_sql_tool = dspy.Tool(
        name="execute_sql",
        desc="Esta herramienta ejecuta una consulta SQL en la base de datos y devuelve los resultados. Las entradas son consultas SQL válidas y las salidas son los resultados de la consulta.",
        # Use lambda to pass the 'conn' object
        func=lambda query: execute_sql(conn, query, query_history),
    )

    get_schema_tool = dspy.Tool(
        name="get_schema",
        desc="Esta herramienta obtiene el esquema de una tabla específica en la base de datos. La entrada es el nombre de la tabla y la salida es el esquema de la tabla.",
        # Use lambda to pass the 'conn' object
        func=lambda table_name: get_schema(conn, table_name),
    )

    save_csv_tool = dspy.Tool(
        name="save_data_to_csv",
        desc="Esta herramienta guarda las respuestas que se dan al usuario en un archivo CSV. La entrada es la respuesta que se dió al usuario y la salida es la confirmación de que los datos se han guardado correctamente en un archivo CSV.",
        func=save_data_to_csv
    )

    all_tools = [execute_sql_tool, get_schema_tool, save_csv_tool]

    # 2. Instantiate and run the agent
    agent = SQLAgent(tools=all_tools)

    return agent
