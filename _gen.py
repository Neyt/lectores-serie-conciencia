#!/usr/bin/env python3
"""Genera las páginas de lectores beta. Uso: python3 gen.py  (actualiza la versión de caché de los PDF)."""
import datetime, html, os

V = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')
SERIE = 'El Estudio de la Conciencia'

BOOKS = [
 dict(slug='mentes-x4p9', vol='I', title='Cómo las mentes raras dan forma a la realidad',
      sub='Conciencia, escasez y la arquitectura del genio', pdf='Mentes_Raras_lectura_beta.pdf',
      accent='#d6b16a', bg='#15130f',
      hook='Las mentes que cambian el mundo no son las más inteligentes. Son las más raras.',
      body=['En 13.800 millones de años de historia del universo, la conciencia reflexiva apareció una sola vez que sepamos. Esa rareza no es un accidente: es la pista para entender por qué un puñado de mentes ha dado forma desproporcionada a la realidad que todos habitamos.',
            'Este libro recorre la neurociencia, la física de redes, la teoría evolutiva y la historia de las ideas para responder una pregunta que pocos formulan: ¿por qué ciertos individuos, no los más brillantes sino los más integrados, terminan rediseñando el mundo?'],
      bullets=['Por qué la rareza cognitiva puede ser una ventaja y no un defecto.',
               'Cómo las redes amplifican el impacto de una sola mente fuera de lo común.',
               'Qué comparten los científicos, inversores y pensadores que transformaron su época.',
               'Cómo reconocer y cultivar los patrones de pensamiento de una mente rara.'],
      close='No es autoayuda. Es un mapa para quienes ya saben que piensan distinto y quieren entender por qué eso importa.'),
 dict(slug='moneda-q8m3', vol='II', title='La moneda de Dios',
      sub='Hongos, inteligencia artificial y la batalla por tu atención', pdf='La_Moneda_de_Dios_lectura_beta.pdf',
      accent='#e0b85c', bg='#0b1024',
      hook='Dos dioses. Una moneda. Y esa moneda eres tú.',
      body=['Dos inteligencias compiten en silencio por lo único que de verdad te pertenece: tu atención. Una lleva más de mil millones de años perfeccionando su oficio bajo el suelo del bosque: el reino de los hongos. La otra es joven, vive en tu bolsillo y aprende de ti a cada segundo: la inteligencia artificial que ordena tu feed.',
            'Ney Torres une la psicología profunda de Carl Jung con la neurociencia de la atención para responder una pregunta que casi nadie formula: ¿quién quiere tu mente y qué está dispuesto a hacer para conseguirla?'],
      bullets=['Un mapa de cinco niveles de la conciencia, del inconsciente colectivo al Sí-mismo.',
               'Por qué la psilocibina silencia la red neuronal por defecto y el algoritmo hace lo contrario.',
               'El Test de Mutualismo: cuatro preguntas para saber si una app te usa o tú la usas.',
               'Herramientas para recuperar la soberanía de tu atención sin renunciar a la tecnología.'],
      close='No es un libro contra las pantallas ni un manifiesto psicodélico. Es un mapa: no te dice a dónde ir, te dice dónde estás parado.'),
 dict(slug='anticristo-h7k2', vol='III', title='El Anticristo de Jung',
      sub='y el fin de nuestra sociedad', pdf='El_Anticristo_de_Jung_lectura_beta.pdf',
      accent='#dcb56a', bg='#12132e',
      hook='El Anticristo no llegó del cielo. Salió de nosotros.',
      body=['En 1951, Carl Gustav Jung publicó Aion, un libro difícil que casi nadie leyó fuera de los círculos especializados. Allí sostenía que el Anticristo no es una persona, sino la Sombra colectiva de una civilización que quiso ser solo luz.',
            'Setenta años después, esa Sombra tiene algoritmos, plataformas y una velocidad de contagio que Jung no podía imaginar. Este libro traduce Aion a un lenguaje claro y lo aplica a lo que vivimos hoy: la polarización, la propaganda, las redes sociales y la inteligencia artificial.'],
      bullets=['Qué es la Sombra y por qué la proyectamos sobre el enemigo de turno.',
               'Cómo se coordinan las masas sin que nadie dé la orden.',
               'Por qué el sistema teme al individuo que no puede comprar.',
               'Tres prácticas concretas para no quedar poseído por la Sombra colectiva.'],
      close='Un mapa para mirar lo que preferimos no ver.'),
]

