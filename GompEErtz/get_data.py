
import pandas as pd
import numpy as np
import pickle

import pdb

#--------------------
#

data_path = '../datos/'


def get_stdout_data(nmin = None, nmax = None,data_type='M',format='stdout',dated='20200707',lugar='CHIHUAHUA'):
    ''' Obtener datos estatales, nacionales o municipales en Mexico.
        Ejemplo:

        data_type = E   ; lugar = CHIHUAHUA
        data_type = M   ; lugar = Chihuahua
        data_type = N   ; lugar = Nacional
    '''

    if 'E' in data_type:
        datosI = pd.read_csv(get_file_name(data_type='EC',dated=dated))
        datosD = pd.read_csv(get_file_name(data_type='ED',dated=dated))
        datosS = pd.read_csv(get_file_name(data_type='ES',dated=dated))
    elif 'M' in data_type:
        datosI = pd.read_csv(get_file_name(data_type='MC',dated=dated))
        datosD = pd.read_csv(get_file_name(data_type='MD',dated=dated))
        datosS = pd.read_csv(get_file_name(data_type='MS',dated=dated))
    elif 'N' in data_type:
        lugar = 'Nacional'
        datosI = pd.read_csv(get_file_name(data_type='EC',dated=dated))
        datosD = pd.read_csv(get_file_name(data_type='ED',dated=dated))
        datosS = pd.read_csv(get_file_name(data_type='ES',dated=dated))
    else:
        raise ValueError('Valor de data_type incorrecto (E,M,N).')

    datosI = datosI[datosI['nombre'] == lugar]
    datosD = datosD[datosD['nombre'] == lugar]
    datosS = datosS[datosS['nombre'] == lugar]

    if len(datosI) == 0:
        raise ValueError('Valor de lugar no existe en base de datos.')

    if dated == '20200606':
        date_D = '04-02-2020'
        date_S = '29-01-2020'
    elif dated == '20200614':
        date_D = '05-03-2020'
        date_S = '29-01-2020'
    else:
        date_D = '17-03-2020'
        date_S = '29-01-2020'

    #Transposing and summing
    datosI = arrange_array(datosI)
    datosD = arrange_array(datosD)
    datosS = arrange_array(datosS)

    #Correction since date for Defunciones starts later ...
    tt = get_number_days_until(data_type=data_type,date=date_D)  # Before '17-03-2020'
    dias = datosI['Dias'].tolist()[:tt]
    datos_dic = {'Dias': dias,'Numero personas diarias': np.zeros(tt,dtype=int),'Numero personas totales': np.zeros(tt,dtype=int)}
    zero_datos = pd.DataFrame(data=datos_dic)
    datosD = pd.concat([zero_datos,datosD])

    #Correction since date for Sospechosos starts later ...
    tt2 = get_number_days_until(data_type=data_type,date=date_S)   # Before '22-03-2020'
    dias2 = datosI['Dias'].tolist()[:tt2]
    datos_dic2 = {'Dias': dias2,'Numero personas diarias': np.zeros(tt2,dtype=int),'Numero personas totales': np.zeros(tt2,dtype=int)}
    zero_datos2 = pd.DataFrame(data=datos_dic2)
    datosS = pd.concat([zero_datos2,datosS])

    datosI.reset_index(drop=True, inplace=True)
    datosD.reset_index(drop=True, inplace=True)
    datosS.reset_index(drop=True, inplace=True)

    if nmin and nmax:
        if nmin > nmax:
            nmin, nmax = nmax, nmin
    if nmax:
        datosI = datosI[datosI['Numero personas diarias'] < nmax]
        datosD = datosD[datosI['Numero personas diarias'] < nmax]
        datosS = datosS[datosI['Numero personas diarias'] < nmax]
        raise DrepecationError('We have some max',nmax)
    if nmin:
        indexI = datosI[datosI['Numero personas diarias'] >= nmin].index[0]
        datosI = datosI.loc[indexI:]
        datosD = datosD.loc[indexI:]
        datosS = datosS.loc[indexI:]

    #Make sure they are the same size.
    if len(datosI) != len(datosS) or len(datosI) != len(datosD):
        datosD = datosD[:len(datosI)]
        datosS = datosS[:len(datosI)]

    if format == 'stdout':
        return np.array(datosI['Numero personas diarias'].tolist()), np.array(datosD['Numero personas totales'].tolist()), np.array(datosS['Numero personas diarias'].tolist())
    elif format == 'all':
        datosI.reset_index(drop=True, inplace=True)
        datosD.reset_index(drop=True, inplace=True)
        datosS.reset_index(drop=True, inplace=True)
        return datosI, datosD, datosS
    elif format == 'deaths':
        datosD.reset_index(drop=True, inplace=True)
        return datosD
    else:
        datosI.reset_index(drop=True, inplace=True)
        datosS.reset_index(drop=True, inplace=True)
        return datosI, datosS



