-- NOTAS FISCAIS DE SAÍDA --
SELECT
	'BASEXYZ' 'Base SX'
	,NF.BPLName 'Filial'
 	,'NF SAIDA' 'Tipo Doc'
	,Case NF.U_indPres
		when 1 then 'SIM'
		WHEN 0 THEN 'NAO'
	END 'Contribuinte'
	,NF.DocNum 'Doc SAP'
	,NF.Serial 'Nota Fiscal'
	,NF.DocDate 'Data Emissão'
	,NF.CardCode 'Codigo Cliente'
	,NF.CardName 'Cliente'
	,NF.U_SKILL_IndIEDest 'Contribuinte'
	,NF1.ItemCode 'Item'
	,NF1.Dscription 'Descricao do Item'
	,GP.ItmsGrpNam 'Grupo Produto'
	,ISNULL(NF1.unitMsr, '') 'Unidade'
	,NF1.Quantity 'Quantidade'
	,NF1.Price 'Unitário.'
	,NF1.LineTotal 'Total Produto'
	,NF1.CFOPCode 'CFOP'
	,CASE LEFT(NF1.CFOPCode,1)
		WHEN 1 THEN 'Entrada'
		WHEN 2 THEN 'Entrada'
		WHEN 3 THEN 'Entrada'
		WHEN 5 THEN 'Saida'
		WHEN 6 THEN 'Saida'
		WHEN 7 THEN 'Saida'
	END 'Tipo'
	,CASE right(NF1.CFOPCode,3) 
		WHEN '101' THEN 'SIM'
		WHEN '102' THEN 'SIM'
		WHEN '103' THEN 'SIM'
		WHEN '107' THEN 'SIM'
		WHEN '108' THEN 'SIM'
		WHEN '109' THEN 'SIM'
		WHEN '118' THEN 'SIM'
		WHEN '120' THEN 'SIM'
		WHEN '401' THEN 'SIM'
		WHEN '403' THEN 'SIM'
		WHEN '404' THEN 'SIM'
		WHEN '405' THEN 'SIM'
		WHEN '551' THEN 'SIM'
		WHEN '922' THEN 'SIM'
		WHEN '933' THEN 'SIM'
		ELSE 'NAO' 
	END 'Receita'
	,ISNULL(NF1.StockPrice * NF1.Quantity, 0) 'CMV'


	--Aliquotas dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Aliq. IPI'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Aliq. PIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Aliq. CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Aliq. DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Aliq. FCP'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Aliq. ISS'

	--Valor dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Valor IPI'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Valor ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Valor ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Valor PIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Valor CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Valor DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Valor FCP'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Valor ISS'

	,NF1.AcctCode 'Conta Contábil'
	,ISNULL(RP.AgentName, '') 'Representante'
	,CASE VD.SlpCode
		WHEN '-1' THEN ''
		ELSE ISNULL(VD.SlpName, '') 
	 END 'Vendedor'
	,NF12.CityS 'Cidade'
	,NF12.StateS 'UF'



FROM
	OINV NF
	INNER JOIN INV1 NF1 ON NF.DocEntry = NF1.DocEntry
	INNER JOIN INV12 NF12 ON NF.DocEntry = NF12.DocEntry
	INNER JOIN OITM IT ON NF1.ItemCode = IT.ItemCode
	INNER JOIN OITB GP ON IT.ItmsGrpCod = GP.ItmsGrpCod
	LEFT JOIN OAGP RP ON NF.AgentCode = RP.AgentCode
	LEFT JOIN OSLP VD ON NF.SlpCode = VD.SlpCode

WHERE
	NF.CANCELED = 'N'
	--AND NF.NumAtCard = '4500553999'
	--AND NF.DocEntry = 3084
	--AND NF1.TargetType <> '14'


UNION ALL

