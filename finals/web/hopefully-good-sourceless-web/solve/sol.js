// Please update the encryptionKey and bounded variable sent over the network respectively in the next 2 lines
const rawKey = "IlhxujABmacY1t7Zh4vy34ke8EMmz0C8zJrxPyh0Mb0="
const arg = "6qteehwO166aQD9JAsL2DnQXuZeQTK5gnod9tYOioIQZRFiX8N3b+qQ/qcazcDvlzmB0x0BIaVMqELnHTFCRPRmpYgciyzYPSazXJph+4ZeW2fi/NcZfCPUV+94zH4aI0WhrXOKH0r+LJJF5"

function stringToUint8Array(binary) {
  const len = binary.length
  const arr = new Uint8Array(len)

  for (let i = 0; i < len; i++) {
    arr[i] = binary.charCodeAt(i)
  }

  return arr
}

function decrypt(key, iv, data) {
  return crypto.subtle.decrypt(
    {
      name: 'AES-GCM',
      iv,
    },
    key,
    data
  )
}

const textDecoder = new TextDecoder()

const key = await crypto.subtle.importKey(
	'raw',
	stringToUint8Array(atob(rawKey)),
	'AES-GCM',
	true,
	['encrypt', 'decrypt']
)

const originalPayload = atob(arg)
const ivValue = originalPayload.slice(0, 16)
const payload = originalPayload.slice(16)

console.log(textDecoder.decode(
  await decrypt(key, stringToUint8Array(ivValue), stringToUint8Array(payload))
))
