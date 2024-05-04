import discord
import asyncio
import websockets

client = discord.Client()

async def send_message(channel, message):
    await channel.send(message)

async def read_messages(channel):
    async with websockets.connect(f'wss://gateway.discord.gg/?v=6&encording=json&compress=zlib-stream') as websocket:
        await websocket.send(json.dumps({
            'op': 2,
            'd': {
                'token': client.http.token,
                'properties': {
                    '$os': 'linux',
                    '$browser': 'discord.py',
                    '$device': 'discord.py'
                }
            }
        }))
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            if message['t'] == 'MESSAGE_CREATE':
                if message['d']['channel_id'] == channel.id:
                    await send_message(channel, f'{message["d"]["author"]["username"]}: {message["d"]["content"]}')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="I am alive"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('Pong!')

    if message.content.startswith('$status'):
        status = message.content.replace('$status ', '')
        await client.change_presence(activity=discord.Game(name=status))
        await message.channel.send(f'Status changed to {status}')

    if message.content.startswith('$read'):
        channel = message.channel
        await message.channel.send('Reading messages...')
        await read_messages(channel)

client.run('MTA0MDI1NzQzODE1NjMyODk2MA.GC_Y1y.ExN5KZIo465IqfabWIc5pcQHKHT1jp3eJGswXs')
