import discord
from discord.ext import commands
import datetime
import os
import os, requests, uuid, json
import pyodbc



botName = 'Alfonso'

key_var_name = 'TOKEN'
endpoint = 'https://api.cognitive.microsofttranslator.com'

class Traduccion(commands.Cog):
    @commands.command(aliases=["traducir", "trd"])
    async def translate(self, ctx, idioma_a_traducir: str, *, texto: str):
        """
        Traducir de un idioma a otro. El idioma fuente se reconoce a automáticamente.
        """
        
        
        headers = {
            'Ocp-Apim-Subscription-Key': key_var_name,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        try:
            path = '/translate?api-version=3.0'
            params = f'&to={idioma_a_traducir}'
            constructed_url = endpoint + path + params

            body = [{
                    'text': f'{texto}'
                    }]

            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()

            embed = discord.Embed(title=f':map: Traducción', color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name=f'**Texto traducido**', value=f"{response[0]['translations'][0]['text']}")
            embed.add_field(name=f'Detalles', value=f"``{response[0]['detectedLanguage']['language']} -> {response[0]['translations'][0]['to']}``")
            await ctx.send(embed=embed)

        except:
            path = '/translate?api-version=3.0'
            params = f'&to=es'
            constructed_url = endpoint + path + params

            error = response['error']['message']
            code = response['error']['code']

            body = [{
                'text': f'{error}'
            }]
            
            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()

            embed = discord.Embed(title=f' :map: Desafortunadamente ocurrió un error al traducir', color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name=f'**Descripción del error:**', value=f"{response[0]['translations'][0]['text']}")
            embed.add_field(name=f'**Código de error:**', value=f"``{code}``")
            await ctx.send(embed=embed)
        # else:

        #     lista_de_idiomas = """Afrikaans, árabe, bangla, bosnio (latino), búlgaro, cantonés (tradicional), catalán, chino simplificado, chino tradicional, croata, checo, danés, holandés, inglés, estonio, fiyiano, Filipino, finlandés, francés, alemán, griego, gujarati, criollo haitiano, hebreo, hindi, hmong Daw, húngaro, islandés, indonesio, irlandés, italiano, japonés, kannada, kiswahili, klingon, klingon, coreano, letón, lituano, malgache, malayo, malayalam, maltés, maorí, marathi, noruego, persa, polaco, portugués (Brasil), rumano, ruso, samoano, serbio (cirílico), serbio (latino), eslovaco, esloveno, español, sueco, tahitiano, tamil, telugu, tailandés, tongano, turco, ucraniano, urdu, vietnamita, galés, yucateco maya."""

        #     codigo_de_idiomas = """af,ar,bn,bs,bg,yue,ca,zh-Hans,zh-Hant,hr,cs,da,nl,en,et,fj,fil,fi,fr,de,el,gu,ht,he,hi,mww,hu,is,id,ga,it,ja,kn,sw,tlh,tlh-Qaak,ko,lv,lt,mg,ms,ml,mt,mi,mr,nb,fa,pl,pt-br,pt-pt,pa,otq,ro,ru,sm,sr-Cyrl,sr-Latn,sk,sl,es,sv,ta,te,th,to,tr,uk,ur,vi,cy,yua"""

        #     embed = discord.Embed(title=f':map: Traducción', color=discord.Color.blue())
        #     embed.add_field(name=f'**Utilización**', value=f"``$translate <idioma-de-destino> <texto>``\n\n**Ejemplo: **Traducción al japonés.\n``$translate ja Hola, hoy me siento bien.``\n\n**Código de los idiomas:**\n```{codigo_de_idiomas}```")
        #     await ctx.send(embed=embed)
        #     embed = discord.Embed(title=f'', color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        #     embed.add_field(name=f'**Idiomas disponibles:**', value=f"```{lista_de_idiomas}```")
        #     await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Traduccion(client))
