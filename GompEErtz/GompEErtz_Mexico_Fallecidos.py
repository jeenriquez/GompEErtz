from GompEErtz import *

nmin = 20
savefig = True

#---------------------------------------------------------------
# Calcular los ajustes con respecto al numero de fallecidos

#fallecidos
gom = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True)

#-------
#Plotting

plt.ion()
plt.figure()
plt.bar(range(len(gom.cases_daily)),gom.cases_daily,color='lightblue',label='Fallecidos')
plt.plot(gom.mfit_day,'k-',label='Gompertz Ajuste a Fallecidos (G)')
plt.plot(gom.mfit_pronostico_day,'-',color='b',label='Gompertz Pronostico a Fallecidos (GP)')
plt.plot(gom.mfit_day,'k-',label='')

text(0, gom.cases_daily.max(),gom.dias[0], rotation=90, verticalalignment='top')
text(len(gom.mfit_day)-1, gom.cases_daily.max(),gom.dias[-1], rotation=90, verticalalignment='top')

#plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
plt.xlim(-2,250)

plt.legend()
plt.xlabel('Dias desde %s '%gom.dia_init)
plt.ylabel('Fallecidos Diarios')
plt.title('Fallecidos diarios Mexico')
if savefig:
    plt.savefig('../results/gom_pronostico_Mexico_fallecidos_%s.png'%gom.dated,dpi=300)


#---------------------------------------------------------------
# Calcular el cambio de pronostico devido a actualizacion de datos.

#positivos
gom_0606 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True,dated='20200606')
gom_0614 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True,dated='20200614')
gom_0621 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True,dated='20200621')
gom_0626 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True,dated='20200626')
gom_0707 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True,dated='20200707')
gom_0715 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,fit_deaths=True,dated='20200715')

#-------
#Plotting

plt.ion()
plt.figure()

plt.plot(gom_0606.mfit_pronostico_day,'-.',color='DeepSkyBlue',label='GP; Junio 06')
plt.plot(gom_0614.mfit_pronostico_day,'--',color='dodgerblue',label='GP; Junio 14')
plt.plot(gom_0621.mfit_pronostico_day,'--',color='CornflowerBlue',label='GP; Junio 21')
plt.plot(gom_0626.mfit_pronostico_day,'-.',color='CadetBlue',label='GP; Junio 26')
plt.plot(gom_0707.mfit_pronostico_day,'--',color='LightSteelBlue',label='GP; Julio 07')
plt.plot(gom_0715.mfit_pronostico_day,'-.',color='k',label='GP; Julio 15')


#plt.hlines(nmin,-1*nmin,200,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
#plt.xlim(-2,250)
plt.xlim(-2,len(gom.mfit_pronostico_day))

plt.vlines(len(gom.dias),-5,np.nanmax(gom.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(-2,np.nanmax(gom.mfit_pronostico_day)*1.05)

plt.legend()
plt.xlabel('Dias desde %s '%gom_0606.dia_init)
plt.ylabel('Fallecidos Diarios')
plt.title('Fallecidos diarios Mexico')
if savefig:
    plt.savefig('../results/gom_pronostico_Mexico_fallecidos_multi_%s.png'%gom.dated,dpi=300)

#-------
#Plotting

gom.plot_tot_fit()
if savefig:
    plt.savefig('../results/gom_pronostico_Mexico_fallecidos_fit_%s.png'%gom.dated,dpi=300)

