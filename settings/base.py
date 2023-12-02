import os

from dotenv import load_dotenv, dotenv_values


env_maping_dict = {"development": "dev", "staging": "stage", "production": "prod"}
env = os.getenv('ENVIRONMENT', 'development')
dotenv_path = f".env.{env_maping_dict.get(env)}"

if not load_dotenv(dotenv_path=dotenv_path):
    raise EnvironmentError(
        "Please add .env.dev or .env.stage or .env.prod file in project directory get reference from .env-EXAMPLE file"
    )

ENV_VARIABLES = dict(dotenv_values(dotenv_path=dotenv_path))

django_project_name = ENV_VARIABLES.get("DJANGO_PROJECT_NAME", "CASTFORM")
print(" "*50 + "\n" + "*"*50 + "\n" + f"Using {django_project_name}_ENV: " + (str(env).upper()) + "\n" + "*"*50 + "\n" + " "*50)