-- ENTREGA --
SELECT
	'BASEXYZ' 'Base SX'
	,NF.BPLName 'Filial'
	,'ENTREGA' 'Tipo Doc'
	,Case NF.U_indPres
		when 1 then 'SIM'
		WHEN 0 THEN 'NAO'
	END 'Contribuinte'
	,NF.DocNum 'Nº Doc SAP'
	,NF.Serial 'Nº NF'
	,NF.DocDate 'Data Emissão'
	,NF.CardCode 'Cod. Cliente'
	,NF.CardName 'Cliente'
	,NF.U_SKILL_IndIEDest 'Contribuinte'
	,NF1.ItemCode 'Item'
	,NF1.Dscription 'Descrição do Item'
	,GP.ItmsGrpNam 'Grupo Produto'
	,ISNULL(NF1.unitMsr, '') 'UM'
	,NF1.Quantity 'Quantidade'
	,NF1.Price 'Preço Unit.'
	,NF1.LineTotal 'Total Produto'
	,NF1.CFOPCode 'CFOP'
	,CASE LEFT(NF1.CFOPCode,1)
		WHEN 1 THEN 'Entrada'
		WHEN 2 THEN 'Entrada'
		WHEN 3 THEN 'Entrada'
		WHEN 5 THEN 'Saida'
		WHEN 6 THEN 'Saida'
		WHEN 7 THEN 'Saida'
	END 'Tipo'
	,CASE right(NF1.CFOPCode,3) 
		WHEN '101' THEN 'SIM'
		WHEN '102' THEN 'SIM'
		WHEN '103' THEN 'SIM'
		WHEN '107' THEN 'SIM'
		WHEN '108' THEN 'SIM'
		WHEN '109' THEN 'SIM'
		WHEN '118' THEN 'SIM'
		WHEN '120' THEN 'SIM'
		WHEN '401' THEN 'SIM'
		WHEN '403' THEN 'SIM'
		WHEN '404' THEN 'SIM'
		WHEN '405' THEN 'SIM'
		WHEN '551' THEN 'SIM'
		WHEN '922' THEN 'SIM'
		WHEN '933' THEN 'SIM'
		ELSE 'NAO' 
	END 'Receita'
	,ISNULL(NF1.StockPrice * NF1.Quantity, 0) 'CMV'

	
	--Aliquotas dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Aliq. IPI'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Aliq. PIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Aliq. CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Aliq. DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Aliq. FCP'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Aliq. ISS'

	--Valor dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Valor IPI'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Valor ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Valor ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Valor PIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Valor CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Valor DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Valor FCP'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Valor ISS'

	,NF1.AcctCode 'Conta Contábil'
	,ISNULL(RP.AgentName, '') 'Representante'
	,CASE VD.SlpCode
		WHEN '-1' THEN ''
		ELSE ISNULL(VD.SlpName, '') 
	 END 'Vendedor'
	,NF12.CityS 'Cidade'
	,NF12.StateS 'UF'


FROM
	ODLN NF
	INNER JOIN DLN1 NF1 ON NF.DocEntry = NF1.DocEntry
	INNER JOIN DLN12 NF12 ON NF.DocEntry = NF12.DocEntry
	INNER JOIN OITM IT ON NF1.ItemCode = IT.ItemCode
	INNER JOIN OITB GP ON IT.ItmsGrpCod = GP.ItmsGrpCod
	LEFT JOIN OAGP RP ON NF.AgentCode = RP.AgentCode
	LEFT JOIN OSLP VD ON NF.SlpCode = VD.SlpCode

WHERE
	NF.CANCELED = 'N'
	--AND NF.NumAtCard = '4500553999'
	--AND NF.DocEntry = 3084
	--AND NF1.TargetType <> '14'


UNION ALL

