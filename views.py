#-------Librerias---------


from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.core.files.storage import FileSystemStorage
from BIO_script.SARS import analysis
import shutil
import csv
import os



#------Variables-----
direc=""
retorno=[]
col1=[]
col2=[]
col3=[]
col4=[]
col5=[]
col6=[]
Error=""
marcador=False
y=0

def inicio(request):
	return render(request,"index.html")#iniciamos el index.hmtl


def form(request): #pagina form

	global direc
	global retorno
	global Error
	global marcador
	global y
	global ista_error
	n=0

	Error=""
	lista=[]
	col1=[]
	col2=[]
	col3=[]
	col4=[]
	col5=[]
	col6=[]
	response = render(request, 'form.html')

	try:
		if request.method == "POST":

			Archivo1= request.FILES['file1']
			Archivo2= request.FILES['file2']
			folder = "media/Temp/"
			fs = FileSystemStorage(location=folder)  
			filename1 = fs.save(Archivo1.name, Archivo1)
			filename2 = fs.save(Archivo2.name, Archivo2)
			direc1=folder+str(Archivo1)
			direc2=folder+str(Archivo2)
			retorno=analysis(direc1,direc2)
			os.remove(direc1)
			os.remove(direc2)
			if retorno[0]=="":
				folder = "media/"
				numero=len(os.listdir(folder))
				carpeta="media/Archivo"+str(numero)+"/"
				fs = FileSystemStorage(location=carpeta) 
				filename1 = fs.save(Archivo1.name, Archivo1)
				filename2 = fs.save(Archivo2.name, Archivo2)
				Archivo=retorno[2]
				limp = Archivo.split('/')
				caracter=len(limp)
				Archivo=limp[caracter-1]
				direc=carpeta+Archivo
				shutil.move(retorno[2], direc)
				marcador= True
				f=open(direc,"r")
				for i in f:
					n=n+1
					if n>2:
						i=i.split("\t")
						lista.append(i)
				try:
					dat1=request.COOKIES['dato1']
					dat2=request.COOKIES['dato2']
					dat3=request.COOKIES['dato3']
					dat4=request.COOKIES['dato4']
					dat5=request.COOKIES['dato5']
					dat6=request.COOKIES['dato6']

					dat1=dat1.split("'")
					dat2=dat2.split("'")
					dat3=dat3.split("'")
					dat4=dat4.split("'")
					dat5=dat5.split("'")
					dat6=dat6.split("'")
					for i in range(1,len(dat1)):
						if i%2!=0:
							col1.append(dat1[i])
							col2.append(dat2[i])
							col3.append(dat3[i])
							col4.append(dat4[i])
							col5.append(dat5[i])

					for i in range(1,len(dat6)):
						if i%2!=0:
							temp=len(dat6[i])
							dato=dat6[i]
							dato=dato[:temp - 1]
							col6.append(dato)
				except:
					pass

				for i in range(len(lista)):
					col1.append(lista[i][0])
					col2.append(lista[i][1])
					col3.append(lista[i][2])
					col4.append(lista[i][3])
					col5.append(lista[i][4])
					col6.append(lista[i][5])
				response =  redirect('/results')
				response.set_cookie(key='dato1', value=col1,max_age=10800)
				response.set_cookie(key='dato2', value=col2,max_age=10800)
				response.set_cookie(key='dato3', value=col3,max_age=10800)
				response.set_cookie(key='dato4', value=col4,max_age=10800)
				response.set_cookie(key='dato5', value=col5,max_age=10800)
				response.set_cookie(key='dato6', value=col6,max_age=10800)
				col1=[]
				col2=[]
				col3=[]
				col4=[]
				col5=[]
				col6=[]
				return response

			else:
				Error=retorno[0]

				return redirect('/form/error')
	except:
		try:
			os.remove(direc1)
			os.remove(direc2)
		except:
			pass
		Error="Error uploading files, please be sure that the two files are uploaded.If you are sure that your two files were correctly uploaded, possibly our server is busy, sorry for the inconvenience and please try again in a while."
		return redirect('/form/error')

	return response

