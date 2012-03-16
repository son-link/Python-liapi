#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  Python Liapi
#  
#  Copyright 2012 Alfonso Saavedra "Son Link" <sonlink.dourden@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Libreria para usar la API del proyecto OpenLibra <http://www.etnassoft.com/api-documentacion/>

import json, thread

from urllib import urlopen, urlretrieve
from re import search

class Liapi():
	
	def __init__(self):
		"""
		Iniciamos las variables que se uasaran en las distintas funciones de la clase
		"""
		
		self.lang = ''
		self.limit = int()
		
		# NO tocar esta linea salvo que cambie la url de la API
		self.__baseurl = 'http://www.etnassoft.com/api/v1/get/'
		
	def getData(self, *params):
		"""
		Esta función se encarga de mandar y recibir los datos necesarios en cada función
		"""
		
		lang = self.lang
		parameters = '?'
		limit = '&num_items=10'
		
		if lang == 'spanish' or lang == 'english':
			lang = '&lang=%s' % self.lang
		else:
			lang = '&lang=all'
		
		if self.limit:
			limit = '&num_items=%i' % self.limit
		
		for p in params:
			parameters += p
			
		print self.__baseurl+parameters+lang+limit
		
		data = urlopen(self.baseurl+parameters+lang+limit).read()
		
		if data or data != '([]);':
			return json.loads(data[1:-2])
		else:
			return False
		
	def getCat(self, catid):
		"""
		Muestra los libros de una categoria especifica
		"""
		
		if type(catid).__name__=='int':
			return 'category_id=%i' % catid
		else:
			return False
		
	def getBookInfo(self, bookid):
		"""
		esta función obtiene la información del libro seleccionado
		"""
		
		if type(bookid).__name__=='int':
			raw = urlopen(self.baseurl+'?id=%i' % bookid ).read()
			data = json.loads(raw[1:-2])
			for d in data:
				content = urlopen(d['url_details']).read()
				c = search('class="addthis_counter addthis_pill_style"></a></div><p>(.+)</p> <script', content )
				if c:
					data[0]['content'] = c.groups()[0]
					
			return data
			
		else:
			return False
			
	def criteria(self, crit):
		"""
		Devuelve una lista dependiendo del criterio seleccionado:
		1: Mas vistos
		2: Mas comentados
		3: Mas votados
		4: Mejor valorados 
		"""
		if type(tags).__name__=='list':
						
			if crit == 1:
				return 'criteria=most_viewed'
			elif crit == 2:
				return 'criteria=most_commented'
			elif crit == 3:
				return 'criteria=most_voted'
			elif crit == 4:
				return 'criteria=high_scored'
			else:
				return False
			
		else:
			return False

	def searchByTags(self, tags):
		"""
		Esta función se encarga de buscar libros por palabras claves.
		"""
		
		if type(tags).__name__=='list':
			return 'any_tags=%s' % tags
		else:
			return False
