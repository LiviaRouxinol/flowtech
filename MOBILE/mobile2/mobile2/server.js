const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Rota inicial
app.get('/', (req, res) => {
  res.send('API do StockPro2 / FlowTech está rodando com sucesso!');
});

// Configuração da Conexão com o MySQL
const db = mysql.createPool({
  host: 'localhost',
  user: 'root',      // Altere para seu usuário do MySQL
  password: '123456',      // Altere para sua senha do MySQL
  database: 'flowtech',
  waitForConnections: true,
  connectionLimit: 10,
});




// 1. Rota de Login
app.post('/login', async (req, res) => {
  const { e_mail, senha } = req.body;

  try {
    // 2. No MySQL, usamos [linhas] para extrair apenas os registros da tabela
    const [linhas] = await db.query('SELECT * FROM funcionario WHERE e_mail = ?', [e_mail]);

    // 3. Se não encontrar nenhum funcionário com esse e-mail
    if (!linhas || linhas.length === 0) {
      return res.status(401).json({
        success: false,
        message: 'Funcionário não cadastrado ou dados incorretos!'
      });
    }

    // Pega os dados do primeiro funcionário que retornou do MySQL
    const dadosFuncionario = linhas[0];

    // Proteção para garantir que valores nulos ou indefinidos não quebrem o sistema
    const senhaBancoLimpa = dadosFuncionario?.senha ? String(dadosFuncionario.senha).trim() : '';
    const senhaDigitadaLimpa = senha ? String(senha).trim() : '';

    // 4. Faz a comparação das senhas limpas
    if (senhaBancoLimpa !== senhaDigitadaLimpa) {
      return res.status(401).json({
        success: false,
        message: 'Senha incorreta!'
      });
    }

    // 5. Se o e-mail e a senha estiverem certos, libera o login!
    return res.status(200).json({
      success: true,
      message: 'Login realizado com sucesso!',
      funcionarioId: dadosFuncionario.id
    });

  } catch (error) {
    console.error("ERRO COMPLETO NO MYSQL:", error);
    return res.status(500).json({
      success: false,
      message: `Erro interno no servidor: ${error.message}`
    });
  }
});