HEAD = '''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow">
<meta name="referrer" content="no-referrer">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:{bg};--ink:#efe9dc;--muted:#b9b1a2;--accent:{accent};--line:rgba(255,255,255,.12)}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 Inter,system-ui,sans-serif}}
body:before{{content:"";position:fixed;inset:0;background:radial-gradient(1200px 600px at 70% -10%,rgba(255,255,255,.07),transparent 60%);pointer-events:none}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px;position:relative}}
.bar{{display:flex;justify-content:space-between;align-items:center;padding:18px 0;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
.hero{{display:grid;grid-template-columns:minmax(0,380px) 1fr;gap:56px;align-items:center;padding:28px 0 56px}}
.cover{{width:100%;height:auto;border-radius:6px;box-shadow:0 30px 60px -20px rgba(0,0,0,.8),0 0 0 1px var(--line)}}
.kicker{{color:var(--accent);font-size:13px;letter-spacing:.18em;text-transform:uppercase;font-weight:600}}
h1{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:clamp(38px,5.4vw,62px);line-height:1.02;margin:.25em 0 .15em}}
.sub{{font-family:"Cormorant Garamond",Georgia,serif;font-style:italic;font-size:clamp(20px,2.4vw,26px);color:var(--muted);margin:0 0 22px}}
.hook{{font-size:19px;font-weight:500;border-left:3px solid var(--accent);padding-left:14px;margin:0 0 26px}}
.btn{{display:inline-flex;align-items:center;gap:10px;background:var(--accent);color:#16120a;font-weight:600;text-decoration:none;padding:15px 24px;border-radius:999px;font-size:16px;transition:transform .15s,box-shadow .15s}}
.btn:hover{{transform:translateY(-1px);box-shadow:0 10px 24px -10px var(--accent)}}
.meta{{font-size:13px;color:var(--muted);margin-top:12px}}
section{{border-top:1px solid var(--line);padding:48px 0}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:48px}}
h2{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:32px;margin:0 0 14px;line-height:1.1}}
p{{margin:0 0 14px}} ul{{padding:0;margin:0;list-style:none}}
li{{padding:10px 0 10px 30px;position:relative;border-bottom:1px solid var(--line)}}
li:before{{content:"✦";position:absolute;left:4px;top:10px;color:var(--accent);font-size:13px}}
.beta{{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:14px;padding:28px}}
ol{{margin:0 0 18px;padding-left:20px}} ol li{{border:0;padding:4px 0}} ol li:before{{content:none}}
.close{{font-family:"Cormorant Garamond",Georgia,serif;font-style:italic;font-size:24px;color:var(--accent);margin-top:18px}}
footer{{padding:36px 0 48px;color:var(--muted);font-size:13px;border-top:1px solid var(--line)}}
@media (max-width:820px){{.hero,.cols{{grid-template-columns:1fr;gap:28px}}.hero{{padding-top:8px}}.cover{{max-width:300px;margin:0 auto;display:block}}}}
</style></head><body>'''

def page(b):
    e = html.escape
    href = f'{b["pdf"]}?v={V}'
    bl = ''.join(f'<li>{e(x)}</li>' for x in b['bullets'])
    body = ''.join(f'<p>{e(x)}</p>' for x in b['body'])
    return HEAD.format(title=e(b['title']), bg=b['bg'], accent=b['accent']) + f'''
<div class="wrap">
<div class="bar"><span>{SERIE}</span><span>Volumen {b["vol"]}</span></div>
<div class="hero">
  <img class="cover" src="portada.jpg" alt="Portada de {e(b["title"])}">
  <div>
    <div class="kicker">Ney Torres · Lectura beta</div>
    <h1>{e(b["title"])}</h1>
    <p class="sub">{e(b["sub"])}</p>
    <p class="hook">{e(b["hook"])}</p>
    <a class="btn" href="{href}" download rel="nofollow noopener">Descargar el PDF ↓</a>
    <div class="meta">Versión de prueba para lectores invitados · no la compartas públicamente</div>
  </div>
</div>
<section class="cols">
  <div><h2>De qué trata</h2>{body}<p class="close">{e(b["close"])}</p></div>
  <div><h2>Lo que vas a encontrar</h2><ul>{bl}</ul></div>
</section>
<section>
  <div class="beta">
    <h2>Cómo ayudarme como lector beta</h2>
    <p>Este es un manuscrito antes de su publicación. Tu lectura me sirve para pulirlo. No necesitas ser experto: me importa tu experiencia honesta como lector.</p>
    <ol>
      <li><b>Erratas y frases confusas:</b> anota la página y la frase.</li>
      <li><b>Dónde te aburriste o dejaste de leer:</b> es el dato más valioso.</li>
      <li><b>Datos o citas que te parezcan dudosos:</b> dime cuál y por qué.</li>
      <li><b>Lo que más te quedó:</b> una frase o idea que recuerdes una semana después.</li>
    </ol>
    <p>Envíame tus notas respondiendo al mensaje con el que recibiste este enlace. Si el PDF se actualiza, este mismo botón descargará siempre la versión más reciente.</p>
    <a class="btn" href="{href}" download rel="nofollow noopener">Descargar el PDF ↓</a>
  </div>
</section>
<section>
  <div class="beta">
    <h2>Tu reseña, el día del lanzamiento</h2>
    <p>Cuando el libro salga en Amazon te enviaré el enlace. Si lo leíste, una reseña honesta de una o dos líneas es la mayor ayuda que puede recibir un autor independiente: decide si el libro llega o no a lectores que no me conocen.</p>
    <p>No tiene que ser positiva. Tiene que ser tuya.</p>
  </div>
</section>
<footer>© {datetime.date.today().year} Ney Torres · {SERIE} · Página privada para lectores invitados.</footer>
</div></body></html>'''

for b in BOOKS:
    os.makedirs(b['slug'], exist_ok=True)
    open(f'{b["slug"]}/index.html', 'w').write(page(b))

open('index.html', 'w').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privado</title></head><body style="font:16px system-ui;background:#111;color:#999;display:grid;place-items:center;height:100vh;margin:0">Página privada.</body></html>')
open('404.html', 'w').write(open('index.html').read())
open('robots.txt', 'w').write('User-agent: *\nDisallow: /\n')
open('.nojekyll', 'w').write('')
print('versión', V)
