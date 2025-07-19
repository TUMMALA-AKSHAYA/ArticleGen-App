from flask import Flask, render_template, request
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")
  
@app.route('/generate', methods=['GET', 'POST'])


def generate():
  if request.method == 'POST':  
    try:
      prompt_template = PromptTemplate.from_template("Generate a blog on title {title}")
      llm = OpenAI(temperature=0.3, openai_api_key=os.getenv('OPENAI_API_KEY'), model_name="gpt-3.5-turbo-instruct") 
      chain = LLMChain(llm=llm, prompt=prompt_template)
      user_prompt = request.json.get('prompt')
      output = chain.run(title=user_prompt)
      return output
    except Exception as e:
      if "quota" in str(e).lower():
        return "Sorry, the OpenAI API quota has been exceeded. Please add credits to your OpenAI account or wait for the quota to reset."
      else:
        return f"Error: {str(e)}"


app.run(host='0.0.0.0', port=81)
