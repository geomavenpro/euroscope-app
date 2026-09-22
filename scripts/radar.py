import json, os, re, hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

SOURCES=[
 ('AÇA Türkiye','https://aca.csb.gov.tr/','career'),
 ('EEA Careers','https://www.eea.europa.eu/en/about/careers/vacancies','career'),
 ('Copernicus Land','https://land.copernicus.eu/en/news','eo'),
 ('Copernicus Data Space','https://dataspace.copernicus.eu/news','eo'),
 ('Eionet','https://www.eionet.europa.eu/','eionet'),
]
OUT=Path('docs/data/items.json'); HEAD={'User-Agent':'EuroScope/3.0 (+personal monitoring)'}
KEYWORDS=['sne','seconded national expert','ulusal uzman','geçici görevli','vacanc','expert','copernicus','sentinel','openeo','api','dataset','product','eionet','reportnet','earth observation','land cover','urban atlas','ground motion','climate','water','vegetation','soil','stac','odata']
LESSONS=[
 {'topic':'Sentinel-1','what':'C-band SAR uydusu; gece-gündüz ve buluttan büyük ölçüde bağımsız radar gözlemi sağlar.','use':'Deformasyon, taşkın, toprak nemi ve arazi değişimi.','you':'PS-InSAR ve afet/şehir izleme çalışmalarında.','idea':'Ankara veya İstanbul için Sentinel-1 zaman serisiyle yüzey hareketi taraması.','url':'https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-1'},
 {'topic':'Sentinel-2','what':'13 spektral bantlı optik kara gözlem görevi.','use':'Bitki, su, yangın, arazi örtüsü ve kentsel değişim.','you':'NDVI/NBR/NDCI ve CLMS doğrulama çalışmalarında.','idea':'CLMS arazi örtüsü ile Sentinel-2 değişim indekslerini karşılaştır.','url':'https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-2'},
 {'topic':'Sentinel-3','what':'Kara ve okyanus yüzeyi için optik, termal ve altimetri gözlemleri sağlar.','use':'Deniz rengi, yüzey sıcaklığı, bitki ve su izleme.','you':'İzmir Körfezi gibi kıyı su kalitesi çalışmalarında Sentinel-2 ile birlikte.','idea':'Sentinel-2/3 klorofil göstergelerinin mekânsal-ölçek karşılaştırması.','url':'https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-3'},
 {'topic':'Sentinel-5P','what':'Atmosfer bileşenlerini ölçen TROPOMI sensörlü görev.','use':'NO₂, SO₂, CO, CH₄, ozon ve aerosol izleme.','you':'Şehirler, sanayi ve iklim/çevre kesişiminde yeni makale hattı açabilir.','idea':'Ankara’da NO₂ zaman serisini arazi kullanımı ve ulaşım göstergeleriyle ilişkilendir.','url':'https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-5p'},
 {'topic':'openEO API','what':'EO verisini indirmeden sunucu tarafında işlemek için açık bir API standardı.','use':'Python/R/JS ile veri küpü, zaman serisi ve toplu uydu analizi.','you':'GEE benzeri iş akışlarını doğrudan Copernicus Data Space üzerinde öğrenmek için.','idea':'Aynı Sentinel-2 analizini GEE ve openEO ile çalıştırıp yöntem/performans karşılaştırması yap.','url':'https://documentation.dataspace.copernicus.eu/APIs/openEO.html'},
 {'topic':'STAC','what':'Uydu ve coğrafi varlıkları standart JSON katalogları üzerinden aramayı sağlayan spesifikasyon.','use':'Tarih, konum ve koleksiyona göre programatik veri keşfi.','you':'Python/Colab veri toplama aşamasını otomatikleştirmek için.','idea':'Türkiye için tekrarlanabilir Sentinel veri keşif modülü geliştir.','url':'https://documentation.dataspace.copernicus.eu/APIs/STAC.html'},
 {'topic':'OData API','what':'Copernicus Data Space kataloğunda ürün arama ve indirme için kullanılan API.','use':'Filtreli ürün sorgusu ve otomatik veri indirme.','you':'Toplu Sentinel arşivi oluşturacağın projelerde.','idea':'Afet öncesi/sonrası görüntüleri otomatik bulan küçük bir Python aracı yap.','url':'https://documentation.dataspace.copernicus.eu/APIs/OData.html'},
 {'topic':'Eionet & Reportnet','what':'Eionet, EEA ve ülkeler arasındaki çevre bilgi ağıdır; Reportnet raporlama/veri akışı altyapısıdır.','use':'Ulusal çevre verilerinin ortak veri akışlarıyla raporlanması.','you':'SNE hedefinde yalnız EO değil Avrupa çevre veri yönetişimini de göstermek için.','idea':'Türkiye’de bir çevre veri temasının Eionet veri akışına uyumunu CBS perspektifiyle incele.','url':'https://www.eionet.europa.eu/reportnet'},
 {'topic':'Copernicus Land Monitoring Service','what':'Arazi örtüsü, arazi kullanımı ve biyofiziksel değişkenler için Avrupa ve küresel ürünler sunar.','use':'CORINE, Urban Atlas, imperviousness, vegetation ve benzeri hazır katmanlar.','you':'Türkiye analizlerinde Sentinel’den türettiğin sonuçları referans ürünlerle birleştirmek için.','idea':'Urban Atlas/CLMS ürünü ile Sentinel tabanlı kentsel büyüme analizini karşılaştır.','url':'https://land.copernicus.eu/'},
]

