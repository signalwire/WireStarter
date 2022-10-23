const { Voice } = require('@signalwire/realtime-api')

const projectId = process.env.PROJECT_ID;
const token = process.env.REST_API_TOKEN;

const client = new Voice.Client({
 project: projectId,
 token: token,
 contexts: ["home","office"],
});

client.on("call.received", async (call) => {
 console.log("Got call", call.from, call.to);

 try {
  await call.answer();
  console.log("Inbound call answered");
  const playback = await call.playTTS({ text: "Welcome to SignalWire!" });
  await playback.waitForEnded();
  await call.hangup()
 } catch (error) {
  console.error("Error answering inbound call", error);
 }
});
