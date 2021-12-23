// Define configuration options
function setUpLink(channelName) {
    let opts = {
        identity: {
            username: "Yhl7",
            password: "PLEASE ENTER YOUR TWITCH PASSWORD CREDENTIAL"
        },
        channels: [
            channelName
        ]
    };
    const client = new tmi.client(opts);
    client.on('message', onMessageHandler);
    client.on('connected', onConnectedHandler);
    client.connect();
}


// https://rapidapi.com/twinword/api/sentiment-analysis


let sentimentList = [0, 0, 0];
let settings;
let commandName;

// Called every time a message comes in
function onMessageHandler(target, context, msg, self) {
    if (self) {
        return;
    }
    commandName = msg.trim();
    // console.log(commandName);

    settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/?text=" + commandName,
        "headers": {
            "x-rapidapi-host": "twinword-sentiment-analysis.p.rapidapi.com",
            "x-rapidapi-key": "PLEASE ENTER YOUR API KEY"
        }
    };
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler(addr, port) {
    console.log(`* Connected to ${addr}:${port}`);
}


