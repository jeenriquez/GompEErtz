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

plt.subplot(2, 3, 1)
gom_40sos.plot_tot_fit(subplot=True,extra='A) ')

#-------
#Plotting

plt.subplot(2, 3, 2)

#plt.plot(gom.cases_daily,'+',color='lightcoral',label='Chihuahua Positivos')
plt.bar(range(len(gom.cases_daily)),gom.cases_daily,color='lightcoral',label='Confirmados')

plt.plot(gom.mfit_day,'k-',label='Gompertz Ajuste a Confirmados (G)')
plt.plot(gom.mfit_pronostico_day,'-',color='red',label='Gompertz Pronostico a Confirmados (GP)')
plt.plot(gom.mfit_day,'k-',label='')


plt.plot(gom_40sos.mfit_pronostico_day,'--',color='firebrick',label='GP + 40% de Sospechosos')
plt.plot(gom_100sos.mfit_pronostico_day,'-.',color='peru',label='GP + 100% de Sospechosos')

#plt.vlines(x=[0,len(gom.mfit_day)],ymin=-10,ymax=100, color = 'Gray')

text(0, gom.cases_daily.max()/2,gom.dias[0], rotation=90, verticalalignment='top')
text(len(gom.mfit_day), gom.cases_daily.max()/2,gom.dias[-1], rotation=90, verticalalignment='top')
#plt.xticks([0,len(gom.mfit_day)], [gom.dias[0],gom.dias[-1]], rotation='vertical')

plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.cases_daily)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(0,np.nanmax(gom_40sos.cases_daily)*1.15)

plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
plt.xlim(-2,165)

plt.legend()
plt.xlabel('Dias desde %s '%gom.dia_init)
plt.ylabel('Casos Diarios')
plt.title('B) Casos Diarios Mpio. Chihuahua')

#---------------------------------------------------------------
# Calcular el cambio de pronostico devido a actualizacion de datos.


#positivos + 40% sospeshosos
gom_40sos_0606 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200606')
gom_40sos_0614 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200615')
gom_40sos_0621 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200621')
gom_40sos_0626 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200626')
gom_40sos_0707 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200707')
gom_40sos_0715 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,factor=0.4,dated='20200715')


#-------
#Plotting

plt.subplot(2, 3, 3)

plt.plot(gom_40sos_0606.mfit_pronostico_day,'-.',color='gold',label='GP+40 ; Junio 06')
plt.plot(gom_40sos_0614.mfit_pronostico_day,'-.',color='orange',label='GP+40 ; Junio 15')
plt.plot(gom_40sos_0621.mfit_pronostico_day,'--',color='darkorange',label='GP+40 ; Junio 21')
plt.plot(gom_40sos_0626.mfit_pronostico_day,'--',color='peru',label='GP+40 ; Junio 26')
plt.plot(gom_40sos_0707.mfit_pronostico_day,'--',color='firebrick',label='GP+40 ; Julio 07')
plt.plot(gom_40sos_0715.mfit_pronostico_day,'-.',color='red',label='GP+40 ; Julio 15')


plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos_0606.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(-0.5,np.nanmax(gom_40sos_0606.mfit_pronostico_day)*1.05)

plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
plt.xlim(-2,165)

plt.legend()
plt.xlabel('Dias desde %s '%gom_40sos_0606.dia_init)
plt.ylabel('Casos Diarios')
plt.title('C) Casos Diarios Mpio. Chihuahua')

#---------------------------------------------------------------
#---------------------------------------------------------------
#Fallecidos

nmin = 1

#---------------------------------------------------------------
# Calcular los ajustes con respecto al numero de fallecidos

gom = GompEErtz(data_type='M',fit_deaths=True,lugar='Chihuahua',nmin=nmin,dated='20200707')

#-------
#Plotting

plt.subplot(2, 3, 4)
gom.plot_tot_fit(subplot=True,extra='D) ')

#-------
#Plotting

plt.subplot(2, 3, 5)

plt.bar(range(len(gom.cases_daily)),gom.cases_daily,color='lightblue',label='Fallecidos')

plt.plot(gom.mfit_day,'k-',label='Gompertz Ajuste a Fallecidos (G)')
plt.plot(gom.mfit_pronostico_day,'-',color='b',label='Gompertz Pronostico a Fallecidos (GP)')
plt.plot(gom.mfit_day,'k-',label='')

text(0, gom.cases_daily.max()/2,gom.dias[0], rotation=90, verticalalignment='top')
text(len(gom.mfit_day), gom.cases_daily.max()/2,gom.dias[-1], rotation=90, verticalalignment='top')

#plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
plt.xlim(-2,120)

plt.vlines(len(gom.dias),-5,np.nanmax(gom.cases_daily)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(0,np.nanmax(gom.cases_daily)*1.05)


plt.legend()
plt.xlabel('Dias desde %s '%gom.dia_init)
plt.ylabel('Fallecidos Diarios')
plt.title('E) Fallecidos Diarios Mpio. Chihhuahua')

#---------------------------------------------------------------
# Calcular el cambio de pronostico devido a actualizacion de datos.

#positivos
gom_0606 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,fit_deaths=True,dated='20200606')
gom_0615 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,fit_deaths=True,dated='20200615')
gom_0621 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,fit_deaths=True,dated='20200621')
gom_0626 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,fit_deaths=True,dated='20200626')
gom_0707 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,fit_deaths=True,dated='20200707')
gom_0715 = GompEErtz(data_type='M',lugar='Chihuahua',nmin=nmin,fit_deaths=True,dated='20200715')

#-------
#Plotting

plt.subplot(2, 3, 6)

plt.plot(gom_0606.mfit_pronostico_day,'-.',color='DeepSkyBlue',label='GP; Junio 06')
plt.plot(gom_0615.mfit_pronostico_day,'--',color='dodgerblue',label='GP; Junio 15')
plt.plot(gom_0621.mfit_pronostico_day,'--',color='CornflowerBlue',label='GP; Junio 21')
plt.plot(gom_0626.mfit_pronostico_day,'-.',color='CadetBlue',label='GP; Junio 26')
plt.plot(gom_0707.mfit_pronostico_day,'--',color='LightSteelBlue',label='GP; Julio 07')
plt.plot(gom_0715.mfit_pronostico_day,'-.',color='k',label='GP; Julio 15')


plt.hlines(1,-1,len(gom.mfit_pronostico_day)*2,linestyles='dotted',colors='Gray', label='Limite 1 caso')
plt.xlim(-2,len(gom.mfit_pronostico_day))

plt.vlines(len(gom.dias),-5,np.nanmax(gom.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(0,np.nanmax(gom.mfit_pronostico_day)*1.05)

plt.legend()
plt.xlabel('Dias desde %s '%gom_0606.dia_init)
plt.ylabel('Fallecidos Diarios')
plt.title('F) Fallecidos Diarios Mpio. Chihhuahua')