-- DEV. NOTAS FISCAIS DE SAÍDA --
SELECT
	'BASEXYZ' 'Base SX'
	,NF.BPLName 'Filial'
	,'DV NF SAIDA' 'Tipo Doc'
	,Case NF.U_indPres
		when 1 then 'SIM'
		WHEN 0 THEN 'NAO'
	END 'Contribuinte'
	,NF.DocNum 'Nº Doc SAP'
	,NF.Serial 'Nº NF'
	,NF.DocDate 'Data Emissão'
	,NF.CardCode 'Cod. Cliente'
	,NF.CardName 'Cliente'
	,NF.U_SKILL_IndIEDest 'Contribuinte'
	,NF1.ItemCode 'Item'
	,NF1.Dscription 'Descrição do Item'
	,GP.ItmsGrpNam 'Grupo Produto'
	,ISNULL(NF1.unitMsr, '') 'UM'
	,-1 * NF1.Quantity 'Quantidade'
	,-1 * NF1.Price 'Preço Unit.'
	,-1 * NF1.LineTotal 'Total Produto'
	,NF1.CFOPCode 'CFOP'
	,CASE LEFT(NF1.CFOPCode,1)
		WHEN 1 THEN 'Entrada'
		WHEN 2 THEN 'Entrada'
		WHEN 3 THEN 'Entrada'
		WHEN 5 THEN 'Saida'
		WHEN 6 THEN 'Saida'
		WHEN 7 THEN 'Saida'
	END 'Tipo'
	,CASE right(NF1.CFOPCode,3) 
		WHEN '101' THEN 'SIM'
		WHEN '102' THEN 'SIM'
		WHEN '103' THEN 'SIM'
		WHEN '107' THEN 'SIM'
		WHEN '108' THEN 'SIM'
		WHEN '109' THEN 'SIM'
		WHEN '118' THEN 'SIM'
		WHEN '120' THEN 'SIM'
		WHEN '401' THEN 'SIM'
		WHEN '403' THEN 'SIM'
		WHEN '404' THEN 'SIM'
		WHEN '405' THEN 'SIM'
		WHEN '551' THEN 'SIM'
		WHEN '922' THEN 'SIM'
		WHEN '933' THEN 'SIM'
		ELSE 'NAO' 
	END 'Receita'
	,-1 * ISNULL(NF1.StockPrice * NF1.Quantity, 0) 'CMV'
	
	--Aliquotas dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Aliq. IPI'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Aliq. PIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Aliq. CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Aliq. DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Aliq. FCP'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Aliq. ISS'

	--Valor dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Valor IPI'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Valor ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Valor ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Valor PIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Valor CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Valor DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Valor FCP'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Valor ISS'

	,NF1.AcctCode 'Conta Contábil'
	,ISNULL(RP.AgentName, '') 'Representante'
	,CASE VD.SlpCode
		WHEN '-1' THEN ''
		ELSE ISNULL(VD.SlpName, '') 
	 END 'Vendedor'
	,NF12.CityS 'Cidade'
	,NF12.StateS 'UF'


FROM
	ORIN NF
	INNER JOIN RIN1 NF1 ON NF.DocEntry = NF1.DocEntry
	INNER JOIN RIN12 NF12 ON NF.DocEntry = NF12.DocEntry
	INNER JOIN OITM IT ON NF1.ItemCode = IT.ItemCode
	INNER JOIN OITB GP ON IT.ItmsGrpCod = GP.ItmsGrpCod
	LEFT JOIN OAGP RP ON NF.AgentCode = RP.AgentCode
	LEFT JOIN OSLP VD ON NF.SlpCode = VD.SlpCode

WHERE
	NF.CANCELED = 'N'
	--AND NF.NumAtCard = '4500553999'
	--AND NF.DocEntry = 3084
	AND NF1.BaseType = '13'

UNION ALL

