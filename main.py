import requests
import json
from bs4 import BeautifulSoup

res = requests.get("https://digitalinnovation.one/blog") # acessando a página de blog da DIO
print(res) # caso consiga acessar o site acima, a requisição retornará o código 200
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find(class_ = "pagination").find_all('a') # pegando os links quando o site têm várias páginas; o find_all('a') vai buscar todos os links das tags 'a'
all_pages = [] # array para armazenar os links obtidos

for link in links:
  page = requests.get(link.get('href'))
  all_pages.append(BeautifulSoup(page.text, 'html.parser')) # acessa todas as páginas disponíveis blog
  # print(link.get('href')) # buscando e imprime os links que contém nos href's das tags 'a'

print(len(all_pages)) # imprime a quantidade de páginas acessadas
all_post = [] # array para armazenar os dados obtidos

# acessando todos os posts de todas as páginas encontradas anterioremente
for posts in all_pages:
  posts = soup.find_all(class_ = "post") # encontrando várias ocorrências da classe 'post'
  # acessando todos os posts de uma única página
  for post in posts:
    info = post.find(class_ = "post-content") # acessando as informações da classe 'post-content'
    title = info.h2.text # acessando a tag html h2, title
    preview = info.p.text # acessando a tag html p, texto
    author = info.find(class_ = "post-author").text # acessando o autor do post do blog da classe 'post-author'
    date = info.footer.find(class_ = 'post-date')['datetime'] #acessando a data do post do blog que está na tag footer dentro do 'datetime'
    # img = info.find(class_ = "wp-post-image")['src'] # buscando a imagem de dentro do 'src'
    
    # armazenando os dados no array all_post
    all_post.append({
      'title': title,
      'preview': preview,
      'author': author,
      'date': date,
      # 'img': img
    })

# salvando os dados do array all_post em um arquivo .json
with open('posts.json', 'w') as json_file:
  json.dump(all_post, json_file, indent = 2, ensure_ascii = False)


# --------------------------------------------------------------------------------------------------------------
# código retirado do Thiago Souza Link (@thiagosouzalink) para verificar como que funcionaria,
# visto que blog da DIO não está mais no ar, os arquivos questions.json e questions.txt referem-se a este código
# GitHub do projeto do Thiago https://github.com/thiagosouzalink/web-scraping-projeto-pratico

# import requests
# import json
# from bs4 import BeautifulSoup

# # Página para extração dos dados
# link = requests.get('https://digitalinnovation.one/faq')
# link.encoding = "utf-8"
# soup = BeautifulSoup(link.text, 'html.parser')
# div_cards = soup.find_all(class_="card")
# all_questions = []

# for card in div_cards:
#   # Recebe as perguntas e trata informações
#   question_card = card.find(class_="card-title")
#   question_temp = question_card.text.split()
#   question = ' '.join(question_temp)
  
#   # Recebe as respostas e trata informações
#   answer_card = card.find(class_="card-body")
#   answer_temp = answer_card.text.split()
#   answer = ' '.join(answer_temp)
  
#   all_questions.append({
#     'pergunta': question,
#     'resposta': answer
#   })

# # Gera arquivo .json contendo as perguntas
# with open('questions.json', 'w', encoding='utf-8') as json_file:
#   json.dump(all_questions, json_file, indent=2, ensure_ascii=False)

# # Gera arquivo .txt contendo as perguntas
# with open('questions.txt', 'w', encoding='utf-8') as question_file:
#   for index in all_questions:
#     question_file.write(f"{index['pergunta']}\n")
#     question_file.write(f"{index['resposta']}\n\n")