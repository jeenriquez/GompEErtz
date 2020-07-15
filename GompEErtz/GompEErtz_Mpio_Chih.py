from GompEErtz import *


nmin = 2

#---------------------------------------------------------------
# Calcular los ajustes dependiendo el porcentaje de sospechosos

#positivos_only
gom = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin)

#positivos + 40% sospeshosos
gom_40sos = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4)

#positivos + sospeshosos
gom_100sos = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=1)

#-------
#Plotting

plt.ion()
plt.figure()
#plt.plot(gom.cases_daily,'+',color='lightcoral',label='Chihuahua Positivos')
plt.bar(range(len(gom.cases_daily)),gom.cases_daily,color='lightcoral',label='Chihuahua Confirmados')

plt.plot(gom.mfit_day,'k-',label='gompertz ajuste a confirmados (G)')
plt.plot(gom.mfit_pronostico_day,'-',color='red',label='gompertz pronostico a confirmados (GP)')
plt.plot(gom.mfit_day,'k-',label='')


plt.plot(gom_40sos.mfit_pronostico_day,'--',color='firebrick',label='GP + 40% de sospechosos')
plt.plot(gom_100sos.mfit_pronostico_day,'-.',color='peru',label='GP + 100% de sospechosos')

#plt.vlines(x=[0,len(gom.mfit_day)],ymin=-10,ymax=100, color = 'Gray')

text(0, gom.cases_daily.max()/2,gom.dias[0], rotation=90, verticalalignment='top')
text(len(gom.mfit_day), gom.cases_daily.max()/2,gom.dias[-1], rotation=90, verticalalignment='top')
#plt.xticks([0,len(gom.mfit_day)], [gom.dias[0],gom.dias[-1]], rotation='vertical')

plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.cases_daily)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(0,np.nanmax(gom_40sos.cases_daily)*1.05)

plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
plt.xlim(-2,165)

plt.legend()
plt.xlabel('Dias desde %s '%gom.dia_init)
plt.ylabel('Casos Diarios')
plt.title('Casos diarios Mpio. Chih')
plt.savefig('../results/gom_pronostico_Mpio_%s.png'%gom.dated,dpi=300)

#---------------------------------------------------------------
# Calcular el cambio de pronostico devido a actualizacion de datos.


#positivos + 40% sospeshosos
gom_40sos_0606 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200606')
gom_40sos_0614 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200615')
gom_40sos_0621 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200621')
gom_40sos_0626 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200626')
gom_40sos_0707 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200707')

#-------
#Plotting

plt.ion()
plt.figure()

plt.plot(gom_40sos_0606.mfit_pronostico_day,'--',color='firebrick',label='GP+40 ; Junio 06')
plt.plot(gom_40sos_0614.mfit_pronostico_day,'--',color='darkorange',label='GP+40 ; Junio 15')
plt.plot(gom_40sos_0621.mfit_pronostico_day,'--',color='peru',label='GP+40 ; Junio 21')
plt.plot(gom_40sos_0626.mfit_pronostico_day,'--',color='darkkhaki',label='GP+40 ; Junio 26')
plt.plot(gom_40sos_0707.mfit_pronostico_day,'--',color='gold',label='GP+40 ; Julio 07')

plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(-0.5,np.nanmax(gom_40sos.mfit_pronostico_day)*1.05)

plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
plt.xlim(-2,165)

plt.legend()
plt.xlabel('Dias desde %s '%gom_40sos_0606.dia_init)
plt.ylabel('Casos Diarios')
plt.title('Casos diarios Mpio. Chih')
plt.savefig('../results/gom_pronostico_Mpio_multi_%s.png'%gom.dated,dpi=300)

#---------------------------------------------------------------
# Calcular el cambio de pronostico con respecto al limites iniciales

#positivos + 40% sospeshosos
gom_40sos_nmin1 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=1,factor=0.4)
gom_40sos_nmin2 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=2,factor=0.4)
gom_40sos_nmin5 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=5,factor=0.4)

#-------
#Plotting

#Issue : start day

plt.ion()
plt.figure()

plt.bar(range(len(gom_40sos_nmin1.cases_daily)),gom_40sos_nmin1.cases_daily,color='lightcoral',label='Chihuahua Confirmados')

plt.plot(gom_40sos_nmin1.mfit_pronostico_day,'--',color='firebrick',label='GP+40 ; lim 1 caso')
plt.plot(list(np.ones(18)*np.NaN)+list(gom_40sos_nmin2.mfit_pronostico_day),'--',color='peru',label='GP+40 ; lim 2 casos')
plt.plot(list(np.ones(33)*np.NaN)+list(gom_40sos_nmin5.mfit_pronostico_day),'--',color='olive',label='GP+40 ; lim 5 casos')

nmin=1
plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
nmin=5
plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='k', label='Limite %i casos'%nmin)
plt.xlim(-2,165)

plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.cases_daily)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(0,np.nanmax(gom_40sos.cases_daily)*1.05)

plt.legend()
plt.xlabel('Dias desde %s '%gom_40sos_nmin1.dia_init)
plt.ylabel('Casos Diarios')
plt.title('Casos diarios Mpio. Chihuahua')
plt.savefig('../results/gom_pronostico_Mpio_multilim_%s.png'%gom.dated,dpi=300)

#-------
#Plotting

gom_40sos.plot_tot_fit()
plt.savefig('../results/gom_pronostico_Mpio_fit_%s.png'%gom.dated,dpi=300)

