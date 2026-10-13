#!/usr/bin/python3
"""Populate TOC/table/figure fields with LibreOffice UNO, preserving DOCX fields."""
import sys, time, pathlib
import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.style.ParagraphAdjust import RIGHT

def prop(name,value):
 p=PropertyValue();p.Name=name;p.Value=value;return p
ctx=uno.getComponentContext();resolver=ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',ctx)
for i in range(30):
 try: remote=resolver.resolve('uno:socket,host=localhost,port=2003;urp;StarOffice.ComponentContext');break
 except Exception:time.sleep(.4)
else:raise RuntimeError('LibreOffice UNO connection unavailable')
sm=remote.ServiceManager;desktop=sm.createInstanceWithContext('com.sun.star.frame.Desktop',remote)
url=uno.systemPathToFileUrl(str(pathlib.Path(sys.argv[1]).resolve()))
doc=desktop.loadComponentFromURL(url,'_blank',0,(prop('Hidden',True),prop('UpdateDocMode',3)))
if doc is None:raise RuntimeError('Document failed to open')
styles=doc.getStyleFamilies().getByName('ParagraphStyles')
changed=[]
for name in styles.getElementNames():
 if name.startswith(('Contents ','Table Index','Illustration Index')):
  st=styles.getByName(name)
  try:
   st.CharFontNameComplex='Noto Naskh Arabic';st.CharHeightComplex=10.5;st.CharFontName='Times New Roman';st.CharHeight=10.5
   st.WritingMode=1;st.ParaAdjust=RIGHT
   st.ParaTopMargin=0;st.ParaBottomMargin=70
   st.CharWeightComplex=150.0 if name=='Contents 1' else 100.0
   st.CharWeight=150.0 if name=='Contents 1' else 100.0
   changed.append(name)
  except Exception: pass
for i in range(doc.getDocumentIndexes().getCount()):doc.getDocumentIndexes().getByIndex(i).update()
doc.refresh()
for i in range(doc.getDocumentIndexes().getCount()):doc.getDocumentIndexes().getByIndex(i).update()
doc.storeAsURL(url,(prop('FilterName','Office Open XML Text'),prop('Overwrite',True)))
print('Indexes:',doc.getDocumentIndexes().getCount(),'Styled:',changed)
doc.close(True)
