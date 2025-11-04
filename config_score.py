# config_score.py

PONTUACAO_ECOSCORE = {
    "TRANSPORTE": {
        "Fui de Carro Sozinho para o evento": -5,
        "Usei Transporte por App sozinho (ex: Uber/99)": -2,
        "Vim de carona compatilhada (com amigos/colegas ou por App)": +3,
        "Usei Transporte Público ou Transporte Gratuito fornecido pelo evento (Metrô/Ônibus)": +5,
        "Vim de Bicicleta ou a Pé": +10
    },
    "RESÍDUOS": {
        "Não separei meu lixo nas lixeiras corretas": -5,
        "Usei materiais descartáveis e sem reuso": -3,
        "Usei materiais compostáveis ou biodegradavéis (copos, pratos, etc.)": +3,
        "Separei o lixo corretamente (Reciclável/Orgânico)": +5,
        "Paguei pelo copo/garrafa reutilizável do evento": +10,
    },
    "ALIMENTAÇÃO": {
        "Desperdicei comida ou bebida": -5,
        "Optei por refeição com carne vermelha": -3,
        "Optei por refeição com carne branca": 0,
        "Comprei de vendedor que usa embalagens ecológicas": +3,
        "Evitei fast-food industrializado": +5,
        "Utilizei bebedouros automáticos fornecidos pelo evento": +6,
        "Optei por refeição vegetariana ou vegana": +5,
        "Evitei o desperdício de comida": +4
    },
    "ENGAJAMENTO E MATERIAIS": {
        "Ignorei campanhas educativas de sustentabilidade do evento": -3,
        "Peguei muitos brindes/materiais impressos desnecessários": 0,
        "Peguei brindes reutilizáveis como ecobags, kits de sementes ou produtos artesanais":+5,
        "Priorizei o uso de materiais digitais (App do evento, QR Code)": +7,
        "Carreguei o celular em totens de energia do evento": +4,
    }
}

CATEGORIAS = list(PONTUACAO_ECOSCORE.keys())