// 2. Rota de Dashboard (Resumo)
app.get('/api/dashboard', async (req, res) => {
  try {
    // 1. Conta o total de itens cadastrados na tabela 'produto'
    const [[{ totalProducts }]] = await db.query('SELECT COUNT(*) as totalProducts FROM produto');

    // 2. Compara a quantidade atual com o 'estoque_minimo' definido
    const [[{ lowStockCount }]] = await db.query('SELECT COUNT(*) as lowStockCount FROM produto WHERE quantidade <= estoque_minimo');

    // 3. Busca o histórico de movimentações relacionando com a chave 'produto_id'
    const [recentActivities] = await db.query(
      'SELECT h.id, h.type, h.quantity, p.nome as product ' +
      'FROM history h ' +
      'JOIN produto p ON h.product_id = p.produto_id ' +
      'ORDER BY h.id DESC LIMIT 5'
    );

    res.json({
      totalProducts: totalProducts || 0,
      lowStockCount: lowStockCount || 0,
      recentActivities,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 3. Listar Produtos
app.get('/api/products', async (req, res) => {
  try {
    // Atualizado para buscar da tabela 'produto' ordenando por 'nome'
    const [products] = await db.query('SELECT * FROM produto ORDER BY nome ASC');
    res.json(products);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 4. Buscar Produto Específico por ID ou RFID (Substituído 'code' por 'RFID')
app.get('/produtos/:id', async (req, res) => {
  const { id } = req.params;
  
  try {
    // Busca na tabela 'produto' usando a desestruturação do MySQL [linhas]
    const [linhas] = await db.query('SELECT * FROM produto WHERE produto_id = ?', [id]);
    
    // Se a busca não retornar nada, avisa o app
    if (!linhas || linhas.length === 0) {
      return res.status(404).json({ message: 'Produto não encontrado no banco!' });
    }
    
    // Se encontrar, envia o primeiro produto (Dipirona) de volta para o React Native
    return res.json(linhas[0]); 
    
  } catch (error) {
    console.error("Erro ao buscar produto no MySQL:", error);
    return res.status(500).json({ message: `Erro interno no servidor: ${error.message}` });
  }
});
  // 5. Movimentação de Estoque (Entrada / Saída)
  app.post('/api/estoque/movimentacao', async (req, res) => {
    const { productId, nome, quantidade } = req.body;
    const qtdNum = parseInt(quantidade);

    if (!productId || !nome || isNaN(qtdNum) || qtdNum <= 0) {
      return res.status(400).json({ message: 'Dados inválidos.' });
    }

    const connection = await db.getConnection();
    try {
      await connection.beginTransaction();

      // Atualiza estoque na tabela 'produto' usando a coluna 'quantidade' e 'produto_id'
      const sqlStock = type === 'Entrada'
        ? 'UPDATE produto SET quantidade = quantidade + ? WHERE produto_id = ?'
        : 'UPDATE produto SET quantidade = quantidade - ? WHERE produto_id = ? AND quantidade >= ?';

      const params = type === 'Entrada' ? [qtdNum, productId] : [qtdNum, productId, qtdNum];
      const [result] = await connection.query(sqlestoque, params);

      if (result.affectedRows === 0) {
        await connection.rollback();
        return res.status(400).json({ message: 'Estoque insuficiente ou produto não encontrado.' });
      }

      // Registra Histórico
      const now = new Date();
      const dateStr = now.toLocaleDateString('pt-BR');
      const hourStr = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

      await connection.query(
        'INSERT INTO history (product_id, type, quantity, date, hour) VALUES (?, ?, ?, ?, ?)',
        [productId, type, qtyNum, dateStr, hourStr]
      );

      await connection.commit();
      res.json({ success: true, message: 'Movimentação realizada com sucesso!' });
    } catch (error) {
      await connection.rollback();
      res.status(500).json({ error: error.message });
    } finally {
      connection.release();
    }
  });

  // 6. Listar Histórico Completo
  app.get('/api/history', async (req, res) => {
    try {
      const [rows] = await db.query(
        'SELECT h.id, h.type, h.quantity, h.date, h.hour, p.nome as product ' +
        'FROM history h ' +
        'JOIN produto p ON h.product_id = p.produto_id ' +
        'ORDER BY h.id DESC'
      );
      res.json(rows);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });





  app.post('/pedido-entrada', async (req, res) => {
    const {
      data_hora, descricao, status_pedido, fornecedor_id, estoque_id, funcionario_id, rfid, local_id, produto_id, preco_custo, quantidade
    } = req.body;

    const connection = await db.getConnection();

    try {
      // Inicia uma transação para garantir que só salva a segunda tabela se a primeira funcionar
      await connection.beginTransaction();

      // 1. Insere na tabela pai: 'pedido_entrada'
      const queryPedido = `
      INSERT INTO pedido_entrada 
      (data_hora, descricao, status_pedido, fornecedor_id, estoque_id, funcionario_id, rfid, local_id) 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;

      const [resultadoPedido] = await connection.query(queryPedido, [
        data_hora,
        descricao,
        status_pedido,
        fornecedor_id,
        estoque_id || null,
        funcionario_id,
        rfid,
        local_id || null
      ]);

      // Captura o ID gerado automaticamente na tabela pai
      const novoPedidoId = resultadoPedido.insertId;

      // 2. Insere na tabela filho: 'itempedido_entrada'
      const queryItem = `
      INSERT INTO itempedido_entrada 
      (preco_custo, quantidade, produto_id, pedido_entrada_id) 
      VALUES (?, ?, ?, ?)
    `;

      await connection.query(queryItem, [
        preco_custo,
        quantidade,
        produto_id,
        novoPedidoId // Vincula o item ao ID do pedido gerado acima
      ]);

      // Se as duas inserções funcionaram perfeitamente, salva em definitivo no MySQL
      await connection.commit();

      return res.status(201).json({
        success: true,
        message: 'Pedido de entrada registrados com sucesso!',
        pedidoId: novoPedidoId
      });

    } catch (error) {
      // Se qualquer uma das tabelas falhar, desfaz tudo e não deixa dados soltos
      await connection.rollback();
      console.error("Erro ao salvar pedido de entrada completo:", error);
      return res.status(500).json({
        success: false,
        message: `Erro interno no servidor: ${error.message}`
      });
    } finally {
      connection.release();
    }
  });





  // Rota Unificada para Registrar a Saída de Estoque (Salva nas duas tabelas)
app.post('/pedido-saida', async (req, res) => {
  // Pega os dados enviados pelo arquivo ExitScreen do React Native
  const { 
    data_hora, 
    status_pedido, 
    descricao, 
    rfid, 
    cliente_id, 
    local_id, 
    estoque_id, 
    funcionario_id,
    quantidade,
    preco_venda,
    produto_id
  } = req.body;

  // Cria uma conexão separada para podermos trabalhar com transação (Transaction)
  const connection = await db.getConnection();

  try {
    // Inicia a transação. Se der erro no meio do caminho, nada é salvo no MySQL
    await connection.beginTransaction();

    // 1. Insere na tabela pai: 'pedido_saida' (Nomes exatos das colunas do seu banco)
    const queryPedidoSaida = `
      INSERT INTO pedido_saida 
      (data_hora, status_pedido, descricao, rfid, cliente_id, local_id, estoque_id, funcionario_id) 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const [resultadoSaida] = await connection.query(queryPedidoSaida, [
      data_hora, // Formato enviado: 'YYYY-MM-DD HH:MM:SS'
      status_pedido,
      descricao,
      rfid,
      cliente_id,
      local_id || null, // Se vier vazio do app, insere NULL no banco
      estoque_id,
      funcionario_id
    ]);

    // Captura o ID gerado automaticamente (PRIMARY KEY) desse novo pedido de saída
    const novoPedidoSaidaId = resultadoSaida.insertId;

    // 2. Insere na tabela filho: 'itempedido_saida' amarrando ao ID do pai acima
    const queryItemSaida = `
      INSERT INTO itempedido_saida 
      (quantidade, preco_venda, produto_id, pedido_sa_id_id) 
      VALUES (?, ?, ?, ?)
    `;

    // ATENÇÃO: Verifique se no seu print a coluna de vínculo chama-se exatamente 'pedido_sa_id_id' ou 'pedido_saida_id'
    await connection.query(queryItemSaida, [
      quantidade,
      preco_venda,
      produto_id,
      novoPedidoSaidaId // Chave estrangeira unindo o item ao cabeçalho da saída
    ]);

    // Se os dois INSERTs derem certo, aplica as mudanças de fato no MySQL
    await connection.commit();

    return res.status(201).json({
      success: true,
      message: 'Pedido de saída e itens cadastrados com sucesso!',
      pedidoSaidaId: novoPedidoSaidaId
    });

  } catch (error) {
    // Caso dê qualquer erro (como chave estrangeira que falhou), cancela tudo o que foi feito acima
    await connection.rollback();
    console.error("ERRO AO SALVAR SAÍDA COMPLETA:", error);
    return res.status(500).json({ 
      success: false, 
      message: `Erro interno no servidor: ${error.message}` 
    });
  } finally {
    // Libera a conexão de volta para o Pool do MySQL continuar livre
    connection.release();
  }
});





  const PORT = 3000;
  app.listen(PORT, () => console.log(`Servidor rodando em http://localhost:${PORT}`));