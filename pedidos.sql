SELECT
T1.[BPLName] as 'Filial', 
T3.[SlpName] as 'Vendedor', 
T1.[AgentCode] as 'Representante', 
T1.[DocNum] as 'Pedido',
T0.[LineNum] + 1 as 'Linha',
T5.[Usage] as 'Utilizacao',
T1.[DocDate] as'Data Emissao', 
T0.[ShipDate] as'Data Entrega', 
T1.[Comments] as 'Comentários',
T1.[CardCode] as 'Cod Cliente', 
T1.[CardName] as 'Cliente',
T0.[ItemCode] as 'Codigo', 
T0.[Dscription] as 'Descricao', 
T0.U_TabelaComiss as 'Comissao',
MAX(T0.[Quantity]) as 'Quantidade', 
MAX(T0.[OpenQty]) as 'Quantidade Pendente', 
AVG(T0.[Price]) 'Valor Unitario Produto',
MAX(T0.[Quantity] * T0.[Price]) as 'Valor total do Pedido', 
MAX(T0.[OpenQty] * T0.[Price]) as 'Valor Total Pendente', 
T1.[PeyMethod] as 'Forma de Pagamento',
(Case T0.TreeType WHEN 'P' THEN 'Produção' WHEN 'N' THEN 'Não é componente de Lista' END) as'Tipo Estrutura',
T2.[absEntry] as 'Numero Picking',
T2.[UpdateDate] as 'Data Picking',
T1.[CANCELED] as 'Cancelado',
T0.[TaxCode] AS 'Cod Imposto',
MAX(ISNULL(T40.[TaxSum],0)) as 'Valor ISS',
MAX(ISNULL(T41.[TaxSum],0)) as 'Valor ICMS',
MAX(ISNULL(T42.[TaxSum],0)) as 'Valor ICMS ST',
MAX(ISNULL(T43.[TaxSum],0)) as 'Valor ICMS DIFAL',
MAX(ISNULL(T44.[TaxSum],0)) as 'Valor FCP',
MAX(ISNULL(T45.[TaxSum],0)) as 'Valor IPI',
MAX(ISNULL(T46.[TaxSum],0)) as 'Valor PIS',
MAX(ISNULL(T47.[TaxSum],0)) as 'Valor COFINS',
MIN(((T0.[Quantity] * T0.[Price]) - ISNULL(T42.[TaxSum],0) - ISNULL(T41.[TaxSum],0)  - ISNULL(T46.[TaxSum],0)  - ISNULL(T47.[TaxSum],0) )) as 'Valor Receita Líquida Pedido',
MAX(((T0.[Quantity] * T0.[Price]) + ISNULL(T42.[TaxSum],0) + ISNULL(T43.[TaxSum],0) + ISNULL(T45.[TaxSum],0) + ISNULL(T44.[TaxSum],0) )) as 'Valor Receita Bruta Pedido',
MIN((((T0.[Quantity] * T0.[Price]) - ISNULL(T42.[TaxSum],0) - ISNULL(T41.[TaxSum],0)  - ISNULL(T46.[TaxSum],0)  - ISNULL(T47.[TaxSum],0) ) / T0.[Quantity] * T0.[OpenQty])) as 'Valor Receita Líquida Pendente',
MAX((((T0.[Quantity] * T0.[Price]) + ISNULL(T42.[TaxSum],0) + ISNULL(T43.[TaxSum],0) + ISNULL(T45.[TaxSum],0) + ISNULL(T44.[TaxSum],0) ) / T0.[Quantity] * T0.[OpenQty])) as 'Valor Receita Bruta Pendente',
(CASE ISNULL(T7.[isIns],'N') WHEN 'Y' THEN 'SIM' WHEN 'N' THEN 'NÃO' END) AS 'Venda Futura?',
(CASE T7.[InvntSttus] when 'O' then 'ABERTO' when 'C' THEN 'FECHADO' END) as 'Status Venda Futura'



