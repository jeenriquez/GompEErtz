#! /usr/bin/env python3
'''
Este codigo utiliza el clase GompEErtz para analizar casos confirmados, estimados o fallecidos de municipios, y estados de Mexico, asi como a nivel nacional.
'''

from .GompEErtz import *
from argparse import ArgumentParser
import matplotlib.pylab as plt

def main():

    parser = ArgumentParser(description='askGompEErtz [options]')

    parser.add_argument('-t',action='store', dest='data_type', type=str, default='M', help='Tipo de entidad (M/E/N). Defecto: E ')
    parser.add_argument('-l',action='store', dest='lugar', type=str, default='Chihuahua', help='Nombre del lugar. Defecto: Chihuahua ')
    parser.add_argument('-n',action='store', dest='nmin', type=int, default=1, help='Numero minimo de casos a analisar. Defecto: 1 ')
    parser.add_argument('-s', action='store', default=False, dest='savefig', help='Guardar figura. Defecto:False')
    parser.add_argument('-f', action='store', default=False, dest='fit_deaths', help='Analisar casos de fallecidos. Defecto:False')

    parse_args = parser.parse_args()

    #Initialize
    data_type = parse_args.data_type
    lugar = parse_args.lugar
    savefig = parse_args.savefig
    fit_deaths = parse_args.fit_deaths
    nmin = parse_args.nmin

    Gom_analysis(nmin=nmin,savefig=savefig,lugar=lugar,data_type=data_type,fit_deaths=fit_deaths)

def Gom_analysis(nmin=1,savefig=False,lugar='Chihuahua',data_type='M',fit_deaths=False):

    #---------------------------------------------------------------

    if data_type == 'M':
        this_one = '15'
    else:
        this_one = '14'


    if not fit_deaths:
        factor=0.4
        colores = ['red','lightcoral']

        colors = ['gold','orange','darkorange','peru','firebrick','red']
        labels = ['GP+40 ; Junio 06','GP+40 ; Junio %s'%this_one,'GP+40 ; Junio 21','GP+40 ; Junio 26','GP+40 ; Julio 07','GP+40 ; Julio 15']

    else:
        factor=0
        colores = ['b','lightblue']

        colors = ['DeepSkyBlue','dodgerblue','CornflowerBlue','CadetBlue','LightSteelBlue','k']
        labels = ['GP; Junio 06','GP; Junio %s'%this_one,'GP; Junio 21','GP; Junio 26','GP; Julio 07','GP; Julio 15']

    #---------------------------------------------------------------
    # Calcular los ajustes dependiendo el porcentaje de sospechosos

    #positivos_only
    gom = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths)

    if not fit_deaths:

        #positivos + 40% sospeshosos
        gom_40sos = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor)

        #positivos + sospeshosos
        gom_100sos = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=1)

    #-------
    #Plotting


    plt.ion()
    plt.figure()
    plt.bar(range(len(gom.cases_daily)),gom.cases_daily,color=colores[1],label='Confirmados')

    plt.plot(gom.mfit_day,'k-',label='Gompertz Ajuste a Confirmados (G)')
    plt.plot(gom.mfit_pronostico_day,'-',color=colores[0],label='Gompertz Pronostico a Confirmados (GP)')
    plt.plot(gom.mfit_day,'k-',label='')

    if not fit_deaths:
        plt.plot(gom_40sos.mfit_pronostico_day,'--',color='firebrick',label='GP + 40% de Sospechosos')
        plt.plot(gom_100sos.mfit_pronostico_day,'-.',color='peru',label='GP + 100% de Sospechosos')

    text(0, gom.cases_daily.max()/2,gom.dias[0], rotation=90, verticalalignment='top')
    text(len(gom.mfit_day), gom.cases_daily.max()/2,gom.dias[-1], rotation=90, verticalalignment='top')

    plt.vlines(len(gom.dias),-5,np.nanmax(gom.cases_daily)*1.1,colors='Gray',label=gom.dias[-1])
    plt.ylim(0,np.nanmax(gom.cases_daily)*1.05)

    plt.hlines(nmin,-1*nmin,int(len(gom.mfit_pronostico_day)*0.9),linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
    plt.xlim(-2,int(len(gom.mfit_pronostico_day)*0.8))

    plt.legend()
    plt.xlabel('Dias desde %s '%gom.dia_init)
    plt.ylabel('Casos Diarios')
    plt.title('Casos diarios %s. %s'%(gom.entidad,gom.lugar_name))

    if savefig:
        plt.savefig('../results/gom_pronostico_%s_%s_%s.png'%(gom.entidad,gom.lugar_name,gom.dated),dpi=300)

    #---------------------------------------------------------------
    # Calcular el cambio de pronostico devido a actualizacion de datos.

    if data_type == 'M':
        this_one = '20200615'
    else:
        this_one = '20200614'

    #positivos + 40% sospeshosos
    gom_40sos_0606 = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor,dated='20200606')
    gom_40sos_0614 = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor,dated=this_one)
    gom_40sos_0621 = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor,dated='20200621')
    gom_40sos_0626 = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor,dated='20200626')
    gom_40sos_0707 = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor,dated='20200707')
    gom_40sos_0715 = GompEErtz(data_type=data_type,lugar=lugar,nmin=nmin,fit_deaths=fit_deaths,factor=factor,dated='20200715')

    #-------
    #Plotting

    plt.ion()
    plt.figure()

    plt.plot(gom_40sos_0606.mfit_pronostico_day,'-.',color=colors[0],label=labels[0])
    plt.plot(gom_40sos_0614.mfit_pronostico_day,'--',color=colors[1],label=labels[1])
    plt.plot(gom_40sos_0621.mfit_pronostico_day,'-.',color=colors[2],label=labels[2])
    plt.plot(gom_40sos_0626.mfit_pronostico_day,'--',color=colors[3],label=labels[3])
    plt.plot(gom_40sos_0707.mfit_pronostico_day,'--',color=colors[4],label=labels[4])
    plt.plot(gom_40sos_0715.mfit_pronostico_day,'-.',color=colors[5],label=labels[5])

    plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos_0606.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
    plt.ylim(0,np.nanmax(gom_40sos_0606.mfit_pronostico_day)*1.05)

    plt.hlines(nmin,-1*nmin,int(len(gom_40sos_0715.mfit_pronostico_day)*0.9),linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
    plt.xlim(-2,int(len(gom_40sos_0715.mfit_pronostico_day)*0.8))

    plt.legend()
    plt.xlabel('Dias desde %s '%gom_40sos_0606.dia_init)
    plt.ylabel('Casos Diarios')
    plt.title('Casos diarios %s. %s'%(gom.entidad,gom.lugar_name))

    if savefig:
        plt.savefig('../results/gom_pronostico_%s_%s_multi_%s.png'%(gom.entidad,gom.lugar_name,gom.dated),dpi=300)

    #-------
    #Plotting

    gom.plot_tot_fit()

    if savefig:
        plt.savefig('../results/gom_pronostico_%s_%s_fit_%s.png'%(gom.entidad,gom.lugar_name,gom.dated),dpi=300)


if __name__ == "__main__":

    main()

