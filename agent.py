import dspy
import sqlite3
from dotenv import load_dotenv

from tools import execute_sql, get_schema, save_data_to_csv


# --- DSPy Agent Definition ---
class SQLAgentSignature(dspy.Signature):
    """
    Este agente sirve para poder responder preguntas en lenguaje natural sobre
    una base de datos SQL que trata acerca de ventas, empleados y sucursales.
    Las herramientas que utiliza son:
    1. execute_sql: ejecuta una consulta SQL en la base de datos y devuelve los resultados.
    2. get_schema: obtiene el esquema de una tabla específica en la base de datos.
    3. save_data_to_csv: guarda las respuestas que se dan al usuario en un archivo CSV.
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
        desc="Esta herramienta guarda las respuestas que se dan al usuario en un archivo CSV. La entrada es la respuesta en lenguaje natural y la salida es la confirmación de que los datos se han guardado.",
        func=save_data_to_csv
    )

    all_tools = [execute_sql_tool, get_schema_tool, save_csv_tool]

    # 2. Instantiate and run the agent
    agent = SQLAgent(tools=all_tools)

    return agent