def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def potential(title,kind):
 t=title.lower()
 if any(k in t for k in ['sne','seconded national','ulusal uzman','geçici görevli']): return 'YÜKSEK — AÇA/SNE hedefinle doğrudan ilgili; koşul ve son tarihi hemen kontrol et.'
 if kind=='career' and any(k in t for k in ['vacanc','expert','ilan']): return 'YÜKSEK — EEA/AÇA kariyer fırsatı olabilir; CBS, veri ve Earth Observation rollerini kontrol et.'
 if any(k in t for k in ['sentinel','openeo','api','dataset','product','stac','odata','land cover']): return 'YÜKSEK — Öğrenme + Türkiye uygulaması + CV/makale çıktısına dönüşme potansiyeli var.'
 if kind=='eionet' or any(k in t for k in ['eionet','reportnet']): return 'ORTA-YÜKSEK — Avrupa çevre veri akışlarını öğrenmek SNE profiline doğrudan katkı sağlar.'
 return 'ORTA — Somut veri/yöntem içeriyorsa kısa uygulama veya teknik nota çevrilebilir.'

def scrape(name,url,kind):
 r=requests.get(url,headers=HEAD,timeout=35); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser'); items=[]
 for a in soup.find_all('a',href=True):
  title=clean(a.get_text(' ',strip=True)); low=title.lower()
  if len(title)<12 or not any(k in low for k in KEYWORDS): continue
  href=urljoin(url,a['href'])
  if href.startswith(('mailto:','javascript:')): continue
  context=clean(a.parent.get_text(' ',strip=True))[:360] if a.parent else title
  uid=hashlib.sha1((name+'|'+href+'|'+title).encode()).hexdigest()[:16]
  items.append({'id':uid,'source':name,'kind':kind,'title':title,'url':href,'summary':context,'potential':potential(title,kind)})
 seen=set(); out=[]
 for x in items:
  if x['url'] not in seen: seen.add(x['url']); out.append(x)
 return out[:50]

def main():
 old=[]
 if OUT.exists():
  try: old=json.loads(OUT.read_text(encoding='utf-8')).get('items',[])
  except: pass
 oldids={x['id'] for x in old}; oldmap={x['id']:x for x in old}; now=datetime.now(timezone.utc); allitems=[]; errors=[]
 for n,u,k in SOURCES:
  try: allitems += scrape(n,u,k)
  except Exception as e: errors.append(f'{n}: {e}')
 uniq={x['id']:x for x in allitems}; items=list(uniq.values())
 for x in items: x['first_seen']=oldmap.get(x['id'],{}).get('first_seen',now.isoformat())
 lesson=LESSONS[now.toordinal()%len(LESSONS)]
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps({'updated_at':now.isoformat(),'items':items,'lesson':lesson,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
 new=[x for x in items if x['id'] not in oldids]
 if old:
  p=[x for x in new if 'YÜKSEK' in x['potential']][:4]
  lines=[]
  if p:
   lines=['🌍 EuroScope — yeni gelişmeler']
   for x in p: lines += [f"\n• {x['title']}",f"{x['source']} — {x['potential']}",x['url']]
  lines += [f"\n🎓 Bugünün kartı: {lesson['topic']}",lesson['what'],f"Sen nerede kullanırsın? {lesson['you']}",f"💡 {lesson['idea']}",lesson['url']]
 print(f'{len(items)} item, {len(new)} new, errors={errors}')
if __name__=='__main__': main()
