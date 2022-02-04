import io from "socket.io-client";
const ENDPOINT = "https://collabserver.shangkaul.repl.co";
export const socket = io(ENDPOINT);
