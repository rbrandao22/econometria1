# Repositório de apoio para alunos do curso MD/econometria1

Passo-a-passo inicial:
- Crie uma vm na google cloud
- Copie o arquivo vmcfg.sh para a vm na cloud:
   gcloud scp vmcfg.sh <nome-da-vm>:~/
- Entre na vm:
   gcloud compute ssh <nome-da-vm>
- Rode o script de configuração inicial da vm:
   sh vmcfg.sh
- Adicione o grupo 'docker' ao seu usuário linux (para facilitar depois):
   sudo usermod -aG docker <seu-nome-de-usuário> (seu nome aparece no prompt)
- Saia e entre na vm (precisa renovar o terminal p/ habilitar o grupo docker):
   exit
   gcloud compute ssh <nome-da-vm>
- Clone o repositório econometria1:
   git clone https://github.com/rbrandao22/econometria1.git
- Crie a imagem de container 'my-python-app':
   cd econometria1/ops
   sh build.sh
- Dispare um container com Python e pacotes (no requirements) instalado:
   cd ~/econometria1
   sh run_python3.sh
   
   