def get_file_name(data_type='MC',dated='20200606'):

    if dated:
        dated = '_'+dated
    else:
        raise ErrorValue('No dated given.')

    file_name = data_path+'Casos_Diarios'

    if 'E' in data_type:
        file_name += '_Estado_Nacional'
    elif 'M' in data_type:
        file_name += '_Municipio'

    if 'C' in data_type:
        file_name += '_Confirmados'
    elif 'D' in data_type:
        file_name += '_Defunciones'
    elif 'S' in data_type:
        file_name += '_Sospechosos'
    else:
        pass

    return file_name+dated+'.csv'

def arrange_array(datos):
    '''Transposing and calculating totals.
    '''

    #Arrange array
    dates = list(datos.columns[3:])
    indx = datos['cve_ent'].index[0]
    datos = datos.T
    num1 = np.array(datos[indx].tolist()[3:])
    sum1 = num1.cumsum()

    datos_dic = {'Dias': dates,'Numero personas diarias': num1,'Numero personas totales': sum1}

    datos = pd.DataFrame(data=datos_dic)

    return datos

def get_number_days_until(data_type='M',date='2020-02-02',nmin = None):

    dias = 'Dias'

    if 'M' in data_type:
        data_type='MCD'
    else:
        data_type='ECD'

    total_data = get_column_data_Chih(data_type=data_type,nmin=nmin,format='all')

    try:
        return total_data[total_data[dias] == date].index[0] - total_data.index[0]
    except:
        raise ValueError('Earliest date in selected data is %s'%total_data.iloc[0][dias])

def get_column_data_Chih(nmin = None, nmax = None, data_type='MCD',format='column',date=''):
    ''' Get total cases in Chihuahua '''


    if 'E' in data_type:
        lugar = 'CHIHUAHUA'
    elif 'M' in data_type:
        lugar = 'Chihuahua'

    if data_type == 'MCD' or data_type == 'MCT':
        datos = pd.read_csv(get_file_name(data_type='MC'))
    elif data_type == 'MDD' or data_type == 'MDT':
        datos = pd.read_csv(get_file_name(data_type='MD'))
    elif data_type == 'MSD' or data_type == 'MST':
        datos = pd.read_csv(get_file_name(data_type='MS'))
    elif data_type == 'ECD' or data_type == 'ECT':
        datos = pd.read_csv(get_file_name(data_type='EC'))
    elif data_type == 'EDD' or data_type == 'EDT':
        datos = pd.read_csv(get_file_name(data_type='ED'))
    elif data_type == 'ESD' or data_type == 'EST':
        datos = pd.read_csv(get_file_name(data_type='ES'))
    else:
        raise ValueError('Need valid value for data_type.')

    datos = datos[datos['nombre'] == lugar]
    datos = arrange_array(datos)

    if 'T' in data_type:
        columna = 'Numero personas totales'
    else:
        columna = 'Numero personas diarias'

    if date:
        indx = datos[datos['Dias'] == date].index[0]
        datos = datos.loc[indx:]
    else:
        if nmin and nmax:
            if nmin > nmax:
                nmin, nmax = nmax, nmin
        if nmax:
            datos = datos[datos[columna] < nmax]
        if nmin:
            datos = datos.loc[datos[datos[columna] >= nmin].index[0]:]
    #         datos = datos[datos[columna] > nmin]

    if format == 'column':
        return np.array(datos[columna].tolist())
    elif format == 'all':
        return datos
    else:
        return np.array(datos)



def save_data(nmin=1,data_type='M',lugar='CHIHUAHUA'):
    '''   '''

    if 'E' in data_type:
        lugar = 'Edo.' + lugar
    elif 'M' in data_type:
        lugar = 'Mpio.' + lugar
    elif 'N' in data_type:
        lugar = lugar
    else:
        lugar = ''

    datosI, datosD, datosS = get_stdout_data(nmin=nmin,data_type=data_type,format='all',lugar=lugar)

    datosI.reset_index(drop=True, inplace=True)
    datosI.to_csv(data_path+'datos_gobmx_%s_Infectados.csv'%lugar)
    datosD.reset_index(drop=True, inplace=True)
    datosD.to_csv(data_path+'datos_gobmx_%s_Fallecidos.csv'%lugar)
    datosS.reset_index(drop=True, inplace=True)
    datosS.to_csv(data_path+'datos_gobmx_%s_Sospechosos.csv'%lugar)