FROM
RDR1 T0	
INNER JOIN ORDR T1 ON T0.[DocEntry] = T1.[DocEntry]
INNER JOIN OSLP T3 ON T3.[SlpCode] = T1.[SlpCode]
INNER JOIN OUSG T5 ON T0.[Usage] = T5.[ID]
LEFT JOIN INV1 T6 ON T0.[DocEntry] = T6.[BaseEntry] AND T0.[LineNum] = T6.[BaseLine] AND T0.[ObjType] = T6.[BaseType]
LEFT JOIN OINV T7 ON T7.[DocEntry] = T6.[DocEntry]
LEFT JOIN OPKL T2 on T0.[PickIdNo] = T2.[AbsEntry]
LEFT JOIN RDR4 T40 ON T0.[DocEntry] = T40.[DocEntry] AND T40.[LineNum] = T0.[LineNum] AND T40.[TaxAcct] = '2.01.04.01.0001'
LEFT JOIN RDR4 T41 ON T0.[DocEntry] = T41.[DocEntry] AND T41.[LineNum] = T0.[LineNum] AND T41.[TaxAcct] = '2.01.04.02.0001' 
LEFT JOIN RDR4 T42 ON T0.[DocEntry] = T42.[DocEntry] AND T42.[LineNum] = T0.[LineNum] AND T42.[TaxAcct] = '2.01.04.02.0002' 
LEFT JOIN RDR4 T43 ON T0.[DocEntry] = T43.[DocEntry] AND T43.[LineNum] = T0.[LineNum] AND T43.[TaxAcct] = '2.01.04.02.0003'
LEFT JOIN RDR4 T44 ON T0.[DocEntry] = T44.[DocEntry] AND T44.[LineNum] = T0.[LineNum] AND T44.[TaxAcct] = '2.01.04.02.0004'
LEFT JOIN RDR4 T45 ON T0.[DocEntry] = T45.[DocEntry] AND T45.[LineNum] = T0.[LineNum] AND T45.[TaxAcct] = '2.01.04.03.0002'
LEFT JOIN RDR4 T46 ON T0.[DocEntry] = T46.[DocEntry] AND T46.[LineNum] = T0.[LineNum] AND T46.[TaxAcct] = '2.01.04.03.0003' 
LEFT JOIN RDR4 T47 ON T0.[DocEntry] = T47.[DocEntry] AND T47.[LineNum] = T0.[LineNum] AND T47.[TaxAcct] = '2.01.04.03.0004'


WHERE T1.[CANCELED] = 'N' AND T0.[OpenQty] > 0
GROUP BY 
T1.[BPLName],
T3.[SlpName],
T1.[AgentCode],
T1.[DocNum],
T0.[LineNum],
T5.[Usage],
T1.[DocDate],
T0.[ShipDate],
T1.[Comments],
T1.[CardCode],
T1.[CardName],
T0.[ItemCode],
T0.[Dscription],
T0.[U_TabelaComiss],
T1.[PeyMethod],
T0.TreeType,
T2.[absEntry],
T2.[UpdateDate],
T1.[CANCELED],
T0.[TaxCode],
t7.[InvntSttus],
T7.[isIns]


union all

SELECT
T1.[BPLName] as 'Filial', 
T3.[SlpName] as 'Vendedor', 
T1.[AgentCode] as 'Representante', 
T1.[DocNum] as 'Pedido',
T0.[LineNum] + 1 as 'Linha',
T5.[Usage] as 'Utilizacao',
T1.[DocDate] as'Data Emissao', 
T0.[ShipDate] as'Data Entrega', 
T1.[Comments] as 'Comentários',
T1.[CardCode] as 'Cod Cliente', 
T1.[CardName] as 'Cliente',
T0.[ItemCode] as 'Codigo', 
T0.[Dscription] as 'Descricao', 
T0.U_TabelaComiss as 'Comissao',
MAX(T0.[Quantity]) as 'Quantidade', 
MAX(T0.[OpenQty]) as 'Quantidade Pendente', 
AVG(T0.[Price]) 'Valor Unitario Produto',
MAX(T0.[Quantity] * T0.[Price]) as 'Valor total do Pedido', 
MAX(T0.[OpenQty] * T0.[Price]) as 'Valor Total Pendente', 
T1.[PeyMethod] as 'Forma de Pagamento',
(Case T0.TreeType WHEN 'P' THEN 'Produção' WHEN 'N' THEN 'Não é componente de Lista' END) as'Tipo Estrutura',
T2.[absEntry] as 'Numero Picking',
T2.[UpdateDate] as 'Data Picking',
T1.[CANCELED] as 'Cancelado',
T0.[TaxCode] AS 'Cod Imposto',
MAX(ISNULL(T40.[TaxSum],0)) as 'Valor ISS',
MAX(ISNULL(T41.[TaxSum],0)) as 'Valor ICMS',
MAX(ISNULL(T42.[TaxSum],0)) as 'Valor ICMS ST',
MAX(ISNULL(T43.[TaxSum],0)) as 'Valor ICMS DIFAL',
MAX(ISNULL(T44.[TaxSum],0)) as 'Valor FCP',
MAX(ISNULL(T45.[TaxSum],0)) as 'Valor IPI',
MAX(ISNULL(T46.[TaxSum],0)) as 'Valor PIS',
MAX(ISNULL(T47.[TaxSum],0)) as 'Valor COFINS',
MIN(((T0.[Quantity] * T0.[Price]) - ISNULL(T42.[TaxSum],0) - ISNULL(T41.[TaxSum],0)  - ISNULL(T46.[TaxSum],0)  - ISNULL(T47.[TaxSum],0) )) as 'Valor Receita Líquida Pedido',
MAX(((T0.[Quantity] * T0.[Price]) + ISNULL(T42.[TaxSum],0) + ISNULL(T43.[TaxSum],0) + ISNULL(T45.[TaxSum],0) + ISNULL(T44.[TaxSum],0) )) as 'Valor Receita Bruta Pedido',
MIN((((T0.[Quantity] * T0.[Price]) - ISNULL(T42.[TaxSum],0) - ISNULL(T41.[TaxSum],0)  - ISNULL(T46.[TaxSum],0)  - ISNULL(T47.[TaxSum],0) ) / T0.[Quantity] * T0.[OpenQty])) as 'Valor Receita Líquida Pendente',
MAX((((T0.[Quantity] * T0.[Price]) + ISNULL(T42.[TaxSum],0) + ISNULL(T43.[TaxSum],0) + ISNULL(T45.[TaxSum],0) + ISNULL(T44.[TaxSum],0) ) / T0.[Quantity] * T0.[OpenQty])) as 'Valor Receita Bruta Pendente',
(CASE ISNULL(T7.[isIns],'N') WHEN 'Y' THEN 'SIM' WHEN 'N' THEN 'NÃO' END) AS 'Venda Futura?',
(CASE T7.[InvntSttus] when 'O' then 'ABERTO' when 'C' THEN 'FECHADO' END) as 'Status Venda Futura'



