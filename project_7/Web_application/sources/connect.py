import pyodbc
import pandas as pd
 

class Sql:
    def __init__(self, database='I**B', server="192.168.***.***"):
        self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+server+";"
                                   "Database="+database+";"
                                   "Trusted_Connection=yes;")

sql = Sql()


def get_data(argument):
  """ Функция для получения из базы данных
  набора случаев медпомощи, по заданным параметрам,
  для проведения предсказания возможности наличия 
  дефектов медпомощи
    
    Args:
        - argument: набор параметров для отбора случаев
    Returns:
        - полученные данные в виде датасет
  """
  SQL_QUERY = """select 
    ss.SchetSluchID as [UUID]
    ,sz.ENP as [ENP]
    ,sz.FAM as [FAM]
    ,sz.IM as [IM]
    ,sz.OT as [OT] 
    ,CONVERT(VARCHAR(10), sz.DR, 104) as [BIRTHDAY]
	,case when sz.ENP is not null then sz.ENP+'_'+SUBSTRING(sz.FAM,0,2)+SUBSTRING(sz.IM,0,2)+SUBSTRING(isnull(sz.OT,' '),0,2)
      when sz.ENP is null then sz.NPOLIS+'_'+SUBSTRING(sz.FAM,0,2)+SUBSTRING(sz.IM,0,2)+SUBSTRING(isnull(sz.OT,' '),0,2) end as [PERSCODE]
    ,s.month as [month]
    ,s.PLAT as [SMO]
    ,SUBSTRING(s.FILENAME, 0,2) as [FILENAME]
    ,s.CODE_MO as [MO]
    ,case when ssa.R_IS_FAP = 1 then 'FAP'
      when s.CODE_MO in ('830005','830007','830008','830015','830016','830017','830020') then 'CRB'
	  when s.CODE_MO in ('830004','830009','830011','830022','830023') then 'GB'
	  when s.CODE_MO in ('830001') then 'OKB'
	  when s.CODE_MO in ('830013','830024','830050') then 'VED'
	  else 'OTER' end as [TYPE_MO]
    ,CONVERT(VARCHAR(10), isnull(ssa.NPR_DATE,ssa.DATE_Z_1), 104) as [NPR_DATE]
    ,ssa.NPR_MO as [NPR_MO]
    ,ssa.VIDPOM
    ,isnull(ssa.USL_OK, 3) as [USL_OK]
    ,case when ssa.FOR_POM is null then 3
	  else ssa.FOR_POM end as [FOR_POM]
    ,v025.N_PC as [P_CEL]
    ,isnull(c_z.IDCZ, 3) as [C_ZAB]
    ,case when ss.PROFIL is null and ss.DET = 1 then 68
	  when ss.PROFIL is null and ss.DET = 0 then 97
	  when ss.PROFIL is null and SUBSTRING(s.FILENAME, 0,3) in ('DS', 'DU', 'DF') then 68
	  when ss.PROFIL is null and SUBSTRING(s.FILENAME, 0,3) in ('DP', 'DV', 'DO', 'DA', 'DB', 'DR', 'DY') then 97
	  else ss.PROFIL end as [PROFIL]
    ,isnull(v020.K_PRNAME, 'no_hospital') as [BED_PROFILE]
    ,case when ss.PRVS3 is null and ss.DET = 1 then 49
	  when ss.PRVS3 is null and ss.DET = 0 then 76
	  when ss.PRVS3 is null and SUBSTRING(s.FILENAME, 0,3) in ('DS', 'DU', 'DF') then 49
	  when ss.PRVS3 is null and SUBSTRING(s.FILENAME, 0,3) in ('DP', 'DV', 'DO', 'DA', 'DB', 'DR', 'DY') then 76
	  else ss.PRVS3 end as [SPEC_CODE]
    ,ss.DS0 as [DS0]
    ,ss.DS1 as [DS1]
    ,isnull(ss.DS1_PR,0) as [DS1_PR]
    , (select top(1) ds2.MKB from [IESDB].ies.T_SCHET_SLUCH_ACCOMPLISHED ssa2
										join [IESDB].ies.T_SCHET_SLUCH ss2 on ssa2.SchetSluchAccomplishedID=ss2.SchetSluchAccomplished
										left join [IESDB].[IES].[T_SCHET_SLUCH_DS] ds2 on ds2.SchetSluch = ss2.SchetSluchID and ds2.MKBType = 0
										where ssa.SchetSluchAccomplishedID = ssa2.SchetSluchAccomplishedID
										order by ss2.DATE_2 asc 
										) as [DS2]
    , (select top(1) ds3.MKB from [IESDB].ies.T_SCHET_SLUCH_ACCOMPLISHED ssa2
										join [IESDB].ies.T_SCHET_SLUCH ss2 on ssa2.SchetSluchAccomplishedID=ss2.SchetSluchAccomplished
										left join [IESDB].[IES].[T_SCHET_SLUCH_DS] ds3 on ds3.SchetSluch = ss2.SchetSluchID and ds3.MKBType = 1
										where ssa.SchetSluchAccomplishedID = ssa2.SchetSluchAccomplishedID
										order by ss2.DATE_2 asc 
										) as [DS3]
    ,case when ksg.N_KSG is not null then ksg.N_KSG
      when v019.IDHM is not null then CONVERT(VARCHAR(5), v019.IDHM)
	  when (select top(1) usl.CODE_USL from [IESDB].[IES].[T_SCHET_USL] usl where usl.SchetSluch=ss.SchetSluchID) is not null 
	  then (select top(1) usl.CODE_USL from [IESDB].[IES].[T_SCHET_USL] usl where usl.SchetSluch=ss.SchetSluchID) end as [CODE_USL]
    ,(select count(usl1.CODE_USL) from [IESDB].[IES].[T_SCHET_USL] usl1 where usl1.SchetSluch=ss.SchetSluchID) as [KOL_USL]
    ,sug.GroupNumber as [GROUP_OMU]
    ,ss.R_ISDENT as [R_ISDENT]
    ,case when DATEDIFF(day,ss.DATE_1,ss.DATE_2)>0 then DATEDIFF(day,ss.DATE_1,ss.DATE_2) else 1 end [KD]
    ,ss.NHISTORY+'_'+s.CODE_MO as [NHISTORY]
    ,isnull(ss.PR_D_N,0) as [DN]
    ,sz.W as [SEX]
    ,CONVERT(VARCHAR(10), ss.DATE_1, 104) as [DATE_1]
    ,CONVERT(VARCHAR(10), ss.DATE_2, 104) as [DATE_2]
    ,isnull(ssa.ISHOD, 306) as [ISHOD]  
    ,case when ssa.RSLT is null then ssa.RSLT_D 
	  else ssa.RSLT end as [RSLT]
    ,ss.TARIF as [TARIF]
    ,ss.SUMV as [SUMV]
    ,(select v024.IDDKK + '#' as [text()] from [IESDB].[IES].[T_KSG_CRIT] crit 
					join [IESDB].[IES].[T_V024_DOP_KR] v024 on v024.V024DopKrID = crit.V024DopKr
					where crit.Ksg = ksg.KsgID
					FOR XML PATH('')) as [CRIT]
    ,ssa.IDSP as [IDSP]
    ,case when ss.IDDOKT is null then
	  (select top(1) mru.[CODE_MD] from [IESDB].[IES].[T_SCHET_USL] usl2 join [IESDB].[IES].[T_MR_USL_N] mru on mru.SchetUsl = usl2.SchetUslID where usl2.SchetSluch=ss.SchetSluchID)
	  else ss.IDDOKT
	  end as [IDDOKT]
    ,ss.LPU_1 as [CODE_OTD]
    ,(select count(usl.CODE_USL) from [IESDB].[IES].[T_SCHET_USL] usl where usl.SchetSluch=ss.SchetSluchID and usl.CODE_USL = 'B03.003.005') as [ORIT]
    ,isnull(ss.REAB,0) as [REAB]
    ,case when ss.DET is null and SUBSTRING(s.FILENAME, 0,3) in ('DS', 'DU', 'DF') then 1
	  else 0 end as [DET]
    ,ssa.R_FULL_AGE_ON_DATE_1 as [AGE]
    ,i.NATION as [COUNTRY]
    ,ss.ED_COL as [ED_COL]

     from [IESDB].ies.T_SCHET_SLUCH ss
    join [IESDB].ies.T_SCHET_SLUCH_ACCOMPLISHED ssa on ssa.SchetSluchAccomplishedID=ss.SchetSluchAccomplished and ssa.DATE_Z_2 >= '20230101'
    join [IESDB].ies.T_SCHET_ZAP sz on sz.SchetZapID=ssa.SchetZap
    join [IESDB].ies.T_SCHET s on s.SchetID=sz.Schet
    left join [IESDB].ies.T_KSG ksg on ksg.SchetSluch=ss.SchetSluchID
    left join [IESDB].[IES].[T_V019_VMP_METHOD] v019 on v019.V019VmpMethodID = ss.METOD_HMP	
    left join [IESDB].ies.T_V020_BED_PROFILE v020 on v020.V020BedProfileID=ss.PROFIL_K	
    left join [IESDB].[IES].[T_INSURED] i on sz.ENP = i.ENP 
    left join [IESDB].ies.R_NSI_SINGLE_USL_GROUP sug on sug.DictionaryBaseID=ss.R_SINGLE_USL_TYPE
    left join [IESDB].ies.T_V025_KPC v025 on v025.V025KpcID=ss.P_CEL
    left join [IESDB].ies.T_V027_C_ZAB c_z on c_z.V027CZabID = ss.C_ZAB

    where s.type_ in (693,554)
    and s.IsDelete <> 1
    and ssa.SUMP > 0
    """+str(argument)+"""
    ;
    """

  cursor = sql.cnxn.cursor()
  cursor.execute(SQL_QUERY)
  answer_temp = cursor.fetchall()
    
  columns = ['UUID','ENP','FAM','IM','OT','BIRTHDAY','PERSCODE','month','SMO','FILENAME','MO',
               'TYPE_MO','NPR_DATE','NPR_MO','VIDPOM','USL_OK','FOR_POM','P_CEL','C_ZAB','PROFIL',
               'BED_PROFILE','SPEC_CODE','DS0','DS1','DS1_PR','DS2','DS3','CODE_USL','KOL_USL',
               'GROUP_OMU','R_ISDENT','KD','NHISTORY','DN','SEX','DATE_1','DATE_2','ISHOD','RSLT',
               'TARIF','SUMV','CRIT','IDSP','IDDOKT','CODE_OTD','ORIT','REAB','DET','AGE','COUNTRY',
               'ED_COL']
  result = []
  for item in answer_temp:
    result.append(list(item))

  return pd.DataFrame(result, columns = columns) 