def result(request):

	global marcador
	global col1
	global col2
	global col3
	global col4
	global col5
	global col6
	n=0
	lista=[]
	context={}
	response = render(request, 'results.html',context)
	if marcador==True:
		dat1=request.COOKIES['dato1']
		dat2=request.COOKIES['dato2']
		dat3=request.COOKIES['dato3']
		dat4=request.COOKIES['dato4']
		dat5=request.COOKIES['dato5']
		dat6=request.COOKIES['dato6']

		dat1=dat1.split("'")
		dat2=dat2.split("'")
		dat3=dat3.split("'")
		dat4=dat4.split("'")
		dat5=dat5.split("'")
		dat6=dat6.split("'")
		for i in range(1,len(dat1)):
			if i%2!=0:
				col1.append(dat1[i])
				col2.append(dat2[i])
				col3.append(dat3[i])
				col4.append(dat4[i])
				col5.append(dat5[i])

		for i in range(1,len(dat6)):
			if i%2!=0:
				temp=len(dat6[i])
				dato=dat6[i]
				dato=dato[:temp - 2]
				col6.append(dato)
		context={
		"col1":col1,
		"col2":col2,
		"col3":col3,
		"col4":col4,
		"col5":col5,
		"col6":col6,
		
		}
		col1=[]
		col2=[]
		col3=[]
		col4=[]
		col5=[]
		col6=[]
		marcador=False
	else:
		col1=[]
		col2=[]
		col3=[]
		col4=[]
		col5=[]
		col6=[]
		try:
			dat1=request.COOKIES['dato1']
			dat2=request.COOKIES['dato2']
			dat3=request.COOKIES['dato3']
			dat4=request.COOKIES['dato4']
			dat5=request.COOKIES['dato5']
			dat6=request.COOKIES['dato6']

			dat1=dat1.split("'")
			dat2=dat2.split("'")
			dat3=dat3.split("'")
			dat4=dat4.split("'")
			dat5=dat5.split("'")
			dat6=dat6.split("'")
			for i in range(1,len(dat1)):
				if i%2!=0:
					col1.append(dat1[i])
					col2.append(dat2[i])
					col3.append(dat3[i])
					col4.append(dat4[i])
					col5.append(dat5[i])

			for i in range(1,len(dat6)):
				if i%2!=0:
					temp=len(dat6[i])
					dato=dat6[i]
					dato=dato[:temp - 2]
					col6.append(dato)
		except:
			pass
		context={
		"col1":col1,
		"col2":col2,
		"col3":col3,
		"col4":col4,
		"col5":col5,
		"col6":col6,
		
		}
	if request.method == "POST":
		col1=[]
		col2=[]
		col3=[]
		col4=[]
		col5=[]
		col6=[]
		response.set_cookie(key='dato1', value="")
		response.set_cookie(key='dato2', value="")
		response.set_cookie(key='dato3', value="")
		response.set_cookie(key='dato4', value="")
		response.set_cookie(key='dato5', value="")
		response.set_cookie(key='dato6', value="")
		return response
	response = render(request, 'results.html',context)

	return response



#---------------------------------------------------------------------------------------



def about(request):

	return render(request,"about.html")

def contact(request):
	
	if request.method == "POST":
		nombre=request.POST["nombre"]
		institucion=request.POST["institucion"]
		correo=request.POST["correo"]
		titulo=request.POST["titulo"]
		texto=request.POST["texto"]
		mensaje="From:  "+str(nombre)+"\n"+"Email:  "+str(correo)+"\n"+"Institution:  "+str(institucion)+"\n----------------------------------\n\n\n"+""+str(texto)
		mail=EmailMessage(titulo,mensaje,to=["santiago.justo@urp.edu.pe"])
		mail.send()
		return redirect('/contact')


	return render(request,"contact.html")


def error(request):
	global Error

	context={
		"Error":Error,

		}
	Error=""
	return render(request,"error.html",context)

def explore(request):

	return render(request,"explore-haplotypes.html")

#---------------------post result-----------
def descriptives(request):

	return render(request,"descriptives.html")
def agps(request):

	return render(request,"agps.html")
def geo(request):

	return render(request,"Geo_An.html")
def nrf(request):

	return render(request,"NRFp.html")
def str_an(request):

	return render(request,"str_an.html")
def tem_an(request):

	return render(request,"Tem_An.html")