-- DEVOLUÇÃO --
SELECT
	'BASEXYZ' 'Base SX'
	,NF.BPLName 'Filial'
	,'DEVOLUCAO' 'Tipo Doc'
	,Case NF.U_indPres
		when 1 then 'SIM'
		WHEN 0 THEN 'NAO'
	END 'Contribuinte'
	,NF.DocNum 'Nº Doc SAP'
	,NF.Serial 'Nº NF'
	,NF.DocDate 'Data Emissão'
	,NF.CardCode 'Cod. Cliente'
	,NF.CardName 'Cliente'
	,NF.U_SKILL_IndIEDest 'Contribuinte'
	,NF1.ItemCode 'Item'
	,NF1.Dscription 'Descrição do Item'
	,GP.ItmsGrpNam 'Grupo Produto'
	,ISNULL(NF1.unitMsr, '') 'UM'
	,-1 * NF1.Quantity 'Quantidade'
	,-1 * NF1.Price 'Preço Unit.'
	,-1 * NF1.LineTotal 'Total Produto'
	,NF1.CFOPCode 'CFOP'
	,CASE LEFT(NF1.CFOPCode,1)
		WHEN 1 THEN 'Entrada'
		WHEN 2 THEN 'Entrada'
		WHEN 3 THEN 'Entrada'
		WHEN 5 THEN 'Saida'
		WHEN 6 THEN 'Saida'
		WHEN 7 THEN 'Saida'
	END 'Tipo'
	,CASE right(NF1.CFOPCode,3) 
		WHEN '101' THEN 'SIM'
		WHEN '102' THEN 'SIM'
		WHEN '103' THEN 'SIM'
		WHEN '107' THEN 'SIM'
		WHEN '108' THEN 'SIM'
		WHEN '109' THEN 'SIM'
		WHEN '118' THEN 'SIM'
		WHEN '120' THEN 'SIM'
		WHEN '401' THEN 'SIM'
		WHEN '403' THEN 'SIM'
		WHEN '404' THEN 'SIM'
		WHEN '405' THEN 'SIM'
		WHEN '551' THEN 'SIM'
		WHEN '922' THEN 'SIM'
		WHEN '933' THEN 'SIM'
		ELSE 'NAO' 
	END 'Receita'
	,-1 * ISNULL(NF1.StockPrice * NF1.Quantity, 0) 'CMV'

	--Aliquotas dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Aliq. IPI'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Aliq. ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Aliq. PIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Aliq. CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Aliq. DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Aliq. FCP'
	,(SELECT ISNULL(SUM(NF4.TaxRate), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Aliq. ISS'

	--Valores dos impostos
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 16 AND NF4.RelateType NOT IN (11)) 'Valor IPI'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (10, 11) AND NF4.RelateType NOT IN (11)) 'Valor ICMS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType = 13 AND NF4.RelateType NOT IN (11)) 'Valor ICMS-ST'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (19, 20) AND NF4.RelateType NOT IN (11)) 'Valor PIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (21, 22) AND NF4.RelateType NOT IN (11)) 'Valor CONFIS'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (32) AND NF4.RelateType NOT IN (11)) 'Valor DIFAL'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (25, 29, 30, 34) AND NF4.RelateType NOT IN (11)) 'Valor FCP'
	,(SELECT ISNULL(SUM(NF4.TaxSum), 0) FROM INV4 NF4 WHERE NF4.DocEntry = NF1.DocEntry AND NF4.LineNum = NF1.LineNum AND NF4.staType IN (24) AND NF4.RelateType NOT IN (11)) 'Valor ISS'

	,NF1.AcctCode 'Conta Contábil'
	,ISNULL(RP.AgentName, '') 'Representante'
	,CASE VD.SlpCode
		WHEN '-1' THEN ''
		ELSE ISNULL(VD.SlpName, '') 
	 END 'Vendedor'
	,NF12.CityS 'Cidade'
	,NF12.StateS 'UF'

FROM
	ORDN NF
	INNER JOIN RDN1 NF1 ON NF.DocEntry = NF1.DocEntry
	INNER JOIN RDN12 NF12 ON NF.DocEntry = NF12.DocEntry
	INNER JOIN OITM IT ON NF1.ItemCode = IT.ItemCode
	INNER JOIN OITB GP ON IT.ItmsGrpCod = GP.ItmsGrpCod
	LEFT JOIN OAGP RP ON NF.AgentCode = RP.AgentCode
	LEFT JOIN OSLP VD ON NF.SlpCode = VD.SlpCode

WHERE
	NF.CANCELED = 'N'
	--AND NF.NumAtCard = '4500553999'
	--AND NF.DocEntry = 3084
	AND (NF1.BaseType = '15' OR NF1.TargetType = '15')