FROM
RDR1 T0	
INNER JOIN ORDR T1 ON T0.[DocEntry] = T1.[DocEntry]
INNER JOIN OSLP T3 ON T3.[SlpCode] = T1.[SlpCode]
INNER JOIN OUSG T5 ON T0.[Usage] = T5.[ID]
LEFT JOIN INV1 T6 ON T0.[DocEntry] = T6.[BaseEntry] AND T0.[LineNum] = T6.[BaseLine] AND T0.[ObjType] = T6.[BaseType]
LEFT JOIN OINV T7 ON T7.[DocEntry] = T6.[DocEntry]
LEFT JOIN OPKL T2 on T0.[PickIdNo] = T2.[AbsEntry]
LEFT JOIN RDR4 T40 ON T0.[DocEntry] = T40.[DocEntry] AND T40.[LineNum] = T0.[LineNum] AND T40.[TaxAcct] = '2.01.04.01.0001'
LEFT JOIN RDR4 T41 ON T0.[DocEntry] = T41.[DocEntry] AND T41.[LineNum] = T0.[LineNum] AND T41.[TaxAcct] = '2.01.04.02.0001' 
LEFT JOIN RDR4 T42 ON T0.[DocEntry] = T42.[DocEntry] AND T42.[LineNum] = T0.[LineNum] AND T42.[TaxAcct] = '2.01.04.02.0002' 
LEFT JOIN RDR4 T43 ON T0.[DocEntry] = T43.[DocEntry] AND T43.[LineNum] = T0.[LineNum] AND T43.[TaxAcct] = '2.01.04.02.0003'
LEFT JOIN RDR4 T44 ON T0.[DocEntry] = T44.[DocEntry] AND T44.[LineNum] = T0.[LineNum] AND T44.[TaxAcct] = '2.01.04.02.0004'
LEFT JOIN RDR4 T45 ON T0.[DocEntry] = T45.[DocEntry] AND T45.[LineNum] = T0.[LineNum] AND T45.[TaxAcct] = '2.01.04.03.0002'
LEFT JOIN RDR4 T46 ON T0.[DocEntry] = T46.[DocEntry] AND T46.[LineNum] = T0.[LineNum] AND T46.[TaxAcct] = '2.01.04.03.0003' 
LEFT JOIN RDR4 T47 ON T0.[DocEntry] = T47.[DocEntry] AND T47.[LineNum] = T0.[LineNum] AND T47.[TaxAcct] = '2.01.04.03.0004'

GROUP BY 
T1.[BPLName],
T3.[SlpName],
T1.[AgentCode],
T1.[DocNum],
T0.[LineNum],
T5.[Usage],
T1.[DocDate],
T0.[ShipDate],
T1.[Comments],
T1.[CardCode],
T1.[CardName],
T0.[ItemCode],
T0.[Dscription],
T0.[U_TabelaComiss],
T1.[PeyMethod],
T0.TreeType,
T2.[absEntry],
T2.[UpdateDate],
T1.[CANCELED],
T0.[TaxCode],
t7.[InvntSttus],
T7.[isIns]
