from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime
from auth import cadastro_usuario, login_usuario
from storage import carregar_registros, salvar_registros
from config_score import PONTUACAO_ECOSCORE, CATEGORIAS
from desempenho import get_dados_desempenho, get_dica_personalizada, get_dados_analise_geral

app = Flask(__name__)
app.jinja_env.globals['enumerate'] = enumerate

app.secret_key = 'uma-chave-secreta-muito-segura-e-dificil-de-adivinhar' 

@app.route('/')
def index():
    """Página inicial: redireciona para o login ou para o menu principal."""
    if 'usuario' in session:
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        
        usuario = login_usuario(nome, senha)
        if usuario:
            session['usuario'] = usuario 
            flash(f'Bem-vindo(a) de volta, {usuario}!', 'success')
            return redirect(url_for('menu'))
        else:
            
            flash('Usuário ou senha inválidos.', 'danger')
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        
        if cadastro_usuario(nome, senha):
            flash('Usuário cadastrado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Nome de usuário já existe. Tente outro.', 'warning')

    return render_template('cadastro.html')

@app.route('/menu')
def menu():
    if 'usuario' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('menu.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None) 
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    data_hoje = datetime.date.today().strftime("%Y-%m-%d")
    

    todos_registros = carregar_registros()
    registros_usuario = [r for r in todos_registros if r.get('nome_usuario') == usuario]
    ja_registrou = any(r.get('data') == data_hoje for r in registros_usuario)

    if request.method == 'POST':
        if ja_registrou:
            flash('Você já registrou seus hábitos hoje.', 'warning')
            return redirect(url_for('menu'))

        respostas_diarias = {}
        pontuacao_total = 0

        
        mapa_chaves = {
            "TRANSPORTE": "transporte",
            "RESÍDUOS": "residuos",
            "ALIMENTAÇÃO": "alimentacao",
            "ENGAJAMENTO E MATERIAIS": "engajamento"
        }

        for categoria_original in CATEGORIAS:
            chave_form = categoria_original.lower()
            chave_csv = mapa_chaves[categoria_original]

            opcoes_selecionadas = request.form.getlist(chave_form)
            
            if opcoes_selecionadas:
                respostas_diarias[chave_csv] = ";".join(opcoes_selecionadas)
                for opcao in opcoes_selecionadas:
                    pontuacao_total += PONTUACAO_ECOSCORE[categoria_original].get(opcao, 0)

        
        novo_registro = {
            "nome_usuario": usuario,
            "data": data_hoje,
            "pontuacao": pontuacao_total,
            **respostas_diarias
        }
        todos_registros.append(novo_registro)
        salvar_registros(todos_registros)

        flash(f'🎉 Registro salvo! Sua pontuação de hoje foi: {pontuacao_total:+d} pontos.', 'success')
        return redirect(url_for('menu'))

    
    return render_template('registro.html', categorias=PONTUACAO_ECOSCORE, ja_registrou=ja_registrou)

@app.route('/desempenho')
def desempenho():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    dados = get_dados_desempenho(usuario)

    
    return render_template('desempenho.html', dados=dados)



@app.route('/dicas')
def dicas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    dica = get_dica_personalizada(usuario)
    
    return render_template('dicas.html', dica=dica)


@app.route('/analise_geral')
def analise_geral():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    dados = get_dados_analise_geral()
    return render_template('analise_geral.html', dados=dados)


if __name__ == '__main__':
    
    app.run()
