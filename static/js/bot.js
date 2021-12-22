// Define configuration options
const opts = {
    identity: {
        username: "Yhl7",
        password: "8mt1clasptu8nzn0l7dgoonhicom6i"
    },
    channels: [
        "xQcOW"
    ]
};

let sentence = "";
// Create a client with our options
const client = new tmi.client(opts);

// Register our event handlers (defined below)
client.on('message', onMessageHandler);
client.on('connected', onConnectedHandler);

// Connect to Twitch:
client.connect();

// https://rapidapi.com/twinword/api/sentiment-analysis
const settings = {
    "async": true,
    "crossDomain": true,
    "url": "https://api.twinword.com/api/sentiment/analyze/latest/?text=" + sentence,
    "method": "GET",
    "headers": {
        "Content-Type": "application/json",
        "Host": "api.twinword.com",
        "X-Twaip-Key": "YjOGT8qTVDV8HUnPOAbYCCrcGSlu3umY61BEP8sdZ3TTK17x3XYxidM95mFOap0SQrYWbm58hCj7MSgZmGsMxw=="
    }
};
setInterval(function () {
    $.ajax(settings).done(function (response) {
        console.log(response);
        sentence = "";
    });
}, 10000)


// Called every time a message comes in
function onMessageHandler(target, context, msg, self) {
    if (self) {
        return;
    }
    const commandName = msg.trim();
    console.log(commandName);
    sentence += commandName;
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler(addr, port) {
    console.log(`* Connected to ${addr}:${port}`);
}
